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

#include "AccelStepper.h"
#include <Servo.h>

/// START STEPPER MOTOR SETTINGS
// The NEMA 17 stepper motors that Dobot uses are 200 steps per revolution.
int stepperMotorStepsPerRevolution = 200;
// I'm using a ramps 1.4 board with all 3 jumpers connected, which gives me a microstepping mode of 1/16.
// In other words, the motor is set up so it takes 16 steps to move 1 of the default steps.
// microstepping jumper guide for the a4988 stepper driver: https://www.pololu.com/product/1182
int baseMicrosteppingMultiplier = 16;
int upperArmMicrosteppingMultiplier = 16;
int lowerArmMicrosteppingMultiplier = 16;
// The NEMA 17 stepper motors Dobot uses are connected to a planetary gearbox, the black cylinders.
// It basically just means that the stepper motor is rotating a smaller gear. That smaller gear is in turn rotating a larger one.
// The gears are set up such that rotating the smaller gear by some number of degrees rotates the larger one by a tenth of that number of degrees (10:1 ratio)
// The bigger gears are actually moving the arm, so the number of steps is increased by a factor of 10 (the gear ratio).
int stepperPlanetaryGearBoxMultiplier = 10;
// This variable will hold the aqctual number of steps per revolution and is calculate by multiplying the three previous variables together.
int baseActualStepsPerRevolution = 0;
int upperArmActualStepsPerRevolution = 0;
int lowerArmActualStepsPerRevolution = 0;
/// END STEPPER MOTOR SETTINGS

/// START STEPPER MOTOR DRIVER PIN SETTINGS
// I'm using a RAMPS 1.4 board with A4988 stepper motor drivers for each stepper motor on the Dobot.
// There is space for 5 stepper motors on the RAMPS 1.4 board, but only 3 stepper motors are needed to control the Dobot arm.
// Therefore, I'm only actually using 3/5 of the stepper drivers, but I include the pin numbers for all the spots here for completeness.
// Make a note of which stepper driver you are using to control which stepper motor on the Dobot arm.

// X stepper driver spot (I connected this to the upper arm stepper motor)
#define X_STEP_PIN 54 // the pin you send a signal to actually step the stepper motor
#define X_DIR_PIN 55  // setting this pin to HIGH or LOW dictates in which direction the stepper motor rotates
// unsure what exactly the rest of these do. I think the max and min pins might be related to endstops? This codes is taken from 3D printer code.
// I'll leave these next 3 lines here for now, but I don't think I will be using them. I would imagine enable either enables or disables the stepper motor.
#define X_ENABLE_PIN 38
#define X_MIN_PIN 3
#define X_MAX_PIN 2

// Y stepper driver spot (I connected this to the lower arm stepper motor)
#define Y_STEP_PIN 60
#define Y_DIR_PIN 61
#define Y_ENABLE_PIN 56
#define Y_MIN_PIN 14
#define Y_MAX_PIN 15

// Z stepper driver spot (has room for two stepper motors, so you can drive simultaneously by the exact same number of steps)
#define Z_STEP_PIN 46
#define Z_DIR_PIN 48
#define Z_ENABLE_PIN 62
#define Z_MIN_PIN 18
#define Z_MAX_PIN 19

// E1 stepper driver, just labeling with E here (I connected this to the base stepper motor)
#define E_STEP_PIN 26
#define E_DIR_PIN 28
#define E_ENABLE_PIN 24

// E2 stepper driver, just labeling with Q here instead
#define Q_STEP_PIN 36
#define Q_DIR_PIN 34
#define Q_ENABLE_PIN 30
/// END STEPPER MOTOR DRIVER PIN SETTINGS

// create dobot specific variables to store the relevant pin numbers in
int baseStepPin = 0;
int baseStepDirPin = 0;
int upperArmStepPin = 0;
int upperArmStepDirPin = 0;
int lowerArmStepPin = 0;
int lowerArmStepDirPin = 0;

// create a variable to keep track of the number of angles fromt the serial. This is probably bad technique and prone to error, more quick and dirty.
int angleCounter = 0;
// create variables to store the current/last angles that the dobot base, upper arm, and lower arm is/was at
// I'm currently doing some calculations on the arduino to convert angles to required steps and direction. I should (and will) definitely move these calculations to the python code.
float lastBaseAngle = 0;
float lastUpperArmAngle = 0;
float lastLowerArmAngle = 0;
float baseAngle = 0;
float upperArmAngle = 0;
float lowerArmAngle = 0;
float powerD8 = 0;
float powerD9 = 0;
float powerD10 = 0;

AccelStepper baseAccelObj(1, E_STEP_PIN, E_DIR_PIN);
AccelStepper upperArmAccelObj(1, X_STEP_PIN, X_DIR_PIN);
AccelStepper lowerArmAccelObj(1, Y_STEP_PIN, Y_DIR_PIN);

Servo servo;
int servoPin = 9;

// the setup function is used to setup code (e.g. variables)
void setup()
{

    // START SETUP STEPPER PINS
    // set their modes to output so we can write values to them (1 or 0  aka HIGH or LOW)
    pinMode(X_STEP_PIN, OUTPUT);
    pinMode(X_DIR_PIN, OUTPUT);
    pinMode(X_ENABLE_PIN, OUTPUT);

    pinMode(Y_STEP_PIN, OUTPUT);
    pinMode(Y_DIR_PIN, OUTPUT);
    pinMode(Y_ENABLE_PIN, OUTPUT);

    pinMode(Z_STEP_PIN, OUTPUT);
    pinMode(Z_DIR_PIN, OUTPUT);
    pinMode(Z_ENABLE_PIN, OUTPUT);

    pinMode(E_STEP_PIN, OUTPUT);
    pinMode(E_DIR_PIN, OUTPUT);
    pinMode(E_ENABLE_PIN, OUTPUT);

    pinMode(Q_STEP_PIN, OUTPUT);
    pinMode(Q_DIR_PIN, OUTPUT);
    pinMode(Q_ENABLE_PIN, OUTPUT);

    // I'm assuming this enables the stepper motors, but not sure
    // again, just copying and pasting from 3D printer software here
    digitalWrite(X_ENABLE_PIN, LOW);
    digitalWrite(Y_ENABLE_PIN, LOW);
    digitalWrite(Z_ENABLE_PIN, LOW);
    digitalWrite(E_ENABLE_PIN, LOW);
    digitalWrite(Q_ENABLE_PIN, LOW);
    // END SETUP STEPPER PINS

    // START DOBOT SPECIFIC STEPPER MOTOR SETUP

    // calculate the actual number of steps it takes for each stepper motor to rotate 360 degrees
    baseActualStepsPerRevolution = stepperMotorStepsPerRevolution * baseMicrosteppingMultiplier * stepperPlanetaryGearBoxMultiplier;
    upperArmActualStepsPerRevolution = stepperMotorStepsPerRevolution * upperArmMicrosteppingMultiplier * stepperPlanetaryGearBoxMultiplier;
    lowerArmActualStepsPerRevolution = stepperMotorStepsPerRevolution * lowerArmMicrosteppingMultiplier * stepperPlanetaryGearBoxMultiplier;

    // initialize dobot specific variables to store the relevant pin numbers in
    // this will depend on how you have wired up your Dobot's stepper motors to the ramps 1.4 board
    int baseStepPin = E_STEP_PIN;
    int baseStepDirPin = E_DIR_PIN;
    int upperArmStepPin = X_STEP_PIN;
    int upperArmStepDirPin = X_DIR_PIN;
    int lowerArmStepPin = Y_STEP_PIN;
    int lowerArmStepDirPin = Y_DIR_PIN;
    // END DOBOT SPECIFIC STEPPER MOTOR SETUP

    // Connect to the serial port. The input argument is the baud rate. IMPORTNAT: Any software communicating to the arduino must use the same baud rate!
    Serial.begin(115200);

    // these settings  need to be optimized, especially when using lower microstepping settings. These worked well with 1/16th, and decent with 1/8 (slipping occured if moving too fast though)
    baseAccelObj.setMaxSpeed(10000);
    baseAccelObj.setSpeed(8000); // 1000
    baseAccelObj.setAcceleration(8000);

    upperArmAccelObj.setMaxSpeed(10000);
    upperArmAccelObj.setSpeed(8000);
    upperArmAccelObj.setAcceleration(8000);

    lowerArmAccelObj.setMaxSpeed(10000);
    lowerArmAccelObj.setSpeed(8000);
    lowerArmAccelObj.setAcceleration(8000);

    servo.attach(servoPin);
}

// any code that needs to run constantly goes here. this function just keeps getting called (not sure how fast),
void loop()
{
    if (Serial.available())
    {
        String data = Serial.readStringUntil('\n');

        // Extract all values (including power signals)
        int comma1 = data.indexOf(',');
        int comma2 = data.indexOf(',', comma1 + 1);
        int comma3 = data.indexOf(',', comma2 + 1);
        int comma4 = data.indexOf(',', comma3 + 1);
        int comma5 = data.indexOf(',', comma4 + 1);

        baseAngle = data.substring(0, comma1).toFloat();
        lowerArmAngle = data.substring(comma1 + 1, comma2).toFloat();
        upperArmAngle = data.substring(comma2 + 1, comma3).toFloat();
        powerD8 = data.substring(comma3 + 1, comma4).toInt();
        powerD9 = data.substring(comma4 + 1, comma5).toInt();
        powerD10 = data.substring(comma5 + 1).toInt();

        moveArmToAngles(baseAngle, upperArmAngle, lowerArmAngle);

        Serial.print("PowerD8:");
        Serial.println(powerD8);
        digitalWrite(8, powerD8);

        Serial.print("PowerD9:");
        Serial.println(powerD9);
        if (powerD9 > 0)
        {
            servo.write(130);
        }
        else
        {
            servo.write(90);
        }

        Serial.print("PowerD10:");
        Serial.println(powerD10);
        analogWrite(10, powerD10);

        Serial.println("Done");
    }
}

void moveArmToAngles(float baseAngle, float upperArmAngle, float lowerArmAngle)
{
    Serial.print("Base Angle");
    Serial.println(baseAngle);
    int baseStepNumber = ((abs(baseAngle) / 360) * baseActualStepsPerRevolution) + 0.5;
    // need this because of the abs value function, which is needed for proper rounding
    if (baseAngle < 1)
    {
        baseStepNumber *= -1;
    }
    Serial.print("Base Step Number:");
    Serial.println(baseStepNumber);
    Serial.print("Upper Arm Angle:");
    Serial.println(upperArmAngle);
    int upperArmStepNumber = ((abs(upperArmAngle) / 360) * upperArmActualStepsPerRevolution) + 0.5;
    // need this because of the abs value function, which is needed for proper rounding
    if (upperArmAngle < 1)
    {
        upperArmStepNumber *= -1;
    }
    Serial.print("Upper Arm Step Number:");
    Serial.println(upperArmStepNumber);
    Serial.print("Lower Arm Angle:");
    Serial.println(lowerArmAngle);
    int lowerArmStepNumber = ((abs(lowerArmAngle) / 360) * lowerArmActualStepsPerRevolution) + 0.5;
    // need this because of the abs value function, which is needed for proper rounding
    if (lowerArmAngle < 1)
    {
        lowerArmStepNumber *= -1;
    }
    Serial.print("Lower Arm Step Number:");
    Serial.println(lowerArmStepNumber);
    // necessary to reverse the direction in which the steppers move, so anngles match my defined angles
    baseStepNumber *= -1;
    upperArmStepNumber *= -1;
    // lowerArmStepNumber *= -1;
    baseAccelObj.moveTo(baseStepNumber);
    upperArmAccelObj.moveTo(upperArmStepNumber);
    lowerArmAccelObj.moveTo(lowerArmStepNumber);
    while ((lowerArmAccelObj.distanceToGo() != 0) || (upperArmAccelObj.distanceToGo() != 0) || (baseAccelObj.distanceToGo() != 0))
    {
        baseAccelObj.run();
        upperArmAccelObj.run();
        lowerArmAccelObj.run();
    }
}

// NOT USING THIS FUNCTION
// OLD code, not using, couldn't get it to work, but I didn't try very hard
// this function steps the base, upper arm, and lower arm stepper motors of the Dobot by the specified number of steps
void step(boolean baseDir, int numBaseSteps,
          boolean upperArmDir, int numUpperArmSteps,
          boolean lowerArmDir, int numLowerArmSteps)
{

    // set the direction to move in
    digitalWrite(baseStepDirPin, baseDir);
    digitalWrite(upperArmStepDirPin, upperArmDir);
    digitalWrite(lowerArmStepDirPin, lowerArmDir);
    delay(50);

    // of the 3 stepper motors determine which one requires the most steps
    int max_steps = max(max(numBaseSteps, numUpperArmSteps), numLowerArmSteps);

    // step the motors at the same time by moving them 1 step at essentially the same time
    // Must alternate between HIGH and LOW signals to step the motors. I don't know the physics of why though. Just look up one of the million tutorials on stepper motors if you're curious why.
    for (int i = 0; i < max_steps; i++)
    {
        if (i < numBaseSteps)
            digitalWrite(baseStepPin, HIGH); // only step the motor if it has more steps remaining to take
        if (i < numUpperArmSteps)
            digitalWrite(upperArmStepPin, HIGH);
        if (i < numLowerArmSteps)
            digitalWrite(lowerArmStepPin, HIGH);
        delayMicroseconds(800);
        if (i < numBaseSteps)
            digitalWrite(baseStepPin, LOW);
        if (i < numUpperArmSteps)
            digitalWrite(upperArmStepPin, LOW);
        if (i < numLowerArmSteps)
            digitalWrite(lowerArmStepPin, LOW);
        delayMicroseconds(800);
    }
}