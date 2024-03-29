/*
  # Example code for the moisture sensor
  # Editor     : Lauren
  # Date       : 13.01.2012
  # Version    : 1.0
  # Connect the sensor analog out to the A0(Analog 0) pin on the Arduino board
  # Connect the sensor VCC pin to 5v pin on Arduino the board
  # Connect the sensor GND pin to GND pin on the Arduino board.
  # the sensor value description
  # 0  ~300     dry soil
  # 300~700     humid soil
  # 700~950     in water
*/
const int humidityPin = A2;

void setup(){
  
  Serial.begin(9600);
  
}

void loop(){
  
  Serial.print("Moisture Sensor Value:");
  Serial.println(analogRead(humidityPin));  
  delay(100);
  
}
