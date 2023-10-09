### PARAMETERS START ### : edit these parameters
use_raspi = True # true to run on raspberry pi

# speed observer parameters
n_teeth = 36 # number of teeth on encoder
wheel_diameter = 0.06 # wheel diameter in meters

# gpio parameters
ENCODER_A_PIN = 22
ENCODER_B_PIN = 27

### PARAMETERS END ###

import multiprocessing

if use_raspi:
    from speed_observer import SpeedObserver
import pigpio
import cv2
import numpy as np
import time
from typing import List


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

def main():

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
