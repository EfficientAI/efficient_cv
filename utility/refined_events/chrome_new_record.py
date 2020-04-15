from com.android.monkeyrunner import MonkeyRunner
from com.android.monkeyrunner import MonkeyDevice
print('Connecting to device...')
device = MonkeyRunner.waitForConnection()
print('Connected to device')

# Reproduce action log from here
print('Start to reproduce action log')

device.touch(533, 1696, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(533, 1696, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(543, 1268, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(543, 1268, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(897, 140, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(897, 140, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(74, 144, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(74, 144, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(907, 144, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(907, 144, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(978, 1120, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(978, 1120, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(978, 1120, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(978, 1120, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(978, 1120, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(978, 1120, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(982, 1116, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(982, 1116, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(982, 1116, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(982, 1116, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(982, 1116, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(982, 1116, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(978, 1116, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(978, 1116, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(978, 1116, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(978, 1116, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(978, 1116, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(978, 1116, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(978, 1116, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(978, 1116, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(742, 908, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(742, 908, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(742, 908, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(742, 908, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
print('Executing : device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

print('Finish to reproduce action log')