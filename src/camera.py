#!/usr/bin/env python3

import logging
import threading
import time

import cv2


class Camera:
    def __init__(self, sensor_id=0):
        self.sensor_id = sensor_id

        self.cap = None
        self.frame = None
        self.is_running = False
        self.lock = threading.Lock()
        self.thread = None

    def _gstreamer_pipeline(self):
        return (
            f"nvarguscamerasrc sensor-id={self.sensor_id} sensor-mode=0 wbmode=1 ! "
            "video/x-raw(memory:NVMM), format=NV12 ! "
            "nvvidconv ! "
            "video/x-raw, format=I420 ! "
            "videoconvert ! "
            "video/x-raw, format=BGR ! "
            "appsink drop=true sync=false"
        )

    def start(self):
        if self.is_running:
            return True

        pipeline = self._gstreamer_pipeline()
        self.cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

        if not self.cap.isOpened():
            return False

        self.is_running = True
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()

        return True

    def _update_loop(self):
        while self.is_running:
            ret, frame = self.cap.read()

            if not ret:
                time.sleep(0.01)
                continue

            with self.lock:
                self.frame = frame

            time.sleep(0.001)

    def get_frame(self):
        with self.lock:
            if self.frame is None:
                return False, None
            return True, self.frame.copy()

    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        if self.cap:
            self.cap.release()
