## Controller Input

Python code meant to run on the windows machine sending commands to the robot.
This code relies on a library designed to accept controller input for headless setups.
Simply named inputs https://pypi.org/project/inputs/.

## To Do
-Get both joysticks from a controller over UDP and a way to distinguish them.
-Get button inputs over UDP.
-Test bandwidth usage. (potentially throttle the frequency of sent packets depending on change in control input i.e when input is the same a new packet does not need to be sent)
-Qt integration.

### Additional resources

[Really nice gamepad/joystick reading library for Qt](https://github.com/alex-spataru/QJoysticks)
