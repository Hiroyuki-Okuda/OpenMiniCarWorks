#!/usr/bin/env python3
'''Animates distances and measurement quality'''
import threading

from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

PORT_NAME = '/dev/ttyUSB0'
DMAX = 4000
IMIN = 0
IMAX = 50

def update_line(num, state, line, fig):
    with state['lock']:
        scan = state['scan']
        error = state['error']
    if error is not None:
        plt.close(fig)
        return line,
    if scan is None:
        return line,
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line,


def read_scans(state, stop_event):
    lidar = None
    try:
        lidar = RPLidar(PORT_NAME)
        for scan in lidar.iter_scans():
            if stop_event.is_set():
                break
            with state['lock']:
                state['scan'] = scan
    except Exception as exc:
        with state['lock']:
            state['error'] = exc
    finally:
        if lidar is not None:
            try:
                lidar.stop()
            finally:
                try:
                    lidar.stop_motor()
                finally:
                    lidar.disconnect()


def run():
    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                           cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(DMAX)
    ax.grid(True)

    state = {'lock': threading.Lock(), 'scan': None, 'error': None}
    stop_event = threading.Event()
    reader = threading.Thread(target=read_scans, args=(state, stop_event))
    ani = animation.FuncAnimation(fig, update_line,
        fargs=(state, line, fig), interval=50, cache_frame_data=False)
    reader.start()
    try:
        plt.show()
    finally:
        stop_event.set()
        reader.join()
    if state['error'] is not None:
        raise state['error']

if __name__ == '__main__':
    run()
