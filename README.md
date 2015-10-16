# ccasp
Cloud Controlled Automation Fall Semester 2015 Senior Project

This web application serves as the front-end reporting and management system for a network of Arduino microcontrollers affixed with various sensors -- at this point, temperature, humidity, soil moisture, and voltage sensors are supported.

The web application is hosted on AWS and receives sensor values from a Raspberry Pi intermediary. The network of microcontrollers transmit the values recorded by their respective sensors to the Raspberry, which decodes and decrypts the received message and populates the AWS RDS database.
