from com.android.monkeyrunner import MonkeyRunner
from com.android.monkeyrunner import MonkeyDevice
print('Connecting to device...')
device = MonkeyRunner.waitForConnection()
print('Connected to device')

# Reproduce action log from here
print('Start to reproduce action log')

device.touch(540, 1696, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(540, 1696, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(118, 608, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(118, 608, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(165, 444, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(165, 444, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(914, 1832, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(914, 1832, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(877, 1032, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(877, 1032, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(87, 72, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(87, 72, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
print('Executing : device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

print('Finish to reproduce action log')