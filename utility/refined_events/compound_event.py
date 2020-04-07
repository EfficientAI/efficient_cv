from com.android.monkeyrunner import MonkeyRunner
from com.android.monkeyrunner import MonkeyDevice
device = MonkeyRunner.waitForConnection()

from camera_record import camera_record
from delete_video import delete_video

import time

for i in range(5):
    camera_record(device, MonkeyDevice, MonkeyRunner)
    time.sleep(2)
    delete_video(device, MonkeyDevice, MonkeyRunner)