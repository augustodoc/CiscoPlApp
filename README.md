# CiscoPlApp  
Python 3 TKinter GUI  Utility
* Scan **HTTP Avahi service**
* Applied for Raspberry Pi with **CISCO Pl-App** (Lab IOT course) on Linux OS  
## Configure Avahi HTTP service
1. Check if avahi-daemon is installed and running  on remote device (aka  Raspberry Pi)  
issue a command **sudo service --status-all**  
if command output show  
**[ + ]  avahi-daemon**  
is all **ok**.  
else install it with **sudo apt-get install avahi-daemon**  

2. In /etc/avahi/services directory put a service definition XML file with extension **.service**  
as template [pl_app.service](https://github.com/augustodoc/CiscoPlApp/blob/master/pl_app.service)

