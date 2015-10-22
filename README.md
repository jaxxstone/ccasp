# ccasp
**Cloud Controlled Automation Senior Project<br>
Fall Semester 2015**<br>
*Scope: Capstone senior project. RESTful cloud-based web application to remotely monitor and control Arduino-based microcontrollers communicating over a mesh topology.*

This web application serves as the front-end reporting and management system for a network of Arduino microcontrollers affixed with various sensors -- at this point, temperature, humidity, and soil moisture sensors are supported.

The web application is hosted on Amazon Web Services (AWS) and receives sensor values from a Raspberry Pi intermediary gateway. The network of microcontrollers transmit the values recorded by their respective sensors to the Raspberry, which populates the AWS RDS database.

The application can be accessed with the username `guest`, password `guest1234`.

[CCASP homepage](http://ccasp.elasticbeanstalk.com/)
