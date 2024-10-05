#include <Arduino.h>
#include <SPI.h>
#include "MCP4261.h"

#define DIGIPOT_CS 22
#define PWM_PIN 7
#define VOLT_READ A0

float Vin = 5; // input voltage
float Vout = 0;
float buff = 0;
float buff2 = 0;
float Rref = 2200; // reference resistor value in ohms
float R = 0;
float R1 = 0;
float R2 = 0;
float R3 = 0;

int voltValue = 0;
int pwmStep = 0;
int digipotStep = 0;

MCP4261 digipot(DIGIPOT_CS, 255, &SPI);

void setup()
{
	pinMode(VOLT_READ, INPUT);
	pinMode(PWM_PIN, OUTPUT);
	pinMode(DIGIPOT_CS, OUTPUT);

	Serial.begin(9600);
	SPI.begin();
	digipot.begin();

	// warmup
	analogWrite(PWM_PIN, 1);
	digipot.setValue(0, 0);

	delay(2000);
}

void loop()
{
	for (pwmStep = 1; pwmStep < 256; pwmStep++)
	{
		for (digipotStep = 0; digipotStep < 256; digipotStep++)
		{
			analogWrite(PWM_PIN, pwmStep);
			digipot.setValue(0, digipotStep);

			delay(250);

			voltValue = analogRead(VOLT_READ);
			buff = (Vin * voltValue);
			Vout = (buff) / 1024.0;

			R1 = (Rref * Vout) / (Vin - Vout);
			voltValue = analogRead(VOLT_READ);
			buff = (Vin * voltValue);
			Vout = (buff) / 1024.0;

			Serial.print(pwmStep);
			Serial.print(",");
			Serial.print(digipotStep);

			R2 = (Rref * Vout) / (Vin - Vout);
			voltValue = analogRead(VOLT_READ); //
			buff = (Vin * voltValue);
			Vout = (buff) / 1024.0;

			R3 = (Rref * Vout) / (Vin - Vout);
			R = (R1 + R2 + R3) / 3;

			Serial.print(",");
			Serial.print((long)R);
			Serial.print(";");
		}
	}

	Serial.println();
	Serial.println("done");
	delay(100000000);
}