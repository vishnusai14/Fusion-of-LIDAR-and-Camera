# Fusion-of-LIDAR-and-Camera

This File Contains Code For Raspberry Pi
Once Cloned, Raspberry Pi has to be configured for Three Things
  1. Servoblaster
  2. TFMini Lidar Sensor
  3. Camera 
 
 # ServoBlaster : https://www.youtube.com/watch?v=NqkvlIHe4Yg
 # TFMini Lidar Sensor : https://github.com/TFmini/TFmini-RaspberryPi
 # Camera : 
          sudo raspi-config 
          Under Interface Option Enalbe Legacy Camera
          To test : raspistill -o output.jpeg
          To send the data to windows : https://www.tomshardware.com/how-to/use-raspberry-pi-as-pc-webcam 
          Note: For input use input_uvc.so 
