# serial-vis

## Commands:

### Control Commands:
- draw: execute current draw buffer
- log: log the following string. A label and value should be provided. A timestamp will be automatically inserted.
```
log:label:datastring
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
drawline:%f,%f:%f%f:%s
```
- drawlinep: draw a line from one pixel location to another at the given color.
```
drawlinep:%d,%d:%d,%d:%s
```
- drawcircle: draw a circle at the given center and radius at the given color.
```
drawcircle:%f,%f:%f:%s
```
- drawray: draw a ray at the given color. This is a separate function from drawing lines so that trig functions solely used for cosmetic reasons can be offloaded from the target system. The tuple forms the start coordinate, and the third float specifies the angle, in radians.
```
drawray:%f,%f:%f:%s
```
- text: display text on the screen at a given coordinate, size, and color.
```
text:%s:%f,%f:%d:%s
```
- textp: dislay text, except using fixed pixel locations.
```
text:%s:%d,%d:%d:%s
```
- echo: output text directly to the python console.
```
echo:%s
```



