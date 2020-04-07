import sys

PATH_TO_LOG = sys.argv[1]  # Path to action log file exported by MonkeyRecorder
PATH_TO_SCRIPT = sys.argv[2] # This converter creates monkey script file here
ACTION_INTERVAL_IN_SECONDS = 1.0  # Waiting time between each action

def main():
  with open(PATH_TO_LOG, 'r') as log_file:
    create_monkey_script(log_file, PATH_TO_SCRIPT)
    
def create_monkey_script(log_file, script_name):
  logs = log_file.readlines()
  methods = [log2method(log) for log in logs]
  methods = [method + "print('Executing : {0}')\n".format(method.strip()) for method in methods]
  # Add sleep method for each action
  methods = [method + create_wait_method(ACTION_INTERVAL_IN_SECONDS) + "\n\n"
      for method in methods]

  # Create script file
  with open(script_name, "w") as script:
    add_script_header(script)
    script.write('\n# Reproduce action log from here\n')
    script.write("print('Start to reproduce action log')\n\n")
    script.writelines(methods)
    script.write("print('Finish to reproduce action log')")

def log2method(log):
  act, args = log.split('|')
  args = eval(args)
  method = ACT_MAP[act]
  method += parse_args(act, args) + "\n"
  return method

def parse_args(act, args):
  if act == "TOUCH":
    return '(%s, %s, MonkeyDevice.DOWN_AND_UP)' % (args['x'], args['y'])
  if act == "TYPE":
    return '("%s")' % args['message']
  if act == "DRAG":
    return '(%s, %s, %s, %s)' % (args['start'], args['end'], args['duration'], args['steps'])
  if act == "PRESS":
    return '("KEYCODE_%s", %s)' % (args['name'], KEY_EVENT_TYPE[args['type']])
  if act == "WAIT":
    return '(%s)' % args['seconds']

def create_wait_method(wait_time_in_second):
  return ACT_MAP["WAIT"] + "({0})".format(wait_time_in_second)

def add_script_header(script_file):
  header = [
      "from com.android.monkeyrunner import MonkeyRunner\n",
      "from com.android.monkeyrunner import MonkeyDevice\n",
      "print('Connecting to device...')\n",
      "device = MonkeyRunner.waitForConnection()\n",
      "print('Connected to device')\n"
      ]
  script_file.writelines(header)

ACT_MAP = {
    "TOUCH" : "device.touch",
    "DRAG"  : "device.drag",
    "TYPE"  : "device.type",
    "PRESS" : "device.press",
    "WAIT"  : "MonkeyRunner.sleep"
    }

KEY_EVENT_TYPE = {
    "downAndUp" : "MonkeyDevice.DOWN_AND_UP",
    "down"      : "MonkeyDevice.DOWN",
    "up"        : "MonkeyDevice.UP"
    }

if __name__ == "__main__":
  main()