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
as template file use  [pl_app.service](https://github.com/augustodoc/CiscoPlApp/blob/master/pl_app.service)  
the Tag`<name></name>` in XML file is critical, it expand name of service with host (%h) and a costant key ':cisco-pl-app'      which is used for identify only a remote machine with CISCO PL-APP (Jupyter Notebook)  
```xml
<name replace-wildcards="yes">%h:cisco-pl-app</name>
```
This method with different key name can be used for discover a generic services type. 
### Install methods
1. Local directory
2. Python package


