void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200)

}

void loop() {
  // put your main code here, to run repeatedly:



}

# function definitions and behavior in
# github.com/thetianshuhuang/serial-vis/README.md

# control commands
void draw() {
  Serial.println("draw");
}

void log(label, datastring) {
  Serial.println("log:" + label + ":" + datastring);
}

void logstart() {
  Serial.println("logstart");
}

void logend() {
  Serial.println("logend");
}

void echo(char* string) {
  Serial.println("echo:" + string);
}

# drawing commands
void definecolor(str string, int* color) {
  Serial.println(
    "definecolor:"
    + string + ":" +
    color[0] + "," + color[1] + "," + color[2])
}

void setscale(float scale) {
  Serial.println("setscale:" + scale)
}

void setoffset(float x_offset, float y_offset) {
  Serial.println("setoffset:" + x_offset + "," + y_offset);
}

void drawline(float x_1, float y_1, float x_2, float y_2, char* color) {
  Serial.println(
    "drawline:" +
    x_1 + "," + y_1 + ":" +
    x_2 + "," + y_2 + ":" +
    color);
}

void drawlinep(int x_1, int y_1, int x_2, int y_2, char* color) {
  Serial.println(
    "drawlinep:" +
    x_1 + "," + y_1 + ":" +
    x_2 + "," + y_2 + ":" +
    color);
}

void drawcircle(float x, float y, float r, char* color) {
  Serial.println(
    "drawcircle:" +
    x + "," + y + ":" +
    r + ":" +
    color);
}

void drawray(float x, float y, float heading, float length, char* color) {
  Serial.println(
    "drawray:" +
    x + "," + y + ":" +
    heading + ":" +
    length + ":" +
    color);
}

void text(char* label, float x, float y, int size, char* color) {
  Serial.println(
    "text:" +
    label + ":" +
    x + "," + y + ":" +
    size + ":" +
    color);
}

void textp(char* label, int x, int y, int size, char* color) {
  Serial.println(
    "textp:" +
    label + ":" +
    x + "," y ":"
    size + ":" +
    color);
}
