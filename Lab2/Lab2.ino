/*
  Lab 2
  Carl Moser and Kevin Zhang
 */
#include <math.h>
#include <Servo.h>

// The upper and lower bounds for pan
#define thetaLower 60
#define thetaUpper 120

// The upper and lower bounds for tilt
#define phiLower 50
#define phiUpper 110

// The change in phi/theta
#define delta 10

// The pins for the sensor and servos
#define analogInPin A0
#define panPin 5
#define tiltPin 6


// Declaring the pan and tilt servos
Servo pan;
Servo tilt;

// Declaring and initializing the angles to their lowest values
int theta = thetaLower; // pan
int phi = phiLower; // tilt

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
  pan.write(theta);
  tilt.write(phi);

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
    if(phi > phiUpper){
      /*
        If the tilt angle is greater than the maximum angle, it resets
        to lower bound and increases the pan angle by delta
      */
      phi = phiLower;
      theta = theta + delta;
      tilt.write(phi);
      pan.write(theta);
      // Delays to allow for the tilt servo to move to the initial position
      delay(250);
    }
    if(theta > thetaUpper){
      /*
        If the pan angle is greater than the maximum angle, the scan
        is over so it resets theta and phi to their lower bounds and
        sets start/started to false
      */
      phi = phiLower;
      theta = thetaLower;
      pan.write(theta);
      start = false;
      started = false;
    }

    // Delays to allow the tilt servo to move to the next position
    delay(100);

    // This is the calibration function
    dist = 64217*pow(analogRead(analogInPin), -1.295);

    // Returns the calculated distance, the tilt angle, and the pan angle
    Serial.println(String(dist) + ", " + phi + ", " + theta);

    // Tilts to the next position and adds the change in angle to phi
    tilt.write(phi);
    phi = phi + delta;
  }
}


void capture2d(){
  /*
    This function captures a 2d scan along the pan axis, with phi
    being halfway between the maximum and minimum. This function is
    outside of the main loop because it is relatively fast compared
    to a 3d scan and does not warrant a need to pause or reset
  */

  // Sets the tilt to the midpoint
  tilt.write(100);

  for(theta = thetaLower; theta < thetaUpper; theta = theta + delta){
    /*
      This for loop increments theta by delta and moves the
      pan servo. At each point, the distance is calculated
      and sent to the computer over serial
    */
    pan.write(theta);
    delay(100);
    dist = 64217*pow(analogRead(analogInPin), -1.295);
    Serial.println(String(dist) + ", " + theta);
  }
  // After the 2d scan, the pan and tilt servos are reset to their lower bounds
  theta = thetaLower;
  tilt.write(phiLower);
  pan.write(theta);
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
