"""from com.android.monkeyrunner import MonkeyRunner
from com.android.monkeyrunner import MonkeyDevice
print('Connecting to device...')
device = MonkeyRunner.waitForConnection()
print('Connected to device')

# Reproduce action log from here
print('Start to reproduce action log')"""

def delete_video(device, MonkeyDevice, MonkeyRunner):
    device.touch(533, 1692, MonkeyDevice.DOWN_AND_UP)
    print('Executing : device.touch(533, 1692, MonkeyDevice.DOWN_AND_UP)')
    MonkeyRunner.sleep(1.0)

    device.touch(104, 600, MonkeyDevice.DOWN_AND_UP)
    print('Executing : device.touch(104, 600, MonkeyDevice.DOWN_AND_UP)')
    MonkeyRunner.sleep(1.0)

    device.touch(182, 460, MonkeyDevice.DOWN_AND_UP)
    print('Executing : device.touch(182, 460, MonkeyDevice.DOWN_AND_UP)')
    MonkeyRunner.sleep(1.0)

    device.touch(877, 1824, MonkeyDevice.DOWN_AND_UP)
    print('Executing : device.touch(877, 1824, MonkeyDevice.DOWN_AND_UP)')
    MonkeyRunner.sleep(1.0)

    device.touch(891, 1812, MonkeyDevice.DOWN_AND_UP)
    print('Executing : device.touch(891, 1812, MonkeyDevice.DOWN_AND_UP)')
    MonkeyRunner.sleep(1.0)

    device.touch(901, 1820, MonkeyDevice.DOWN_AND_UP)
    print('Executing : device.touch(901, 1820, MonkeyDevice.DOWN_AND_UP)')
    MonkeyRunner.sleep(1.0)

    device.touch(877, 1024, MonkeyDevice.DOWN_AND_UP)
    print('Executing : device.touch(877, 1024, MonkeyDevice.DOWN_AND_UP)')
    MonkeyRunner.sleep(1.0)

    device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
    print('Executing : device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)')
    MonkeyRunner.sleep(1.0)