from com.android.monkeyrunner import MonkeyRunner
from com.android.monkeyrunner import MonkeyDevice
print('Connecting to device...')
device = MonkeyRunner.waitForConnection()
print('Connected to device')

# Reproduce action log from here
print('Start to reproduce action log')

device.touch(536, 1704, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(536, 1704, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(536, 1268, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(536, 1268, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(904, 140, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(904, 140, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(74, 128, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(74, 128, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(901, 132, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(901, 132, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(982, 1112, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(982, 1112, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(500, 1000, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(982, 1112, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
print('Executing : device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

print('Finish to reproduce action log')