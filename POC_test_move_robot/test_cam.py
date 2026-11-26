import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

if ret:
    cv2.imwrite('/home/pi/board_test.jpg', frame)
    print("Saved image successfully!")
else:
    print("Failed to read from camera (might be busy by ROS node)")