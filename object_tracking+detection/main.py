from ultralytics import YOLO
import cv2

#load yolov8 model 
model = YOLO('yolov8n.pt')
#load video
#so either load video or webcam
""""
video_path = 'video.mp4'
cap = cv2.VideoCapture(video_path)
"""
#load webcam
cap = cv2.VideoCapture(0)

ret = True
while ret:
    ret, frame = cap.read()

    #detect object 
    results = model.track(frame, persist=True)

    #plot results
    frame_ = results[0].plot()
    #visualize 
    cv2.imshow('frame', frame_)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

#release video capture
cap.release()
cv2.destroyAllWindows()


