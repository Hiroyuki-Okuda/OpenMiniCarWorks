from picamera2 import Picamera2

picam2 = Picamera2()

#カメラ画像を保存する
picam2.start_and_capture_file("test.jpg")