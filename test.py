import cv2
import depthai as dai

# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.createColorCamera()
xoutVideo = pipeline.createXLinkOut()
xoutVideo.setStreamName("video")
# Properties
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setVideoSize(1920, 1080)
camRgb.setFps(50)

xoutVideo.input.setBlocking(False)
xoutVideo.input.setQueueSize(1)

# Linking
camRgb.video.link(xoutVideo.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:
    frame_width = 1920
    frame_height = 1080

    size = (frame_width, frame_height)
    video = device.getOutputQueue(name="video", maxSize=100, blocking=False)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    result = cv2.VideoWriter('filename.mp4',
                             fourcc,
                             50, size)
    while True:
        videoIn = video.get()
        frame = videoIn.getCvFrame()
        # Get BGR frame from NV12 encoded video frame to show with opencv
        # Visualizing the frame on slower hosts might have overhead
        cv2.imshow("video - frame 1", frame)
        result.write(frame)
        if cv2.waitKey(1) == ord('q'):
            break
# video.release()
result.release()
cv2.destroyAllWindows()
print("The video was successfully saved")