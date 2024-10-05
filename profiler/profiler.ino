#include <Arduino.h>

const int voltRead = A0;

int voltValue = 0;
float Vin = 5; // input voltage
float Vout = 0;
float buff = 0;
float buff2 = 0;
float Rref = 2200; // reference resistor value in ohms
float R = 0;
float R1 = 0;
float R2 = 0;
float R3 = 0;

int pwmStep = 0;
const int pwmPin = 2;

void setup()
{
	pinMode(voltRead, INPUT);
	pinMode(pwmPin, OUTPUT);

	Serial.begin(9600);

	analogWrite(pwmPin, 1);
	delay(2000);
}

void loop()
{
	for (pwmStep = 1; pwmStep < 256; pwmStep++)
	{
		analogWrite(pwmPin, pwmStep);
		delay(250);

		voltValue = analogRead(voltRead);
		buff = (Vin * voltValue);
		Vout = (buff) / 1024.0;

		R1 = (Rref * Vout) / (Vin - Vout);
		voltValue = analogRead(voltRead);
		buff = (Vin * voltValue);
		Vout = (buff) / 1024.0;

		Serial.print(pwmStep);

		R2 = (Rref * Vout) / (Vin - Vout);
		voltValue = analogRead(voltRead); //
		buff = (Vin * voltValue);
		Vout = (buff) / 1024.0;

		R3 = (Rref * Vout) / (Vin - Vout);
		R = (R1 + R2 + R3) / 3;

		Serial.print(",");
		Serial.print((long)R);
		Serial.print(";");
	}

	Serial.println();
	Serial.println("done");
	delay(100000000);
}