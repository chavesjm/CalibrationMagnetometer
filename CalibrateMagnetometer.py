import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque

import matplotlib.pyplot as plt
import matplotlib.animation as animation


# plot class
class AnalogPlot:
    # constr
    def __init__(self, strPort, maxLen):
        # open serial port
        self.ser = serial.Serial(strPort, 38400)
        self.ax = deque()
        self.ay = deque()
        self.az = deque()
        self.maxLen = maxLen

    # add to buffer
    def addToBuf(self, buf, val):
            buf.append(val)

    # add data
    def add(self, data):
        assert (len(data) == 3)
        self.addToBuf(self.ax, data[0])
        self.addToBuf(self.ay, data[1])
        self.addToBuf(self.az, data[2])

    # update plot
    def update(self, frameNum, a0, a1, a2):
        try:
            line = self.ser.readline()
            data = [float(val) for val in line.split(",")]
            # print data
            if (len(data) == 3):
                self.add(data)
                a0.set_data(self.ax,self.ay)
                a1.set_data(self.ax,self.az)
                a2.set_data(self.ay,self.az)
        except KeyboardInterrupt:
            print('exiting')

        return a0,

        # clean up

    def close(self):
        # close serial
        print "Max X"
        print max(self.ax)
        print "Min X"
        print min(self.ax)
        print "Max Y"
        print max(self.ay)
        print "Min Y"
        print min(self.ay)
        print "Max Z"
        print max(self.az)
        print "Min Z"
        print min(self.az)

        self.ser.flush()
        self.ser.close()

        # main() function


def main():
    # create parser
    parser = argparse.ArgumentParser(description="LDR serial")
    # add expected arguments
    parser.add_argument('--port', dest='port', required=True)

    # parse args
    args = parser.parse_args()

    # strPort = '/dev/tty.usbserial-A7006Yqh'
    strPort = args.port

    print('reading from serial port %s...' % strPort)

    # plot parameters
    analogPlot = AnalogPlot(strPort, 100)

    print('plotting data...')

    # set up animation
    fig = plt.figure()
    ax = plt.axes(xlim=(-2000, 2000), ylim=(-500, 2000))
    a0, = ax.plot([], [], 'x')
    a1, = ax.plot([], [], '*')
    a2, = ax.plot([], [], 'o')
    anim = animation.FuncAnimation(fig, analogPlot.update,
                                   fargs=(a0, a1, a2),
                                   interval=50)

    # show plot
    plt.show()

    # clean up
    analogPlot.close()

    print('exiting.')


# call main
if __name__ == '__main__':
    main()





