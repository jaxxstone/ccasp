#include <Time.h>
int pins[] = {0, 0, 0, 3, 4};
int pinCount = 5;

const int tempPin = A0;

const int numReadings = 100;

float readings[numReadings];

int counter = 0;
int randomPin = 1;

time_t lastTime = now();
  
void setup()
{
  Serial.begin(9600);
  for (int thisPin = 2; thisPin < pinCount; thisPin++)
    {
      pinMode(pins[thisPin], OUTPUT); 
    }
    
  for (int i = 0; i < 100; i++)
    {
      readings[i] = -1.0;
    }
    
}
  
void loop()
{
  // Check if signal has been sent to the Arduino
  // Serial.available() > 0 means there's bytes to read
  if (Serial.available() > 0)
    {
      // pin will hold the pin requested by the server
      int pin = Serial.parseInt();
      // Check that it's valid
      if (pin > 0)
	{
          // Signal 5 requests status -- which pins are online
	  if (pin == 5)
	    {
	      for (int thisPin = 3; thisPin < pinCount; thisPin++)
		{
		  int toSend = pins[thisPin];
		  delay(2);
		  Serial.print(toSend);
            
		  toSend = digitalRead(thisPin);
		  delay(2);
		  Serial.print(toSend);
            
		  Serial.flush();
		}
	    }
          // Signal 6 requests data from Arduino
	  else if (pin == 6)
	    {
	      dump_data();
              delay(2);
	    }
          // Otherwise it tries to toggle the pin
	  else if (pin != 101)
	    {
	      digitalWrite(pins[pin], HIGH  ^ digitalRead(pins[pin]));
	    }
	}
    }
  // Otherwise read and store sensor value(s)
  else
    {
      add_data();
    }
}

// Tries to read and store a temperature value every minute
void add_data()
{
  // Make sure we haven't updated in the past minute
  if ((now() - lastTime) > 60)
    {
      // Read the sensor value
      int sensorVal = analogRead(tempPin);
      // Convert
      float voltage = (sensorVal/1024.0) * 5.0;
      float temperature = (voltage - 0.5) * 100;
      // Set last updated time to current time
      lastTime = now();
      // Store and increment array counter
      readings[counter++] = temperature;
    } 
}

// Tries to send data to server
void dump_data()
{
  // Iterate over pin array
  for (int i = 0; i < numReadings; i++)
    {
      // If array[i] has a value > 0, send it
      if (readings[i] > 0)
	{
          delay(2);
          // "Send" node UUID
          Serial.println(randomPin++);
          delay(2);
          
          // Model 5 nodes, set to 1 if > 5
          if (randomPin > 5)
          {
            randomPin = 1;
          }
          
          // Print the reading
          Serial.println(readings[i]);
          delay(2); 
	}
      // "Remove" the value that was just sent
      readings[i] = -1;
    }
  // Reset counter
  counter = 0;
  delay(2);
}

  

