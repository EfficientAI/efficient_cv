from com.android.monkeyrunner import MonkeyRunner
from com.android.monkeyrunner.recorder import MonkeyRecorder
device = MonkeyRunner.waitForConnection()
MonkeyRecorder.start(device)