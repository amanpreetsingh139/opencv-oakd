from pathlib import Path
import cv2
import depthai
import numpy as np

# define the pipeline
pipeline = depthai.Pipeline()

# Define the source - color camera

cam_rgb = pipeline.createColorCamera()
cam_rgb.setBoardSocket(depthai.CameraBoardSocket.RGB)
cam_rgb.setFps(50)
cam_rgb.setResolution(depthai.ColorCameraProperties.SensorResolution.THE_1080_P)
cam_rgb.setInterleaved(False)
print(cam_rgb.getFps(), cam_rgb.getResolution())
# cam_rgb.setCamId(0)

# create output
xout_rgb = pipeline.createXLinkOut()
xout_rgb.setStreamName("rgb")
xout_rgb.input.setQueueSize(1)
cam_rgb.preview.link(xout_rgb.input)
# Linking
cam_rgb.video.link(xout_rgb.input)
# Pipeline defined, now the device is assigned and pipeline is started
# device = dai.Device(pipeline)
# device.startPipeline()

with depthai.Device(pipeline) as device:
    # Output queue will be used to get the rgb frames from the output defined above
    q_rgb = device.getOutputQueue(name="rgb", maxSize=1, blocking=False)
    # print(device.getFirstAvailableDevice())
    # q_rgb = device.getOutputQueue("rgb")

    frame = None
    while True:
        in_rgb = q_rgb.tryGet()

        if in_rgb is not None:
            frame = in_rgb.getCvFrame()

        if frame is not None:
            cv2.imshow("preview", frame)

        if cv2.waitKey(1) == ord('q'):
            break
