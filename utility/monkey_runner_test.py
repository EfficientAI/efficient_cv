from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
device = MonkeyRunner.waitForConnection()
print("found device")

y = 400
x1 = 100
x2 = 300

start = (x1, y)
end = (x2, y)

duration = 0.2
steps = 2
pause = 0.2

for i in range(1, 250):
    # Every so often inject a touch to spice things up!
    if i % 9 == 0:
        device.touch(x2, y, 'DOWN_AND_UP')
        MonkeyRunner.sleep(pause)
    # Swipe right
    device.drag(start, end, duration, steps)
    MonkeyRunner.sleep(pause)
    # Swipe left
    device.drag(end, start, duration, steps)
    MonkeyRunner.sleep(pause)