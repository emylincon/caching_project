## This is a property of London South Bank University licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

### Please get permission before use

### @Author: Emeka Emmanuel Ugwuanyi ugwuanye@lsbu.ac.uk with contributions from Saptarshi Ghosh
### GNS3 Architecture
![gns3 architecture](gns3_arch.png)
### Docker Linux Use instructions
#### Prior to Package Download
* change your docker root password
* install sudo in your docker
* add a new user in your linux with the following details:
- username: `mec`
- password: `password`
* `usermod -aG sudo mec`
* then clone the folder into the mec directory 
#### After Download 
* Change directory to ./caching_project and Run set_up.sh as sudo
* Start your ssh server
* You will require a web server, make sure it is running
* choose any of the algorithm and run it
* there are 4 caching co-operative algorithms with each having a gui version with shows realtime graphs
* always run gui version as sudo
* You will be required to put the following:
- ip address of the webserver (use mec.x10host.com)
- number of requests (default is 30)
- number of html contents (choose from 7 to 20). 7 is default
* After each run; run the files_cache/refresh_db.py file to refresh the database and clean up residual files

### Any other Linux device 
* install sudo
* add a new user in your linux with the following details:
- username: `mec`
- password: `password`
* `usermod -aG sudo mec`
* then clone the folder into the mec directory 
#### After Download 
* Change directory to ./caching_project and Run set_up.sh as sudo
* Start your ssh server
* You will require a web server, make sure it is running
* choose any of the algorithm and run it
* there are 4 caching co-operative algorithms with each having a gui version with shows realtime graphs
* always run gui version as sudo
* You will be required to put the following:
- ip address of the webserver
- number of requests (default is 500)
- number of html contents (choose from 7 to 20). 7 is default
* After each run; run the files_cache/refresh_db.py file to refresh the database and clean up residual files

### Note
* if you run a script with an ssh tag on an mec, all other mecs shoudl also run an ssh tag script
* likewise if you run a script with a multicast tag all other mecs should also run a multicast tag script


### zipf distribution parameter
The zipf parameter to use is 1.2 this is cited by the following article [Cooperate Caching with Multicast for Mobile Edge
Computing in 5G Networks](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8108600)
__________________________________________________
#### SET UP Commands
```
apt update  
passwd   
password   
password   
apt install git sudo -y  
adduser mec  
password  
password  
usermod -aG sudo mec  
su - mec  
git clone https://github.com/emylincon/caching_project.git  
cd caching_project  
sudo bash set_up.sh  
password
```
