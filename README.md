# serial-vis
A serial-driven visual display script for data logging and debugging of complex embedded systems where visual outputs are critical to interpreting sensor output.

## Dependencies
- Pygame (<http://www.pygame.org>)
- PySerial (<https://pythonhosted.org/pyserial/>)

## Basic usage
1. Open example.py. Replace the keyword 'path' with the filepath of the device. In the example, an Arduino is connected to the default COM port ("/dev/ttyACM0").
2. Set the keyword 'baudrate' with the appropriate baudrate as defined by the system. On an Arduino, this is the integer argument passed to Serial.begin().
3. Run serial-vis. A pygame window should pop up.
4. Press space to pause the graphical output. Press space again to return to live mode. Use ',' and '.' (the comma and period keys) to advance by one frame and go back by one frame when in paused mode. By default, the system stores 100 frames forward and backwards from the pause point. The '[' and ']' keys can be used to move by 10 frames at a time.
5. The log (anything written by the log instruction) is saved by default to serial_log.csv.

## API
See the [wiki](https://github.com/thetianshuhuang/serial-vis/wiki).
