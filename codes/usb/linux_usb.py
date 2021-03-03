#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2021/3/2 16:49
import threading
import pyudev


class LinuxUSBDetector(object):
    """ Monitor udev for detection of usb 
    [Detecting USB Insertion/Removal using Python – Vivek's Blog](https://vivekanandxyz.wordpress.com/2018/01/03/detecting-usb-insertion-removal-using-python/)
    """

    def __init__(self):
        """ Initiate the object """
        thread = threading.Thread(target=self.work)
        thread.daemon = True
        thread.start()

    def work(self):
        """ Runs the actual loop to detect the events """
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='usb')
        # this is module level logger, can be ignored
        print("Starting to monitor for usb")
        self.monitor.start()
        for device in iter(self.monitor.poll, None):
            print("Got USB event: %s", device.action)
            if device.action == 'add':
                # some function to run on insertion of usb
                self.on_created()
            else:
                # some function to run on removal of usb
                self.on_deleted()

    def on_created(self):
        print('is add')

    def on_deleted(self):
        print('is del')


if __name__ == '__main__':
    u = LinuxUSBDetector()
    u.work()
