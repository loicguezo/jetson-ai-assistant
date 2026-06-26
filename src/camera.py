#!/usr/bin/env python3

import logging
import threading
import time

import cv2


class Camera:
    """"""

    def __init__(self, sensor_id=0, sensor_mode=0):
        self.sensor_id = sensor_id
        self.sensor_mode = sensor_mode

        self.cap = None
        self.frame = None
        self.is_running = False
        self.lock = threading.Lock()
        self.thread = None

        logging.debug("Camera initialized (sensor_id=%d)", self.sensor_id)

    def _gstreamer_pipeline(self) -> str:
        return (
            f"nvarguscamerasrc sensor-id={self.sensor_id} sensor-mode={self.sensor_mode} wbmode=1 ! "
            f"video/x-raw(memory:NVMM), format=NV12 ! "
            f"nvvidconv ! "
            f"video/x-raw, format=RGBA ! "
            f"appsink max-buffers=1 drop=true sync=false emit-signals=false"
        )

    def start(self):
        """"""
        if self.is_running:
            return True

        pipeline = self._gstreamer_pipeline()
        self.cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

        if not self.cap.isOpened():
            return False

        self.is_running = True
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()

        logging.debug("Camera capture thread started")

        return True

    def _update_loop(self):
        while self.is_running:
            ret, frame = self.cap.read()

            if not ret:
                logging.warning("Failed to read frame, retrying...")
                time.sleep(0.01)
                continue

            with self.lock:
                self.frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

    def get_frame(self):
        """"""
        with self.lock:
            if self.frame is None:
                return False, None
            return True, self.frame.copy()

    def stop(self):
        """"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        if self.cap:
            self.cap.release()
            logging.debug("Camera stopped")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s] %(message)s",
    )

    cam = Camera()
    cam.start()
    start = time.time()
    logging.info("Waiting for the camera to be ready...")
    while True:
        ok, _ = cam.get_frame()
        if ok:
            break
        if time.time() - start > 5:
            logging.error("Camera timeout")
            exit(1)
        time.sleep(0.05)
    logging.info("Camera ready")
    cam.stop()
