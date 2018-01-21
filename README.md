# serial-vis
A serial-driven visual display script. This is intended to be used for data logging and debugging of complex embedded systems where visual outputs are critical to interpreting sensor output.


## Usage
Create a main python script. This script needs the following parts:
```
serial_device = serial_vis(device_mount_path)
while(1):
    serial_device.update()
```
where device_mount_path is the filepath where the serial device has been mounted (/dev/XXXX in linux).

Settings are passed through to the class by either using an intermediary or using keyword arguments in the constructor method.
```
class my_serial_vis(serial_vis):
    settings = {"first_example_setting": "example_value"}

my_serial_device = my_serial_vis(device_mount_path, second_example_setting="example_value")
```


## Commands
Commands should be written to the serial interface, and are read by the script.

### Control Commands:
- draw: execute current draw buffer
- log: log the following string. A label and value should be provided. A timestamp (epoch time) will be automatically inserted.
```
log:label:datastring
```
- logstart, logend: start a block where data with the same label will be combined into one row. For example,
```
logstart
log:data1:100
log:data2:115
log:data1:106
logend
```
will write
```
<timestamp>,data1,100,106
<timestamp>,data2,115
```
to the output csv.
- echo: output text directly to the python console.
```
echo:%s
```

### Drawing Commands:
- definecolor: define a color in RGB, with each value 0 to 255.
```
definecolor:%s:%d%d%d
```
- setscale: set the draw scale. The output is drawn in pixels.
```
setscale:%f
```
- setoffset: set the x and y offset, in pixels. An offset of (0,0) starts from the bottom left corner, with positive x to the right and positive y upwards.
```
setoffset:%d,%d
```
- drawline: draw a line from one coordinate to the other at the given color.
```
drawline:%f,%f:%f,%f:%s
```
- drawlinep: draw a line from one pixel location to another at the given color.
```
drawlinep:%d,%d:%d,%d:%s
```
- drawcircle: draw a circle at the given center and radius at the given color.
```
drawcircle:%f,%f:%f:%s
```
- drawray: draw a ray at the given color. This is a separate function from drawing lines so that trig functions solely used for cosmetic reasons can be offloaded from the target system. The tuple forms the start coordinate, the third float specifies the angle, in radians, and the fourth float specifies the length.
```
drawray:%f,%f:%f:%f:%s
```
- text: display text on the screen at a given coordinate, size, and color.
```
text:%s:%f,%f:%d:%s
```
- textp: dislay text, except using fixed pixel locations.
```
textp:%s:%d,%d:%d:%s
```


## Default Settings

### Serial:
```
"baudrate": 115200,                     
"timeout": 60,                          # time in seconds before serial detection gives up
"encoding": "ascii"                     # serial communication protocol; "ascii" or "utf-8"
```

### Graphics window:
```
"window_size": (800, 600),              # window size, in pixels
"scale": 1.000,                         # scale between raw units and pixels
"offset": (0, 0),                       # offset of origin from bottom left
"frame_limit": 60,                      # max fps
"line_width": 2,                        # width of drawn lines
"font": "arial",                        # pygame text font
"events": {                             # keys to be registered by the program
    pygame.QUIT: "quit",
    pygame.K_SPACE: "pause",
    pygame.K_PERIOD: "fwd",
    pygame.K_LEFTBRACKET: "fwdplus",
    pygame.K_COMMA: "back",
    pygame.K_RIGHTBRACKET: "backplus"
},
"colors": {                             # initial colors
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "background": (255, 255, 255)
```

### Log file:
```
"log_output_name": "serial_log.csv",    # output file name
"time_format": "epoch"                  # output time format. Currently only supports 'epoch'
```

### Data storage:
```
"max_size_forward": 100,                # number of frames stored after pause point                
"max_size_backward": 100                # number of frames stored before the pause point
```


## API

### User Commands:
First, create a graphics class containing the commands:
```
class user_vector_graphics(default_vector_graphics):
    # this command will be called when the opcode 'exampleusercommand' is passed.
    def exampleusercommand(self, instruction):
        print("Example user command: " + instruction[1] + instruction[2])
```
Then, register the graphics class and command format with the main class:
```
class my_serial_vis(serial_vis):
    user_commands = {"exampleusercommand": "s", "d"}
    graphics_class = user_vector_graphics
```
Argument formats are represented by:
- "s": string
- "d": int
- "f": float
- "l": long (unused)
- "ss", "dd", "ff", "ll": array of the given type

### User keyboard events:
Add the requested events to settings, and add a 'process_user_events' function. events[0] is the list of currently pressed keys, and events[1] is the list of keys pressed during the most recent cycle.
```
class my_serial_vis(serial_vis):

    settings = {
        "events": {pygame.K_a: "pressed_key_a"}
    }

    def process_user_events(self, events):
        if "pressed_key_a" in events[0]:
            print("a is currently pressed")
        if "pressed_key_a" in events[1]:
            print("a has just been pressed")
```

### Classes and methods:

#### serial_vis:
- update(): Full update method.
- process_events(events): Apply keyboard commands.
- process_user_events(events): Empty method. Overwrite this to create user-defined keyboard commands.
- user_commands: Format for user-defined commands
- graphics_class: Graphics methods to be used.
- is_live: Pause or play mode
- display_buffer_id: Current frame being displayed

#### serial_vis.serial_device:
- str get_line(): read a line from the serial output. Returns the line without the newline character.
- close(): close the serial interface cleanly.
- write(line): write the line to serial.

#### serial_vis.csv_log:
- log_data(instruction): log the data encoded in the input instruction
- close_file(): close the output csv cleanly.

#### serial_vis.graphics_window:
- current_buffer_id: most recently rendered frame
- update_screen(frame_buffer): draw the input frame_buffer. Will not draw if the provided frame_buffer is the same as the previously drawn frame buffer.
- check_events(): go through settings["events"] and return any events (keypresses). Returns a tuple containing (keys pressed, keys pressed this cyckle)
- close_window(): close pygame window cleanly

#### serial_vis.buffer_db:
- new_buffer(frame_buffer): register a frame buffer. If the id is -1 (not assigned), it will be automatically created.
- get_buffer(index, relative=): get the frame with id index; if relative=True, index is added to self.view_buffer.
- set_current_view(absolute= or relative=): set the current logical view. If absolute=id is given, this is set absolutely; if relative=id, the logical view is set relative to id + self.view_buffer.
- get_buffer_info(): returns (view_buffer, input_buffer).

#### serial_vis.current_buffer:
- frame_id: ID of the frame stored by the buffer. frame_id = -1 if the id has not yet been assigned.
- instructions: instructions in the frame buffer.

