import multiprocessing
import cv2
import numpy as np
import time
from typing import List, Tuple


class ColorDetector(object):
    @staticmethod
    def updateFrame(
            q_frame_list: List[multiprocessing.Queue],
            update_rate: float = 10,
            frame_width: int = 320,
            frame_height: int = 240,
        ):
        '''
        Add frame to queue from camera.

        q_frame_list: list of queue of frame
        frame_width: frame width (1 for minimum)
        frame_height: frame height (1 for minimum)
        '''
        # capture setup
        capture = cv2.VideoCapture(-1)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

        # clock setup
        update_period = 1.0 / update_rate
        update_time = time.clock_gettime(time.CLOCK_BOOTTIME) + update_period

        while True:
            # read frame
            got_frame, frame = capture.read()

            # skip until update time
            if time.clock_gettime(time.CLOCK_BOOTTIME) < update_time:
                continue

            # skip if frame is not read
            if not got_frame:
                print("failed to grab frame")
                update_time += 1.0
                continue

            for q_frame in q_frame_list:
                # remove queue if full
                if q_frame.full():
                    q_frame.get()

                # add frame to queue
                q_frame.put(frame)

            update_time += update_period


    @staticmethod
    def getBinFrame(
            hsv_range: List[Tuple[int, int, int]],
            q_frame: multiprocessing.Queue,
            q_bin: multiprocessing.Queue,
        ):
        '''
        Add binarized image to queue from frame.

        hsv_range: hsv range for binarization [(hsv_low), (hsv_high)] h:0-255 s:0-255 v:0-255
        q_frame: queue of frame (frame)
        q_bin: queue of binarized image (frame, bin_frame, bgr_disp)
        '''
        # get mean rgb value from hsv range
        hsv_low, hsv_high = hsv_range
        h_mean = (hsv_low[0] + hsv_high[0]) / 2
        hsv_disp = np.array([h_mean, hsv_high[1], hsv_high[2]])
        bgr_disp = cv2.cvtColor(np.uint8([[hsv_disp]]), cv2.COLOR_HSV2BGR_FULL)[0, 0]
        bgr_disp = (int(bgr_disp[0]), int(bgr_disp[1]), int(bgr_disp[2]))

        while True:
            # get frame from queue
            frame = q_frame.get()

            # get hsv values
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)

            # binarize image based on hsv values
            bin_frame = cv2.inRange(hsv_frame, hsv_range[0], hsv_range[1])

            # remove queue if full
            if q_bin.full():
                q_bin.get()

            # add binarized image to queue
            q_bin.put([frame, bin_frame, bgr_disp])


    @staticmethod
    def getConnectedComponents(
            q_bin: multiprocessing.Queue,
            q_stats: multiprocessing.Queue,
        ):
        '''
        Add connected components to queue from binarized image.

        q_bin: queue of binarized image (frame, bin_frame, bgr_disp)
        q_stats: queue of connected components (frame, n_labels, labels, stats, centroids, bgr_disp)
        '''
        while True:
            # get frames from queue
            frame, bin_frame, bgr_disp = q_bin.get()

            # get connected components
            n_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bin_frame)

            # remove queue if full
            if q_stats.full():
                q_stats.get()

            # add connected components to queue
            q_stats.put([frame, n_labels, labels, stats, centroids, bgr_disp])


def run(
        q_stats_list: List[multiprocessing.Queue],
        show_image: bool = True
    ):
    while True:
        frame_updated = False
        for q_stats in q_stats_list:
            # get stats from queue
            _frame, n_labels, labels, stats, centroids, bgr_disp = q_stats.get()

            # get frame
            if not frame_updated:
                frame = _frame
                frame_updated = True

            # if connected components exist (excluding background)
            if n_labels >= 2:
                # get largest connected component
                max_idx = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1

                left, top, width, height, area = stats[max_idx]
                centroid = centroids[max_idx]

                if show_image:
                    # draw red circle for centroid
                    cv2.circle(frame, tuple(np.int32(centroid)), 5, bgr_disp, thickness=-1)

                    # draw green rectangle for bounding box
                    cv2.rectangle(frame, (left, top), (left + width, top + height), bgr_disp, thickness=2)

        if show_image:
            # rotate image
            frame = cv2.rotate(frame, cv2.ROTATE_180)

            # update window
            cv2.waitKey(1)
            cv2.imshow("camera", frame)


def main():
    # parameters
    update_rate = 10 # frame update rate
    frame_width = 160 # frame width (1 for minimum)
    frame_height = 120 # frame height (1 for minimum)
    show_image = True # true to show image
    hsv_range_list = [ # hsv range for each color [(hsv_low), (hsv_high)] h:0-255 s:0-255 v:0-255
        [(0, 120, 120), (25, 255, 255)], # red
        [(25, 130, 150), (55, 255, 255)], # yellow
        [(55, 120, 70), (120, 255, 255)], # green
        [(120, 100, 70), (190, 255, 255)], # blue
    ]

    # round up parameters to prevent opencv error
    frame_width = 32 * round(frame_width / 32)
    frame_height = 16 * round(frame_height / 16)

    # create queues
    q_frame_list = []
    q_bin_list = []
    q_stats_list = []
    for i in range(len(hsv_range_list)):
        q_frame_list.append(multiprocessing.Queue(maxsize=2))
        q_bin_list.append(multiprocessing.Queue(maxsize=2))
        q_stats_list.append(multiprocessing.Queue(maxsize=2))

    # create processes
    processes: List[multiprocessing.Process] = []
    processes.append(
        multiprocessing.Process(
            target=ColorDetector.updateFrame,
            args=(q_frame_list, update_rate, frame_width, frame_height,)
        )
    )
    for hsv_range, q_frame, q_bin, q_stats in zip(hsv_range_list, q_frame_list, q_bin_list, q_stats_list):
        processes.append(
            multiprocessing.Process(
                target=ColorDetector.getBinFrame,
                args=(hsv_range, q_frame, q_bin,)
            )
        )
        processes.append(
            multiprocessing.Process(
                target=ColorDetector.getConnectedComponents,
                args=(q_bin, q_stats,)
            )
        )
    processes.append(
        multiprocessing.Process(
            target=run,
            args=(q_stats_list, show_image,)
        )
    )

    # start processes
    for process in processes:
        process.start()

    # wait for keyboard interrupt
    try:
        while True:
            time.sleep(1e5)
    except KeyboardInterrupt:
        # close processes
        for process in processes:
            process.terminate()
            process.join()
        print("\nclosed all processes")


if __name__ == "__main__":
    main()
