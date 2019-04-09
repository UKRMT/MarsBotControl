# MarsBotControl
Code for communicating with and controlling the robot

## TODO
- class for controlling actuators ```ActuatorControl```
  - one roboclaw connected to two linear actuators, both actuators must be in same position at all times
  - monitors position of actuators through serial interface to teensy3.2
  - always monitoring adc to call stop if limits are reached
  - ```moveDown() ```
  - ```moveUp()```
  - ```stop()```
  - ```setInterface( TeensySerialObject )```
  
- class for interfacing with teensy3.2 to read adc channels ```ADCInterface```
  - 2 channels for dig arm raise/lower actuators
  - 2 channels for dig belt extension actuators
  - singleton b/c only one serial conn to teensy 
  - ```startStream()``` : begin sending adc values at interval
  - ```stopStream()``` : end send adc values at interval
  

- Teensy3.2 arduino firmware to provide information on ADC channels for sensor readings (for now)
  - await a serial message "begin" + newline = "begin\n", then start streaming values separated by tabs or commas every 100ms or so
  - if message "end\n" is recieved, stop sending ADC readings.

- add two instances of ```ActuatorControl``` to ```MessageHub```, add parsing logic for corresponding control input messages received
- add instance of ```ADCInterface``` to ```MessageHub``` and call setInterface on the ```ActuatorControl``` objects

- reorganize repo to reflect all-python design 
