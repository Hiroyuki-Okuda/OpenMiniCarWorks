import cv2

cap = cv2.VideoCapture(0)

print("Opened:", cap.isOpened())

ret, frame = cap.read()
print("Frame captured:", ret)

if ret:
    print("Frame shape:", frame.shape)

cap.release()