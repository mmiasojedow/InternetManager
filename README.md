# Interner Manager
Project for monitoring WiFi and fixing problems for TP-Link modem using RaspberryPi.

## Features
The primary function is selenium running  tplinkmodem.net app to catch errors of internet connection, basing on CSS classes, and reset the connection if such error appears. Secondary - the app is testing connection speed. Both functions are creating files with reports, which are later sent via email. 
Whole project is ment to run by cron on RaspberryPi, for example:
```
0 7 * * * python3 WiFiBot.py
*/15 7-22 * * * python3 speed_test.py
0 23 * * * /usr/bin/pkill -f WiFiBot.py
0 23 * * * pkill chromium
0 23 * * * python3 email_sender.py
```
 
## Technologies
* Python
* Selenium
* Cron
