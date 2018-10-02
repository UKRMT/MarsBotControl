# TelemServer

This Qt ocnsole application creates a websocket server on port 1234 that responds to subscribe/ubsubscribe messages from the OpenMCT front end.

It is based on a [Qt websocket example](http://doc.qt.io/qt-5/qtwebsockets-echoserver-example.html).

It then starts a timer to periodically respond to the user interface with bogus telemetry data.

In the future it can collect sensor data and publish meaningful information.

At the same time this program can also receive telem information from the teams controlling computer so that information like current joystick input can also be sent back and seen over OpenMCT.

## ToDo
Add support for more than one active websocket connection.
Gracefully handle websocket disconnection

## Building Setup
Run qmake then make

## Requirements
- libqt5websockets5-dev
- libqt5network5-dev
- ...
