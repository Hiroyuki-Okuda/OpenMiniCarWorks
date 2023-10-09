### PARAMETERS START ### : edit these parameters

use_raspi = True # true to run on raspberry pi

# color detector parameters
update_rate = 20 # frame update rate
frame_width = 160 # frame width
frame_height = 120 # frame height
show_image = True # true to show image
hsv_range_list = [ # hsv range for each color [(hsv_low), (hsv_high)] h:0-255 s:0-255 v:0-255
    [(0, 0, 80), (255, 15, 255)], # white
    [(0, 120, 120), (25, 255, 255)], # red
    [(25, 130, 150), (55, 255, 255)], # yellow
    [(60, 70, 110), (90, 255, 255)], # green
    [(120, 100, 70), (190, 255, 255)], # blue
]

# speed observer parameters
n_teeth = 36 # number of teeth on encoder
wheel_diameter = 0.06 # wheel diameter in meters

# gpio parameters
STEER_PIN = 17
THROTTLE_PIN = 18
ENCODER_A_PIN = 22
ENCODER_B_PIN = 27
NEUTERAL_INPUT = 1500

### PARAMETERS END ###

import multiprocessing
from color_detector import ColorDetector
if use_raspi:
    from speed_observer import SpeedObserver
import pigpio
import cv2
import numpy as np
import time
from typing import List

# create pigpio instance
if use_raspi:
    raspi = pigpio.pi()


def custom_control_function(
        centroid_list: List[tuple],
        area_list: List[float],
        speed: float
    ):
    ### CONTROL START ### : place your code here to control the car

    white_centroid = centroid_list[0]
    white_area = area_list[0]

    red_centroid = centroid_list[1]
    red_area = area_list[1]

    yellow_centroid = centroid_list[2]
    yellow_area = area_list[2]

    green_centroid = centroid_list[3]
    green_area = area_list[3]

    blue_centroid = centroid_list[4]
    blue_area = area_list[4]

    # calculate steering and throttle
    steer = 0
    throttle = 0
    if green_centroid is not None:
        center_error = (green_centroid[0] - frame_width/2) / (frame_width/2) 
        steer = -600 * center_error
        throttle = 30 * (1-0.3*abs(center_error))

    # set steering and throttle
    if use_raspi:
        raspi.set_servo_pulsewidth(STEER_PIN, NEUTERAL_INPUT + steer)
        raspi.set_servo_pulsewidth(THROTTLE_PIN, NEUTERAL_INPUT - throttle)

    ### CONTROL END ###


def run(
        q_stats_list: List[multiprocessing.Queue],
        q_speed: multiprocessing.Queue,
        show_image: bool
    ):
    ### SETUP START ### : place your code here to run once

    # initialize variables
    color_stats_list = [None for i in range(len(hsv_range_list))]
    speed = None
    frame = None

    # set steering and throttle to neuteral
    neuteral()

    # check if all color detectors are ready
    for i, q_stats in enumerate(q_stats_list):
        while True:
            try:
                color_stats_list[i] = q_stats.get(timeout=1.0)
                break
            except multiprocessing.queues.Empty:
                print ("waiting for color detection")
                continue
    frame = color_stats_list[0][0]

    # check if speed observer is ready
    if use_raspi:
        while True:
            try:
                speed = q_speed.get(timeout=1.0)
                break
            except multiprocessing.queues.Empty:
                print ("waiting for speed observation")
                continue

    ### SETUP END ###

    ### LOOP START ### : place your code here to run repeatedly

    while True:
        # get color detection results
        frame_updated = False
        for i, q_stats in enumerate(q_stats_list):
            try:
                color_stats_list[i] = q_stats.get(block=False)
                if not frame_updated and show_image:
                    frame = color_stats_list[i][0]
                    frame_updated = True
            except multiprocessing.queues.Empty:
                continue

        # get speed
        try:
            speed = q_speed.get(block=False)
        except multiprocessing.queues.Empty:
            pass

        # get stats of largest component for each color
        centroid_list = []
        area_list = []
        for color_stats in color_stats_list:
            centroid, area = get_largest_component(color_stats, frame)
            centroid_list.append(centroid)
            area_list.append(area)

        if show_image and frame_updated:
            # rotate image
            frame = cv2.rotate(frame, cv2.ROTATE_180)

            # show image
            cv2.imshow('frame', frame)
            cv2.waitKey(1)

        # control car
        custom_control_function(centroid_list, area_list, speed)

    ### LOOP END ###


def get_largest_component(
        color_stats: List,
        frame: np.ndarray
    ):
    '''
    Get largest connected component from color detection results.

    color_stats: color detection results
    frame: frame to draw bounding box and centroid
    '''
    _frame, n_labels, labels, stats, centroids, bgr_disp = color_stats

    # initialize variables
    centroid = None
    area = None

    # if connected components exist (excluding background)
    if n_labels >= 2:
        # get largest connected component
        max_idx = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1

        # get centroid and area of largest component
        left, top, width, height, area = stats[max_idx]
        centroid = centroids[max_idx]

        if show_image:
            # draw bounding box for largest component
            cv2.rectangle(frame, (left, top), (left + width, top + height), bgr_disp, 2)

            # draw red circle for centroid
            cv2.circle(frame, (int(centroid[0]), int(centroid[1])), 5, bgr_disp, -1)

    return centroid, area


def neuteral():
    if use_raspi:
        raspi.set_servo_pulsewidth(STEER_PIN,NEUTERAL_INPUT)
        raspi.set_servo_pulsewidth(THROTTLE_PIN,NEUTERAL_INPUT)


def main():
    # round up parameters to prevent opencv error
    global frame_width, frame_height
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
    q_speed = multiprocessing.Queue(maxsize=10)

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
    if use_raspi:
        processes.append(
            multiprocessing.Process(
                target=SpeedObserver.updateSpeed,
                args=(q_speed, ENCODER_A_PIN, ENCODER_B_PIN, n_teeth, wheel_diameter,)
            )
        )
    processes.append(
        multiprocessing.Process(
            target=run,
            args=(q_stats_list, q_speed, show_image,)
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
        neuteral()
        print("\nclosed all processes")


if __name__ == "__main__":
    main()
