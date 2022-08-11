"""Supervisor of the Robot Programming benchmark."""

from controller import Supervisor
import os
import sys

def stop_recording(robot):
  if robot.getFromDef("ANIMATION_RECORDER_SUPERVISOR"):
      for _ in range(50):
          robot.step(timestep)
      robot.animationStopRecording()
      for _ in range(10):
          robot.step(timestep)
      print('The animation is saved')
      robot.simulationQuit(0)

""" try:
    includePath = "../../../include"
    includePath.replace('/', os.sep)
    sys.path.append(includePath)
    from benchmark import benchmarkPerformance
except ImportError:
    print("error")
    sys.stderr.write("Warning: 'benchmark' module not found.\n")
    sys.exit(0) """

robot = Supervisor()

timestep = int(robot.getBasicTimeStep())

thymio = robot.getFromDef("BENCHMARK_ROBOT")
translation = thymio.getField("translation")

tx = 0
running = True
while robot.step(timestep) != -1:
    t = translation.getSFVec3f()
    if running:
        percent = 1 - abs(0.25 + t[0]) / 0.25
        if percent < 0:
            percent = 0
        if t[0] < -0.01 and abs(t[0] - tx) < 0.0001:  # away from starting position and not moving any more
            message = "complete"
            running = False
        else:
            message = "percent"
        message += ":" + str(percent)
        robot.wwiSendText(message)
        tx = t[0]
    else:  # wait for record message
        message = robot.wwiReceiveText()
        while message:
            if message.startswith("success:"):
                print(message[9:])
                stop_recording(robot)
                break
            message = robot.wwiReceiveText()

robot.simulationSetMode(Supervisor.SIMULATION_MODE_PAUSE)
