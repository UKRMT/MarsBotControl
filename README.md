# MarsBotControl
Code for communicating with and controlling the robot

## TODO
- add seperate socket controls for each actuator in '''MessageHub ''' - 
  - check to make sure positions are equal between the two actuators - 
  - if not, catch up in the right direction - 
- debug lag on the controller - 
  - find bottleneck, diagnose from there - 
  - if bottleneck is the connection, switch from ws:// to TCP - 
- configure camera operation - 
  - ~1s per photo sent to WS - 
- get comprhensive power level readings - 
  - current draw from all controllers and calculate from constant voltages - 
  - also battery levels? If not possible then we can at least use them for checking accuracy - 
- practice operating the bot - 


