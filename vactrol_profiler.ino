//initialize pins
const int voltRead = A0;  // Analog input pin that senses Vout--used for ohm conversion


//initialize ohmmeter
int voltValue = 0;
float Vin = 5;  // Input voltage
float Vout = 0;
float buff = 0;
float buff2 = 0;
float Rref = 2200;  // Reference resistor's value in ohms
float R = 0;
float R1 = 0;
float R2 = 0;
float R3 = 0;

//pwm stuff
int x = 0;
const int pwmPin = 2;

void setup() {

  pinMode(voltRead, INPUT);
  pinMode(pwmPin, OUTPUT);

  Serial.begin(9600);  //breakfast serial

  analogWrite(pwmPin, 1);
  delay(2000);
}

void loop() {

  for (x = 1; x < 256; x++) {

    analogWrite(pwmPin, x);
    delay(250);

    voltValue = analogRead(voltRead);
    buff = (Vin * voltValue);
    Vout = (buff) / 1024.0;

    R1 = (Rref * Vout) / (Vin - Vout);
    voltValue = analogRead(voltRead);
    buff = (Vin * voltValue);
    Vout = (buff) / 1024.0;

    Serial.print(x);

    R2 = (Rref * Vout) / (Vin - Vout);
    voltValue = analogRead(voltRead);  //
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