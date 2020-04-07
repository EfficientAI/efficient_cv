"""from com.android.monkeyrunner import MonkeyRunner
from com.android.monkeyrunner import MonkeyDevice
print('Connecting to device...')
device = MonkeyRunner.waitForConnection()
print('Connected to device')

# Reproduce action log from here
print('Start to reproduce action log')"""

def camera_record(device, MonkeyDevice, MonkeyRunner):
    device.touch(533, 1704, MonkeyDevice.DOWN_AND_UP)
    print('Executing : device.touch(533, 1704, MonkeyDevice.DOWN_AND_UP)')
    MonkeyRunner.sleep(1.0)

    device.touch(334, 612, MonkeyDevice.DOWN_AND_UP)
    print('Executing : device.touch(334, 612, MonkeyDevice.DOWN_AND_UP)')
    MonkeyRunner.sleep(1.0)

    device.touch(320, 1760, MonkeyDevice.DOWN_AND_UP)
    print('Executing : device.touch(320, 1760, MonkeyDevice.DOWN_AND_UP)')
    MonkeyRunner.sleep(2.0)

    device.touch(310, 1792, MonkeyDevice.DOWN_AND_UP)
    print('Executing : device.touch(310, 1792, MonkeyDevice.DOWN_AND_UP)')
    MonkeyRunner.sleep(6.0)

    device.touch(519, 1780, MonkeyDevice.DOWN_AND_UP)
    print('Executing : device.touch(519, 1780, MonkeyDevice.DOWN_AND_UP)')
    MonkeyRunner.sleep(2.0)

    device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
    print('Executing : device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)')
    MonkeyRunner.sleep(1.0)