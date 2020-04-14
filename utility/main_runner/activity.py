import time

from com.android.monkeyrunner import MonkeyRunner
from com.android.monkeyrunner import MonkeyDevice

device = MonkeyRunner.waitForConnection()

def camera_record(device, MonkeyDevice, MonkeyRunner):
    print("Running camera record activity")
    device.touch(533, 1704, MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(1.0)
    device.touch(334, 612, MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(1.0)
    device.touch(320, 1760, MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(2.0)
    device.touch(310, 1792, MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(6.0)
    device.touch(519, 1780, MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(2.0)
    device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(1.0)

def delete_video(device, MonkeyDevice, MonkeyRunner):
    print("Running delete video activity")
    device.touch(533, 1692, MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(1.0)
    device.touch(104, 600, MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(1.0)
    device.touch(182, 460, MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(1.0)
    device.touch(877, 1824, MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(1.0)
    device.touch(891, 1812, MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(1.0)
    device.touch(901, 1820, MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(1.0)
    device.touch(877, 1024, MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(1.0)
    device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(1.0)

def run_automated_seq():
    camera_record(device, MonkeyDevice, MonkeyRunner)
    time.sleep(2)
    delete_video(device, MonkeyDevice, MonkeyRunner)

if __name__ == "__main__":
    run_automated_seq()