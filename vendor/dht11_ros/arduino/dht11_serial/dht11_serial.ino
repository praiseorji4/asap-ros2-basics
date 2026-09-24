// dht11_serial.ino - print a DHT11 reading over USB serial every 2 seconds.
//
// Output, one line per reading (9600 baud):
//   T:24.0,H:55.0     temperature in degrees C, relative humidity in percent
//   ERR               the sensor did not answer this time
//
// Library: "DHT sensor library" by Adafruit (Arduino IDE -> Library Manager);
// it also installs "Adafruit Unified Sensor".
//
// Wiring (3-pin module):  + -> 5V,  - -> GND,  out/S -> D2
// Bare 4-pin sensor: pin1 VCC -> 5V, pin2 DATA -> D2 with 10k pull-up to 5V, pin4 -> GND.

#include <DHT.h>

#define DHT_PIN 2
#define DHT_TYPE DHT11

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  delay(2000);  // the DHT11 cannot be read faster than about once a second

  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();  // Celsius

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("ERR");
    return;
  }

  Serial.print("T:");
  Serial.print(temperature, 1);
  Serial.print(",H:");
  Serial.println(humidity, 1);
}
