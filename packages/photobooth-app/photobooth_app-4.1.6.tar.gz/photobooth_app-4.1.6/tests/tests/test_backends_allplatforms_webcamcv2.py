"""
Testing VIRTUALCAMERA Backend
"""

import logging

import pytest

from photobooth.services.backends.webcamcv2 import WebcamCv2Backend
from photobooth.services.backends.webcamcv2 import available_camera_indexes as cv2_avail
from photobooth.services.config.groups.backends import GroupBackendOpenCv2

from .utils import get_images

logger = logging.getLogger(name=None)


@pytest.fixture()
def backend_cv2() -> WebcamCv2Backend:
    # setup
    backend = WebcamCv2Backend(GroupBackendOpenCv2())

    logger.info("probing for available cameras")
    _availableCameraIndexes = cv2_avail()
    if not _availableCameraIndexes:
        pytest.skip("no camera found, skipping test")

    cameraIndex = _availableCameraIndexes[0]

    logger.info(f"available camera indexes: {_availableCameraIndexes}")
    logger.info(f"using first camera index to test: {cameraIndex}")

    backend._config.device_index = cameraIndex
    backend._config.CAMERA_TRANSFORM_HFLIP = True
    backend._config.CAMERA_TRANSFORM_VFLIP = True

    # deliver
    backend.start()
    backend.block_until_device_is_running()
    yield backend
    backend.stop()


def test_get_images_webcamcv2(backend_cv2: WebcamCv2Backend):
    """get lores and hires images from backend and assert"""
    get_images(backend_cv2)
