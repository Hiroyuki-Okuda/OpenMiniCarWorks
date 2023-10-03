import cv2


def main():
    # parameters
    frame_width = 160
    frame_height = 120

    # round up parameters
    frame_width = 32 * round(frame_width / 32)
    frame_height = 16 * round(frame_height / 16)

    # capture setup
    capture = cv2.VideoCapture(-1)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    print(f"frame width: {capture.get(cv2.CAP_PROP_FRAME_WIDTH)}")
    print(f"frame height: {capture.get(cv2.CAP_PROP_FRAME_HEIGHT)}")

    try:
        while True:
            # read frame
            got_frame, frame = capture.read()

            # rotate image
            frame = cv2.rotate(frame, cv2.ROTATE_180)

            # get hsv values
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)

            # draw hsv values
            h_val = hsv_frame[(int)(frame_height/2), (int)(frame_width/2)][0]
            s_val = hsv_frame[(int)(frame_height/2), (int)(frame_width/2)][1]
            v_val = hsv_frame[(int)(frame_height/2), (int)(frame_width/2)][2]
            cv2.drawMarker(frame, ((int)(frame_width/2), (int)(frame_height/2)), (0, 0, 255), cv2.MARKER_TILTED_CROSS, 10)
            cv2.putText(frame, "h:" + "%3.0f"%h_val, ((int)(frame_width/2 + 10), (int)(frame_height/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255))
            cv2.putText(frame, "s:" + "%3.0f"%s_val, ((int)(frame_width/2 + 10), (int)(frame_height/2 -  0)), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255))
            cv2.putText(frame, "v:" + "%3.0f"%v_val, ((int)(frame_width/2 + 10), (int)(frame_height/2 + 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255))

            # update window
            cv2.waitKey(1)
            cv2.imshow("camera", frame)


    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
