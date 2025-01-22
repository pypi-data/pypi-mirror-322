"""
abstract for the photobooth-app backends
"""

import dataclasses
import logging
import os
import subprocess
import threading
import time
import uuid
from abc import ABC, abstractmethod
from enum import Enum, auto
from multiprocessing import Condition, Lock, shared_memory
from pathlib import Path

from ...utils.stoppablethread import StoppableThread
from ..config import appconfig

logger = logging.getLogger(__name__)


class EnumDeviceStatus(Enum):
    """enum for device status"""

    initialized = auto()
    starting = auto()
    running = auto()
    stopping = auto()
    stopped = auto()
    fault = auto()
    # halt = auto()


#
# Dataclass for stats
#


@dataclasses.dataclass
class BackendStats:
    """
    defines some common stats - if backend supports, they return these properties,
    if not, may be 0 or None
    """

    backend_name: str = __name__
    fps: int = None
    exposure_time_ms: float = None
    lens_position: float = None
    again: float = None
    dgain: float = None
    lux: float = None
    colour_temperature: int = None
    sharpness: int = None


class AbstractBackend(ABC):
    """
    photobooth-app abstract to create backends.
    """

    @abstractmethod
    def __init__(self):
        # statisitics attributes
        self._backendstats: BackendStats = BackendStats(backend_name=self.__class__.__name__)
        self._fps = 0
        self._stats_thread: StoppableThread = None

        # (re)connect supervisor attributes
        self._device_status: EnumDeviceStatus = EnumDeviceStatus.initialized
        # concrete backend implementation can signal using this flag there is an error and it needs restart.
        self._device_status_fault_flag: bool = False
        # used to indicate if the app requires this backend to deliver actually lores frames (live-backend or only one main backend)
        # default is to assume it's not responsible to deliver frames. once wait_for_lores_image is called, this is set to true.
        # the backend-implementation has to decide how to handle this once True.
        self._device_enable_lores_flag: bool = False
        # only for (webcam, picam and virtualcamera) error can detected by missing lores img
        self._failing_wait_for_lores_image_is_error: bool = False
        self._connect_thread: StoppableThread = None

        # video feature
        self._video_worker_capture_started = threading.Event()
        self._video_feature_available: bool = False
        self._video_worker_thread: StoppableThread = None
        self._video_recorded_videofilepath: Path = None
        self._video_framerate: int = None

        # services are responsible to create their folders needed for proper processing:
        os.makedirs("tmp", exist_ok=True)

        super().__init__()

    def __repr__(self):
        return f"{self.__class__}"

    def stats(self) -> BackendStats:
        self._backendstats.fps = int(round(self._fps, 0))
        return self._backendstats

    def _stats_fun(self):
        # FPS = 1 / time to process loop
        last_calc_time = time.time()  # start time of the loop

        # to calc frames per second every second
        while not self._stats_thread.stopped():
            try:
                self._wait_for_lores_image()  # blocks until new image is avail, we do not ready it here, only calc fps
                self._fps = 1.0 / (time.time() - last_calc_time)
            except Exception:
                # suffer in silence. If any issue occured assume the FPS is 0
                self._fps = 0

            # store last time
            last_calc_time = time.time()

    @property
    def device_status(self) -> EnumDeviceStatus:
        return self._device_status

    @device_status.setter
    def device_status(self, value: EnumDeviceStatus):
        logger.info(f"setting device status from {self._device_status.name} to {value.name}")
        self._device_status = value

    @property
    def device_enable_lores_stream(self) -> bool:
        return self._device_enable_lores_flag

    @device_enable_lores_stream.setter
    def device_enable_lores_stream(self, value: bool):
        logger.info(f"setting device enable_lores_flag from {self._device_enable_lores_flag} to {value} on backend {self.__class__.__name__}")
        self._device_enable_lores_flag = value

    def _connect_fun(self):
        while not self._connect_thread.stopped():  # repeat until stopped # try to reconnect
            # is running but problem detected!
            if self.device_status is EnumDeviceStatus.running and self._device_status_fault_flag is True:
                logger.info("implementation signaled a fault during run! set status to fault and try to recover.")
                self.device_status = EnumDeviceStatus.fault
                try:
                    self._device_stop()
                except Exception as exc:
                    logger.error(f"error stopping faulty backend {exc}, still trying to recover")

            # if running or stopping, busy waiting
            if self.device_status in (EnumDeviceStatus.running, EnumDeviceStatus.stopping):
                time.sleep(1)  # abort processing in these states, still need to delay
                continue

            if self.device_status in (EnumDeviceStatus.initialized, EnumDeviceStatus.stopped, EnumDeviceStatus.fault):
                logger.info(f"connect_thread device status={self.device_status}, so trying to start")
                self.device_status = EnumDeviceStatus.starting

            # if not connected, check for device availability as long as not requested to shut down.
            if self.device_status is EnumDeviceStatus.starting and not self._connect_thread.stopped():
                logger.info("trying to start backend")
                try:
                    # device available, start the backends local functions
                    if self._device_available():
                        logger.info("device is available")
                        self._device_start()

                        # after start ensure idle mode is selected.
                        self._on_configure_optimized_for_idle()

                        # clear the flag at this point
                        # if backend needs longer than the amount of time until wait_for_lores_image finally fails (example after 20 retries)
                        # the device could have set the flag in the meantime again during startup.
                        self._device_status_fault_flag = False

                        # when _device_start is finished, the device needs to be up and running, access allowed.
                        # signal that the device can be used externally in general.
                        self.device_status = EnumDeviceStatus.running
                        logger.info("device started, set status running")
                    else:
                        logger.error("device not available to (re)connect to, retrying")
                        # status remains starting, so in next loop it retries.
                        try:
                            self._device_stop()
                        except Exception as exc:
                            logger.error(f"error stopping faulty backend {exc}, still trying to recover")

                except Exception as exc:
                    logger.exception(exc)
                    logger.critical("device failed to initialize!")
                    self.device_status = EnumDeviceStatus.fault
                    try:
                        self._device_stop()
                    except Exception as exc:
                        logger.error(f"error stopping faulty backend {exc}, still trying to recover")

            time.sleep(1)
            # next after wait is to check if connect_thread is stopped - in this case no further actions.
            # means: sleep has to be last statement in while loop

        # supervising connection thread was asked to stop - so we ask device to do the sam
        logger.info("exit connection supervisor function, stopping device")
        self._device_stop()

    def _block_until_delivers_lores_images(self):
        # block until startup completed, this ensures tests work well and backend for sure delivers images if requested
        for _ in range(1, 20):
            try:
                self._wait_for_lores_image()  # blocks 0.5s usually. 10 retries default wait time=5s
                break  # stop trying we got an image can leave without hitting else.
            except TimeoutError:
                # if timeout occured it will retry several attempts more before finally fail
                continue
            except Exception as exc:
                raise RuntimeError("failed to start up backend due to error") from exc
        else:
            # didn't make it within (, xx) retries
            raise RuntimeError("giving up waiting for backend to start")

    def start(self):
        """To start the backend to serve"""

        # reset the request for this backend to deliver lores frames
        self.device_enable_lores_stream = False

        # disable video feature avail
        self._video_feature_available = False

        # statistics
        self._stats_thread = StoppableThread(name="_statsThread", target=self._stats_fun, daemon=True)
        self._stats_thread.start()

        # (re)connect supervisor
        self._connect_thread = StoppableThread(name="_connect_thread", target=self._connect_fun, daemon=True)
        self._connect_thread.start()

        if "PYTEST_CURRENT_TEST" in os.environ:
            # in pytest we need to wait for the connect thread properly set up the device.
            # if we do not wait, the test is over before the backend is acutually ready to deliver frames and might fail.
            # in reality this is not an issue
            logger.info("test environment detected, blocking until backend started")
            self.block_until_device_is_running()
            logger.info("backend started, finished blocking")

        # load ffmpeg once to have it in memory. otherwise first video might fail because startup time is not respected by implementation
        logger.info("running ffmpeg once to have it in memory later for video use")
        try:
            subprocess.run(
                args=["ffmpeg", "-version"],
                timeout=10,
                check=True,
                stdout=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            logger.warning("ffmpeg not found on system. this is not a problem if video functions are not used.")
        except subprocess.CalledProcessError as exc:
            # non zero returncode
            logger.error(f"ffmpeg returned an error: {exc}")
        except subprocess.TimeoutExpired as exc:
            logger.error(f"ffmpeg took too long to load, timeout {exc}")
        else:
            # no error, service restart ok
            logger.info("ffmpeg loaded successfully")
            self._video_feature_available = True

    def stop(self):
        """To stop the backend to serve"""

        self.stop_recording()

        if self._connect_thread and self._connect_thread.is_alive():
            self._connect_thread.stop()
            self._connect_thread.join()

        if self._stats_thread and self._stats_thread.is_alive():
            self._stats_thread.stop()
            self._stats_thread.join()

    def block_until_device_is_running(self):
        """Mostly used for testing to ensure the device is up.

        Returns:
            _type_: _description_
        """
        while self.device_status is not EnumDeviceStatus.running:
            logger.debug("waiting")
            time.sleep(0.2)

        logger.info("device status is running now")

    def device_set_status_fault_flag(self):
        if self.device_status is EnumDeviceStatus.running:
            logger.info("set flag to indicate fault in device despite backend shall be in running mode")
            self._device_status_fault_flag = True
        else:
            logger.info(f"ignored to flag device as faulty because not in running mode, mode is {self.device_status}")

    def wait_for_hq_image(self, retries: int = 3) -> bytes:
        """
        function blocks until high quality image is available
        """

        for attempt in range(1, retries + 1):
            try:
                return self._wait_for_hq_image()
            except Exception as exc:
                logger.exception(exc)
                logger.error(f"error capture image. {attempt=}/{retries}, retrying")
                continue

        else:
            # we failed finally all the attempts - deal with the consequences.
            self.device_set_status_fault_flag()
            logger.critical(f"finally failed after {retries} attempts to capture image!")
            raise RuntimeError(f"finally failed after {retries} attempts to capture image!")

    def wait_for_lores_image(self, retries: int = 10):
        """Function called externally to receivea low resolution image.
        Also used to stream. Tries to recover up to retries times before giving up.

        Args:
            retries (int, optional): How often retry to use the private _wait_for_lores_image function before failing. Defaults to 10.

        Raises:
            exc: Shutdown is handled different, no retry
            exc: All other exceptions will lead to retry before finally fail.

        Returns:
            _type_: _description_
        """

        for _ in range(1, retries):
            try:
                return self._wait_for_lores_image()  # blocks 0.5s usually. 10 retries default wait time=5s
            except TimeoutError:
                # if timeout occured it will retry several attempts more before finally fail (else of for below)
                # logger.debug(f"device timed out deliver lores image ({attempt}/{retries}).")  # removed to avoid too many log entries.
                if self._connect_thread.stopped():
                    raise StopIteration("backend is shutting down") from None  # allows calling function to stop requesting images if app shuts down
                else:
                    continue
            except Exception as exc:
                # other exceptions fail immediately
                logger.warning("device raised exception (maybe lost connection to device?)")
                raise RuntimeError("device raised exception (maybe lost connection to device?)") from exc

        logger.debug(f"device timed out deliver lores image in {retries-1} attempts. One last try now or raise exception.")

        # final call
        try:
            return self._wait_for_lores_image()  # blocks 0.5s usually. 10 retries default wait time=5s
        except Exception as exc:
            # we failed finally all the attempts - deal with the consequences.
            logger.exception(exc)
            logger.critical(f"finally failed after {retries} attempts to capture lores image!")

            if self._failing_wait_for_lores_image_is_error:
                logger.error("failing to get lores images from device is considered as error, set fault flag to recover.")
                self.device_set_status_fault_flag()

            raise RuntimeError("device raised exception") from exc

    def start_recording(self, video_framerate: int):
        if not self._video_feature_available:
            raise RuntimeError("video feature is not available. check logs for more information. maybe ffmpeg missing?")

        self._video_worker_capture_started.clear()
        self._video_framerate = video_framerate
        self._video_worker_thread = StoppableThread(name="_videoworker_fun", target=self._videoworker_fun, daemon=True)
        self._video_worker_thread.start()

        tms = time.time()
        # gives 3 seconds to actually capture with ffmpeg, otherwise timeout. if ffmpeg is not in memory it needs time to load from disk
        if not self._video_worker_capture_started.wait(timeout=3):
            logger.warning("ffmpeg could not start within timeout; cpu too slow?")
        logger.debug(f"-- ffmpeg startuptime: {round((time.time() - tms), 2)}s ")

    def is_recording(self):
        return self._video_worker_thread is not None and self._video_worker_capture_started.is_set()

    def stop_recording(self):
        # clear notifier that capture was started
        self._video_worker_capture_started.clear()

        if self._video_worker_thread:
            logger.debug("stop recording")
            self._video_worker_thread.stop()
            self._video_worker_thread.join()
            logger.info("_video_worker_thread stopped and joined")

        else:
            logger.info("no _video_worker_thread active that could be stopped")

    def get_recorded_video(self) -> Path:
        # basic idea from https://stackoverflow.com/a/42602576
        if self._video_recorded_videofilepath is not None:
            return self._video_recorded_videofilepath
        else:
            raise FileNotFoundError(f"'{self._video_recorded_videofilepath}' video not found! pls check logs")

    def _videoworker_fun(self):
        logger.info("_videoworker_fun start")
        # init worker, set output to None which indicates there is no current video available to get
        self._video_recorded_videofilepath = None

        # generate temp filename to record to
        mp4_output_filepath = Path("tmp", f"{self.__class__.__name__}_{uuid.uuid4().hex}").with_suffix(".mp4")

        command_general_options = [
            "-hide_banner",
            "-loglevel",
            "info",
            "-y",
        ]
        command_video_input = [
            "-use_wallclock_as_timestamps",
            "1",
            "-thread_queue_size",
            "64",
            "-f",
            "image2pipe",
            "-vcodec",
            "mjpeg",
            "-i",
            "-",
        ]
        command_video_output = [
            "-vcodec",
            "libx264",  # warning! image height must be divisible by 2! #there are also hw encoder avail: https://stackoverflow.com/questions/50693934/different-h264-encoders-in-ffmpeg
            "-preset",
            "veryfast",
            "-b:v",
            f"{appconfig.mediaprocessing.video_bitrate}k",
            "-movflags",
            "+faststart",
            "-r",
            f"{self._video_framerate}",
        ]
        command_video_output_compat_mode = []
        if appconfig.mediaprocessing.video_compatibility_mode:
            # fixes #233. needs more cpu and seems deprecated, maybe in future it will be configurable to disable
            command_video_output_compat_mode = [
                "-pix_fmt",
                "yuv420p",
            ]

        ffmpeg_command = (
            ["ffmpeg"]
            + command_general_options
            + command_video_input
            + command_video_output
            + command_video_output_compat_mode
            + [str(mp4_output_filepath)]
        )

        ffmpeg_subprocess = subprocess.Popen(
            ffmpeg_command,
            stdin=subprocess.PIPE,
            # following report is workaround to avoid deadlock by pushing too much output in stdout/err
            # https://thraxil.org/users/anders/posts/2008/03/13/Subprocess-Hanging-PIPE-is-your-enemy/
            env=dict(os.environ, FFREPORT="file=./log/ffmpeg-last.log:level=32"),
            # stdout=subprocess.PIPE,
            # stderr=subprocess.STDOUT,
        )

        logger.info("writing to ffmpeg stdin")
        tms = time.time()

        # inform calling function, that ffmpeg received first image now
        self._video_worker_capture_started.set()

        while not self._video_worker_thread.stopped():
            try:
                # retry with a low number because video would be messed anyways if needs to retry
                ffmpeg_subprocess.stdin.write(self.wait_for_lores_image(retries=4))
                ffmpeg_subprocess.stdin.flush()  # forces every frame to get timestamped individually
            except Exception as exc:  # presumably a BrokenPipeError? should we check explicitly?
                ffmpeg_subprocess = None
                logger.exception(exc)
                logger.error(f"Failed to create video! Error: {exc}")

                self._video_worker_thread.stop()
                break

        if ffmpeg_subprocess is not None:
            logger.info("writing to ffmpeg stdin finished")
            logger.debug(f"-- process time: {round((time.time() - tms), 2)}s ")

            # release final video processing
            tms = time.time()

            _, ffmpeg_stderr = ffmpeg_subprocess.communicate()  # send empty to stdin, indicates close and gets stderr/stdout; shut down tidily
            code = ffmpeg_subprocess.wait()  # Give it a moment to flush out video frames, but after that make sure we terminate it.

            if code != 0:
                logger.error(ffmpeg_stderr)  # can help to track down errors for non-zero exitcodes.

                # more debug info can be received in ffmpeg popen stderr (pytest captures automatically)
                # TODO: check how to get in application at runtime to write to logs or maybe let ffmpeg write separate logfile
                logger.error(f"error creating videofile, ffmpeg exit code ({code}).")

            ffmpeg_subprocess = None

            logger.info("ffmpeg finished")
            logger.debug(f"-- process time: {round((time.time() - tms), 2)}s ")

            self._video_recorded_videofilepath = mp4_output_filepath
            logger.info(f"record written to {self._video_recorded_videofilepath}")

        logger.info("leaving _videoworker_fun")

    #
    # ABSTRACT METHODS TO BE IMPLEMENTED BY CONCRETE BACKEND (cv2, v4l, ...)
    #

    @abstractmethod
    def _device_start(self):
        """
        start the device ()
        """

    @abstractmethod
    def _device_stop(self):
        """
        stop the device ()
        """

    @abstractmethod
    def _device_available(self) -> bool:
        """
        available device ()
        """

    @abstractmethod
    def _wait_for_hq_image(self):
        """
        function blocks until image still is available
        """

    @abstractmethod
    def _wait_for_lores_image(self):
        """
        function blocks until frame is available for preview stream
        """

    @abstractmethod
    def _on_configure_optimized_for_idle(self):
        """called externally via events and used to change to a preview mode if necessary"""

    @abstractmethod
    def _on_configure_optimized_for_hq_preview(self):
        """called externally via events and used to change to a preview mode if necessary"""

    @abstractmethod
    def _on_configure_optimized_for_hq_capture(self):
        """called externally via events and used to change to a capture mode if necessary"""


#
# INTERNAL FUNCTIONS to operate on the shared memory exchanged between processes.
#


@dataclasses.dataclass
class SharedMemoryDataExch:
    """
    bundle data array and it's condition.
    1) save some instance attributes and
    2) bundle as it makes sense
    """

    sharedmemory: shared_memory.SharedMemory = None
    condition: Condition = None
    lock: Lock = None


def decompile_buffer(shm: memoryview) -> bytes:
    """
    decompile buffer holding jpeg buffer for transport between processes
    in shared memory
    constructed as
    INT(4bytes)+JPEG of length the int describes

    Args:
        shm (memoryview): shared memory buffer

    Returns:
        bytes: concat(length of jpeg+jpegbuffer)
    """
    # ATTENTION: shm is a memoryview; sliced variables are also a reference only.
    # means for this app in consequence: here is the place to make a copy
    # of the image for further processing
    # ATTENTION2: this function needs to be called with lock aquired
    length = int.from_bytes(shm.buf[0:4], "big")
    ret: memoryview = shm.buf[4 : length + 4]
    return ret.tobytes()


def compile_buffer(shm: memoryview, jpeg_buffer: bytes) -> bytes:
    """
    compile buffer holding jpeg buffer for transport between processes
    in shared memory
    constructed as
    INT(4bytes)+JPEG of length the int describes

    Args:
        shm (bytes): shared memory buffer
        jpeg_buffer (bytes): jpeg image
    """
    # ATTENTION: shm is a memoryview; sliced variables are also a reference only.
    # means for this app in consequence: here is the place to make a copy
    # of the image for further processing
    # ATTENTION2: this function needs to be called with lock aquired
    length: int = len(jpeg_buffer)
    length_bytes = length.to_bytes(4, "big")
    shm.buf[0:4] = length_bytes
    shm.buf[4 : length + 4] = jpeg_buffer
