from com.android.monkeyrunner import MonkeyRunner
from com.android.monkeyrunner import MonkeyDevice
print('Connecting to device...')
device = MonkeyRunner.waitForConnection()
print('Connected to device')

# Reproduce action log from here
print('Start to reproduce action log')

device.touch(533, 1708, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(533, 1708, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(735, 304, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(735, 304, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(796, 1852, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(796, 1852, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(779, 1848, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(779, 1848, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(799, 1852, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(799, 1852, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(928, 1008, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(928, 1008, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(907, 600, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(907, 600, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
print('Executing : device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

print('Finish to reproduce action log')