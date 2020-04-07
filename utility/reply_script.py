from com.android.monkeyrunner import MonkeyRunner
from com.android.monkeyrunner import MonkeyDevice
print('Connecting to device...')
device = MonkeyRunner.waitForConnection()
print('Connected to device')

# Reproduce action log from here
print('Start to reproduce action log')

y = 400
x1 = 100
x2 = 300

start = (x1, y)
end = (x2, y)

duration = 0.2
steps = 2
pause = 0.2

#for i in range(1, 11):
    # Every so often inject a touch to spice things up!
#    if i % 9 == 0:
#        device.touch(x2, y, 'DOWN_AND_UP')
#        MonkeyRunner.sleep(pause)
    # Swipe right
    #device.drag(start, end, duration, steps)
    #MonkeyRunner.sleep(pause)
    # Swipe left
    #device.drag(end, start, duration, steps)
    #MonkeyRunner.sleep(pause)

MonkeyRunner.sleep(1.0)
device.touch(543, 1704, 'DOWN_AND_UP')
print('Executing : device.touch(543, 1704, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(327, 660, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(327, 660, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(273, 1756, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(273, 1756, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(553, 1784, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(553, 1784, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
print('Executing : device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(540, 1716, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(540, 1716, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(111, 624, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(111, 624, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(162, 464, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(162, 464, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(897, 1844, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(897, 1844, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(887, 1024, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(887, 1024, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.press("KEYCODE_MENU", MonkeyDevice.DOWN_AND_UP)
print('Executing : device.press("KEYCODE_MENU", MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
print('Executing : device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(118, 1096, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(118, 1096, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.touch(928, 1792, MonkeyDevice.DOWN_AND_UP)
print('Executing : device.touch(928, 1792, MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)
print('Executing : device.press("KEYCODE_HOME", MonkeyDevice.DOWN_AND_UP)')
MonkeyRunner.sleep(1.0)

device.drag((432, 1536), (432, 307), 1.0, 10)
print('Executing : device.drag((432, 1536), (432, 307), 1.0, 10)')
MonkeyRunner.sleep(1.0)

print('Finish to reproduce action log')