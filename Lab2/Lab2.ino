/*
  Lab 2
 */
#include <math.h>
#include <Servo.h>

const int analogInPin = A0;
Servo pan;
Servo tilt;
int theta = 0;
int phi = 0;
double dist = 0;
int sensorValue = 0;
String input = "";
volatile bool start = false;
volatile bool started = false;
void(* resetFunc)(void) = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if(start){
    if(theta > 170){
      theta = 0;
      phi++;
    }
    if(phi > 170){
      theta = 0;
      phi = 0;
      start = false;
    }
    delay(15);
    sensorValue = analogRead(analogInPin);
    dist = 642.17*pow(sensorValue, -1.295);
    Serial.println(String(dist) + ", " + theta + ", " + phi);
    delay(10);
    theta++;
  }
}

void serialEvent(){
  input = Serial.readString();
  if(input == "start" && start == false){
    started = true;
    start = true;
  }
  else if (input == "stop"){
    resetFunc();
  }
  else if(input == "pause" && started == true){
    start = !start;
  }
}
