#include <Keyboard.h>

const int threshold0 = 1000;
const int threshold1 = 1000; // base
const int threshold2 = 1500; // hi-hat
int sensorReading0 = 0;
int sensorReading1 = 0;
int sensorReading2 = 0;


void setup() {
  Serial.begin(115200);   
}

void loop() {
  Keyboard.begin();
  sensorReading0 = analogRead(A0); // snare
  sensorReading1 = analogRead(A1); // base
  sensorReading2 = analogRead(A2); // hi-hat
  Serial.println(sensorReading0);
  Serial.println(sensorReading1);
  Serial.println(sensorReading2);

  if (sensorReading0 >= threshold0) {
    Keyboard.write('a');
    //delay(100);
  }
  if (sensorReading1 >= threshold1) {
    Keyboard.write('e');
    //delay(100);
  }
  if (sensorReading2 >= threshold2) {
    Keyboard.write('c');
    //delay(100);
  }
  if ((sensorReading0 >= threshold0) or (sensorReading1 >= threshold1) or (sensorReading2 >= threshold2)) {
    delay(100);
  }
  Keyboard.end();
  }
