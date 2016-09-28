/*
  Lab 2
  Carl Moser and Kevin Zhang
 */
#include <math.h>
#include <Servo.h>

// The upper and lower bounds for pan
#define phiLower 30
#define phiUpper 140

// The upper and lower bounds for tilt
#define thetaLower 40
#define thetaUpper 130

// The change in theta/phi
#define delta 10

// The pins for the sensor and servos
#define analogInPin A0
#define panPin 5
#define tiltPin 6


// Declaring the pan and tilt servos
Servo pan;
Servo tilt;

// Declaring and initializing the angles to their lowest values
int phi = phiLower; // pan
int theta = thetaLower; // tilt

// The value to hold the calibrated distance
double dist = 0;

// Initializing a string to hold serial input
String input = "";

// Volatile booleans to start the scan and to tell if a 3d scan is in the process
volatile bool start = false;
volatile bool started = false;

// Declaring a reset function to stop a scan
void(* resetFunc)(void) = 0;


void setup() {
  // Attaching the servos to their respective pins
  pan.attach(panPin);
  tilt.attach(tiltPin);

  // Setting the servos to their lowest values
  pan.write(phi);
  tilt.write(theta);

  // Initializing serial communication
  Serial.begin(9600);
}


void loop() {
  /*
    The 3d pan/tilt scanner code was written in the loop
    instead of a nested for loop because serial events are
    not registerd within the loop

    This allows for the scanning to be reset or paused
  */
  if(start){
    // If start is true, it the scanning begins
    if(theta > thetaUpper){
      /*
        If the tilt angle is greater than the maximum angle, it resets
        to lower bound and increases the pan angle by delta
      */
      theta = thetaLower;
      phi = phi + delta;
      tilt.write(theta);
      pan.write(phi);
      // Delays to allow for the tilt servo to move to the initial position
      delay(250);
    }
    if(phi > phiUpper){
      /*
        If the pan angle is greater than the maximum angle, the scan
        is over so it resets phi and theta to their lower bounds and
        sets start/started to false
      */
      theta = thetaLower;
      phi = phiLower;
      pan.write(phi);
      start = false;
      started = false;
    }

    // Delays to allow the tilt servo to move to the next position
    delay(100);

    // This is the calibration function
    dist = 642.17*pow(analogRead(analogInPin), -1.295);

    // Returns the calculated distance, the tilt angle, and the pan angle
    Serial.println(String(dist) + ", " + theta + ", " + phi);

    // Tilts to the next position and adds the change in angle to theta
    tilt.write(theta);
    theta = theta + delta;
  }
}


void capture2d(){
  /*
    This function captures a 2d scan along the pan axis, with theta
    being halfway between the maximum and minimum. This function is
    outside of the main loop because it is relatively fast compared
    to a 3d scan and does not warrant a need to pause or reset
  */

  // Sets the tilt to the midpoint between the upper and lower bounds
  tilt.write((thetaUpper + thetaLower)/2);

  for(phi = phiLower; phi < phiUpper; phi = phi + delta){
    /*
      This for loop increments phi by delta and moves the
      pan servo. At each point, the distance is calculated
      and sent to the computer over serial
    */
    pan.write(phi);
    delay(100);
    dist = 642.17*pow(analogRead(analogInPin), -1.295);
    Serial.println(String(dist) + ", " + phi);
  }
  // After the 2d scan, the pan and tilt servos are reset to their lower bounds
  phi = phiLower;
  tilt.write(thetaLower);
  pan.write(phi);
}


void serialEvent(){
  /*
    This function queues up serial events while the loop is running
    and before the loop resets, it runs through the queue. It reads
    the input as a string and runs through some if statements
  */
  input = Serial.readString();
  if(input == "start" && !start){
    /*
      If the input is start and the scan has not started,
      it sets start and started to true
    */
    started = true;
    start = true;
  }
  else if (input == "stop"){
    // If the input is stop, the arduino resets
    resetFunc();
  }
  else if(input == "pause" && started){
    // If the input is pause and it has started scanning, it pauses
    start = !start;
  }
  else if(input == "twodimensions" && !started){
    /*
      If the input is for a 2d scan and a 3d scan is not in process,
      it will start a 2d scan
    */
    capture2d();
  }
}
