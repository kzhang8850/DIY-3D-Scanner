/*
  Lab 2
 */
#include <math.h>
#include <Servo.h>

const int analogInPin = A0;
int delta = 1;
Servo pan;
Servo tilt;
int theta_lower = 40;
int theta_upper = 130;
int phi_lower = 30;
int phi_upper = 110;
int theta;
int phi;
double dist = 0;
int sensorValue = A0;
String input = "";
volatile bool start = false;
volatile bool started = false;
void(* resetFunc)(void) = 0;

void setup() {
  pan.attach(5);
  tilt.attach(6);
  theta = theta_lower;
  phi = phi_lower;
  pan.write(phi);
  tilt.write(theta);
  Serial.begin(9600);
}

void loop() {
  if(start){
    if(theta > theta_upper){
      theta = theta_lower;
      phi = phi + delta;
      tilt.write(theta);
      pan.write(phi);
      delay(250);
    }
    if(phi > phi_upper){
      theta = theta_lower;
      phi = phi_lower;
      pan.write(phi);
      start = false;
    }
    delay(100);
    sensorValue = analogRead(analogInPin);
    dist = 642.17*pow(sensorValue, -1.295);
    tilt.write(theta);
    Serial.println(String(dist) + ", " + theta + ", " + phi);
    theta = theta + delta;
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
