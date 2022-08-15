import cv2

video_capture = cv2.VideoCapture('rtsp://192.168.31.91:8000/h264_ulaw.sdp')

while True:
    try:
        ret, frame = video_capture.read()
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except KeyboardInterrupt:
        break
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
