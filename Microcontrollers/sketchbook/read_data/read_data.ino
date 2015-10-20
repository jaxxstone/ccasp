#include <Time.h>
#include <DHT.h>

/* Digital pins for sensors */
// Temperature/Humidity sensor
// https://github.com/adafruit/DHT-sensor-library/
#define DHTPIN 2 // digital pin 2
#define DHTTYPE DHT11 // model DHT11
DHT dht(DHTPIN, DHTTYPE); // initialize

/* Analog pins for sensors */
const int tempPin = A0;
const int humidityPin = A1;
const int moisturePin = A2;
/* Update frequency to transmit data (in seconds) */
const int updateFrequency = 5;
/* Store last time that data was transmitted */
time_t lastTime = now();

void setup()
{
  Serial.begin(9600);
  dht.begin();
}
  
void loop()
{
  // Check if signal has been sent to the Arduino
  // Serial.available() > 0 means there's bytes to read
  if (Serial.available() > 0)
    {
      // command will hold the command requested by the server
      int command = Serial.parseInt();
      // Check that it's valid
      if (command > 0)
	{
          // command 6 requests data to be transmitted to gateway
	  if (command == 6)
	    {
	      add_data();
              delay(2);
	    }
	}
    }
}

/* Function to read analog inputs and write values to gateway */
void add_data()
{
  // Make sure time delta is >= update frequency
  if ((now() - lastTime) >= updateFrequency)
    {
      /* Temperature pin */
      write_temperature();
      delay(5);
      /* Humidity pin */
      write_humidity();
      delay(5);
      /* Moisture pin */
      write_moisture();
      delay(5);
    } 
}

/* Function to read analog input from moisture pin and write to gateway 
 * Function converts analog value to useable value
 */
void write_moisture()
{
  delay(2);
  int sensorVal = analogRead(moisturePin);
  delay(2);
  // Convert to percentage
  // 0 is 100%, 1023 is 0%
  sensorVal = map(sensorVal, 0, 1023, 100, 0);
  delay(2);
  // Set last updated time to current time
  lastTime = now();
  // Write sensor ID
  delay(2);
  Serial.println(moisturePin);
  delay(2);
  // Write value
  Serial.println(sensorVal);
  delay(2);
}

/* Function to read analog input from humidity pin and write to gateway 
 * Function converts analog value to useable value
 */
void write_humidity()
{
  delay(2);
  // Read humidity using dht library
  float humidity = dht.readHumidity();
  // Set last updated time to current time
  lastTime = now();
  // Write sensor ID
  delay(2);
  Serial.println(humidityPin);
  delay(2);
  // Write value
  Serial.println(humidity);
  delay(2);
}

/* Function to read analog input from temperature pin and write to gateway 
 * Function converts analog value to useable value
 */
void write_temperature()
{
  delay(2);
  // Read temperature in celsius using dht library
  float temperature = dht.readTemperature();
  // Set last updated time to current time
  lastTime = now();
  // Write sensor ID
  delay(2);
  Serial.println(tempPin);
  delay(2);
  // Write value
  Serial.println(temperature);
  delay(2);
}
  

