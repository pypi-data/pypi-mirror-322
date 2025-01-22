"""
_summary_
"""

import functools
import json
import platform
import socket
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from threading import Timer
from typing import Any, ClassVar

import psutil
from psutil._common import sbattery

from ..__version__ import __version__
from ..utils.repeatedtimer import RepeatedTimer
from .aquisitionservice import AquisitionService
from .baseservice import BaseService
from .sseservice import SseEventIntervalInformationRecord, SseEventOnetimeInformationRecord, SseService

STATS_INTERVAL_TIMER = 2  # every x seconds


# https://stackoverflow.com/a/78227581
# https://gist.github.com/walkermatt/2871026
def debounce(timeout: float):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.func.cancel()
            wrapper.func = Timer(timeout, func, args, kwargs)
            wrapper.func.start()

        wrapper.func = Timer(timeout, lambda: None)
        return wrapper

    return decorator


@dataclass
class StatsCounter:
    images: int = 0
    collages: int = 0
    animations: int = 0
    videos: int = 0
    shares: int = 0
    limits: dict[str, int] = field(default_factory=dict)
    last_reset: str = None

    stats_file: ClassVar = "stats.json"

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            images=data.get("images", 0),
            collages=data.get("collages", 0),
            animations=data.get("animations", 0),
            videos=data.get("videos", 0),
            shares=data.get("shares", 0),
            limits=data.get("limits", {}),
            last_reset=data.get("last_reset", None),
        )

    @classmethod
    def from_json(cls):
        try:
            with open(cls.stats_file, encoding="utf-8") as openfile:
                return StatsCounter.from_dict(json.load(openfile))
        except FileNotFoundError:
            cls = StatsCounter()
            cls.persist_stats()
            return cls
        except Exception as exc:
            raise RuntimeError(f"unknown error loading stats, error: {exc}") from exc

    def reset(self, field=None):
        try:
            if not field:
                # reset all
                self.__init__(last_reset=datetime.now().astimezone().strftime("%x %X"))  # ("%Y-%m-%d %H:%M:%S"))
            else:
                # reset specific field only
                setattr(self, field, getattr(StatsCounter(), field))

            self.persist_stats()
        except Exception as exc:
            raise RuntimeError(f"failed to reset statscounter, error: {exc}") from exc

    def increment(self, field):
        try:
            current_value = getattr(self, field)
            setattr(self, field, current_value + 1)
        except Exception as exc:
            raise RuntimeError(f"cannot increment {field}, error: {exc}") from exc
        else:
            self.persist_stats()

    def increment_limits(self, field: str):
        try:
            if field in self.limits:
                self.limits[field] += 1
            else:
                self.limits[field] = 1
        except Exception as exc:
            raise RuntimeError(f"cannot increment {field}, error: {exc}") from exc
        else:
            self.persist_stats()

    @debounce(timeout=1)
    def persist_stats(self) -> None:
        try:
            with open(self.stats_file, "w", encoding="utf-8") as outfile:
                json.dump(asdict(self), outfile, indent=2)
        except Exception as exc:
            raise RuntimeError(f"could not save statscounter file, error: {exc}") from exc


class InformationService(BaseService):
    """_summary_"""

    def __init__(self, sse_service: SseService, aquisition_service: AquisitionService):
        super().__init__(sse_service)

        self._aquisition_service = aquisition_service

        # objects
        self._stats_interval_timer: RepeatedTimer = RepeatedTimer(STATS_INTERVAL_TIMER, self._on_stats_interval_timer)
        self._stats_counter: StatsCounter = StatsCounter.from_json()

        # log some very basic common information
        self._logger.info(f"{platform.system()=}")
        self._logger.info(f"{platform.uname()=}")
        self._logger.info(f"{platform.release()=}")
        self._logger.info(f"{platform.machine()=}")
        self._logger.info(f"{platform.python_version()=}")
        self._logger.info(f"{platform.node()=}")
        self._logger.info(f"{self._gather_model()=}")
        self._logger.info(f"{psutil.cpu_count()=}")
        self._logger.info(f"{psutil.cpu_count(logical=False)=}")
        self._logger.info(f"{psutil.disk_partitions()=}")
        self._logger.info(f"{psutil.disk_usage(str(Path.cwd().absolute()))=}")
        self._logger.info(
            [(name, [addr.address for addr in addrs if addr.family == socket.AF_INET]) for name, addrs in psutil.net_if_addrs().items()]
        )
        self._logger.info(f"{psutil.virtual_memory()=}")
        # run python with -O (optimized) sets debug to false and disables asserts from bytecode
        self._logger.info(f"{__debug__=}")

        self._logger.info("initialized information service")

    def start(self):
        """_summary_"""
        self._stats_interval_timer.start()

    def stop(self):
        """_summary_"""
        self._stats_interval_timer.stop()

    def stats_counter_reset(self, field: str = ""):
        self._stats_counter.reset(field)

    def stats_counter_increment(self, varname):
        self._stats_counter.increment(varname)

    def stats_counter_increment_limits(self, field: str):
        self._stats_counter.increment_limits(field)

    def initial_emit(self):
        """_summary_"""

        # gather one time on connect information to be sent off:
        self._sse_service.dispatch_event(
            SseEventOnetimeInformationRecord(
                version=__version__,
                platform_system=platform.system(),
                platform_release=platform.release(),
                platform_machine=platform.machine(),
                platform_python_version=platform.python_version(),
                platform_node=platform.node(),
                platform_cpu_count=psutil.cpu_count(),
                model=self._gather_model(),
                data_directory=Path.cwd().resolve(),
                python_executable=sys.executable,
                disk=self._gather_disk(),
            ),
        )

        # also send interval data initially once
        self._on_stats_interval_timer()

    def _on_stats_interval_timer(self):
        """_summary_"""

        # gather information to be sent off on timer tick:
        self._sse_service.dispatch_event(
            SseEventIntervalInformationRecord(
                cpu1_5_15=self._gather_cpu1_5_15(),
                memory=self._gather_memory(),
                cma=self._gather_cma(),
                backends=self._gather_backends_stats(),
                stats_counter=asdict(self._stats_counter),
                battery_percent=self._gather_battery(),
                temperatures=self._gather_temperatures(),
            ),
        )

    def _gather_cpu1_5_15(self):
        return [round(x / psutil.cpu_count() * 100, 2) for x in psutil.getloadavg()]

    def _gather_memory(self):
        return psutil.virtual_memory()._asdict()

    def _gather_cma(self):
        try:
            with open("/proc/meminfo", encoding="utf-8") as file:
                meminfo = dict((i.split()[0].rstrip(":"), int(i.split()[1])) for i in file.readlines())

            cma = {
                "CmaTotal": meminfo.get("CmaTotal", None),
                "CmaFree": meminfo.get("CmaFree", None),
            }
        except FileNotFoundError:
            # linux only
            cma = {"CmaTotal": None, "CmaFree": None}

        return cma

    def _gather_backends_stats(self):
        return self._aquisition_service.stats()

    def _gather_disk(self):
        return psutil.disk_usage(str(Path.cwd().absolute()))._asdict()

    def _gather_model(self) -> str:
        model = "unknown"

        if platform.system() == "Linux":
            # try to get raspberry model
            try:
                with open("/proc/device-tree/model") as f:
                    model = f.read()
            except Exception:
                self._logger.info("cannot detect computer model")

        return model

    def _gather_battery(self) -> int:
        battery_percent = None

        # https://psutil.readthedocs.io/en/latest/index.html#psutil.sensors_battery
        # None if not determinable otherwise named tuple.
        # clamp to 0...100%
        battery: sbattery | None = psutil.sensors_battery() if hasattr(psutil, "sensors_battery") else None
        if battery:
            battery_percent = max(min(100, round(battery.percent, None)), 0)

        return battery_percent

    def _gather_temperatures(self) -> dict[str, Any]:
        temperatures = {}

        # https://psutil.readthedocs.io/en/latest/index.html#psutil.sensors_temperatures
        psutil_temperatures = psutil.sensors_temperatures() if hasattr(psutil, "sensors_temperatures") else {}
        for name, entry in psutil_temperatures.items():
            temperatures[name] = round(entry[0].current, 1)  # there could be multiple sensors to one zone, we just use the first.

        return temperatures
