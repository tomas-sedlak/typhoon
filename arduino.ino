/*
"""
Open Source Dobot GUI firmware: initial firmware used for testing
First Author: Mike Ferguson www.mikeahferguson.com 3/26/2016
Additional Authors (Add your name below):
02.01.2023
1. Filip Findorak
2. Tomas Sedlak
3. Mark Takac
Under the leadership: Jan Poradsky
License: MIT
*/

#include <MultiStepper.h>
#include <Servo.h>

#include "AccelStepper.h"

// START ramps 1.4 pins
#define X_STEP_PIN 54
#define X_DIR_PIN 55
#define X_ENABLE_PIN 38
#define X_MIN_PIN 3
#define X_MAX_PIN 2

#define Y_STEP_PIN 60
#define Y_DIR_PIN 61
#define Y_ENABLE_PIN 56
#define Y_MIN_PIN 14
#define Y_MAX_PIN 15

#define Z_STEP_PIN 46
#define Z_DIR_PIN 48
#define Z_ENABLE_PIN 62
#define Z_MIN_PIN 18
#define Z_MAX_PIN 19

// extruder 1
#define E0_STEP_PIN 26
#define E0_DIR_PIN 28
#define E0_ENABLE_PIN 24

// extruder 2
#define E1_STEP_PIN 36
#define E1_DIR_PIN 34
#define E1_ENABLE_PIN 30
/// END ramps 1.4 pins

float joint1Steps = 0;
float joint2Steps = 0;
float joint3Steps = 0;
float powerD8 = 0;
float powerD9 = 0;
float powerD10 = 0;
long positions[3];

AccelStepper Joint1(1, E0_STEP_PIN, E0_DIR_PIN);
AccelStepper Joint2(1, X_STEP_PIN, X_DIR_PIN);
AccelStepper Joint3(1, Y_STEP_PIN, Y_DIR_PIN);

MultiStepper steppers;

Servo servo;
int servoPin = 9;

void setup() {
  // START setup ramps pins
  pinMode(X_STEP_PIN, OUTPUT);
  pinMode(X_DIR_PIN, OUTPUT);
  pinMode(X_ENABLE_PIN, OUTPUT);

  pinMode(Y_STEP_PIN, OUTPUT);
  pinMode(Y_DIR_PIN, OUTPUT);
  pinMode(Y_ENABLE_PIN, OUTPUT);

  pinMode(Z_STEP_PIN, OUTPUT);
  pinMode(Z_DIR_PIN, OUTPUT);
  pinMode(Z_ENABLE_PIN, OUTPUT);

  pinMode(E0_STEP_PIN, OUTPUT);
  pinMode(E0_DIR_PIN, OUTPUT);
  pinMode(E0_ENABLE_PIN, OUTPUT);

  pinMode(E1_STEP_PIN, OUTPUT);
  pinMode(E1_DIR_PIN, OUTPUT);
  pinMode(E1_ENABLE_PIN, OUTPUT);

  digitalWrite(X_ENABLE_PIN, LOW);
  digitalWrite(Y_ENABLE_PIN, LOW);
  digitalWrite(Z_ENABLE_PIN, LOW);
  digitalWrite(E0_ENABLE_PIN, LOW);
  digitalWrite(E1_ENABLE_PIN, LOW);
  // END setup ramps pins

  // Connect to the serial port. The input argument is the baud rate.
  // IMPORTNAT: Any software communicating to the arduino must use the same baud
  // rate!
  Serial.begin(115200);

  Joint1.setMaxSpeed(2500);
  Joint1.setAcceleration(200);

  Joint2.setMaxSpeed(2500);
  Joint2.setAcceleration(200);

  Joint3.setMaxSpeed(2500);
  Joint3.setAcceleration(200);

  steppers.addStepper(Joint1);
  steppers.addStepper(Joint2);
  steppers.addStepper(Joint3);

  servo.attach(servoPin);
}

// any code that needs to run constantly goes here. this function just keeps
// getting called (not sure how fast),
void loop() {
  while (!Serial.available()) {
  }

  String data = Serial.readStringUntil('\n');

  if (data == "coords") {
    String coords = Serial.readStringUntil('\n');

    // Extract all values
    int comma1 = coords.indexOf(",");
    int comma2 = coords.indexOf(",", comma1 + 1);

    joint1Steps = coords.substring(0, comma1).toFloat();
    joint2Steps = coords.substring(comma1 + 1, comma2).toFloat();
    joint3Steps = coords.substring(comma2 + 1).toFloat();

    moveArmToAngles();
  }

  if (data == "powers") {
    String powers = Serial.readStringUntil('\n');

    // Extract all values
    int comma1 = powers.indexOf(",");
    int comma2 = powers.indexOf(",", comma1 + 1);

    powerD8 = powers.substring(0, comma1).toInt();
    powerD9 = powers.substring(comma1 + 1, comma2).toInt();
    powerD10 = powers.substring(comma2 + 1).toInt();

    sendPowers();
  }

  Serial.println("Done");
}

void moveArmToAngles() {
  // Print output
  Serial.print("Joint1 steps");
  Serial.println(joint1Steps);
  Serial.print("Joint2 steps:");
  Serial.println(joint2Steps);
  Serial.print("Joint3 steps:");
  Serial.println(joint3Steps);

  positions[0] = joint1Steps;
  positions[1] = joint2Steps;
  positions[2] = joint3Steps;

  steppers.moveTo(positions);
  steppers.runSpeedToPosition();  // preferable to allow checking for reaching
                                  // limit switches
}

void sendPowers() {
  // Print output
  Serial.print("PowerD8:");
  Serial.println(powerD8);
  Serial.print("PowerD9:");
  Serial.println(powerD9);
  Serial.print("PowerD10:");
  Serial.println(powerD10);

  digitalWrite(8, powerD8);
  servo.write(powerD9);
  analogWrite(10, powerD10);
}