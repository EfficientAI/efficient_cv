from com.android.monkeyrunner import MonkeyRunner
from com.android.monkeyrunner import MonkeyDevice
print('Connecting to device...')
device = MonkeyRunner.waitForConnection()
print('Connected to device')

# Reproduce action log from here
print('Start to reproduce action log')

device.touch(553, 1728, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(553, 1728, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(941, 620, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(941, 620, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(141, 1604, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(141, 1604, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(0.2)

device.touch(394, 1600, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(394, 1600, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(0.2)

device.touch(644, 1616, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(644, 1616, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(0.2)

device.touch(158, 1412, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(158, 1412, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(0.2)

device.touch(428, 1440, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(428, 1440, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(0.2)

device.touch(634, 1376, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(634, 1376, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(0.2)

device.touch(951, 1164, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(951, 1164, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(0.2)

device.touch(141, 1172, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(141, 1172, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(0.2)

device.touch(408, 1204, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(408, 1204, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(0.2)

device.touch(651, 1176, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(651, 1176, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(0.2)

device.touch(155, 1444, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(155, 1444, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(0.2)

device.touch(388, 1432, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(388, 1432, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(0.2)

device.touch(644, 1368, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(644, 1368, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(0.2)

device.touch(951, 1780, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(951, 1780, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(0.2)

device.touch(172, 964, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(172, 964, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
print('Executing : device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

print('Finish to reproduce action log')