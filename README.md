# flask-raspberrypi-servo
Install a webserver, and deploy a website on a raspberry pi to move a servo motor.

Follow these steps before you start cloning the repo.

set keyboard to english us

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install vim

~/.vimrc
set smartindent
set tabstop=4
set expandtab

sudo apt-get install nginx
sudo service nginx start

sudo apt-get install build-essential python-dev
sudo pip install uwsgi

sudo pip install flask
# 

cd Desktop
mkdir switch
cd switch

#

vim app.py
from flask import Flask
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
	return "hello world"

if __name__ == "__main__":
	app.run()
#
python app.py
try running the app using python and mod_wsgi:

python app.py

try running the app using uwsgi:

uwsgi --socket 0.0.0.0:8000 --protocol=http -w app:app

make wsgi init file in the app directory

[uwsgi]

chdir = /home/pi/Desktop/switch
module = app:app

master = true
processes = 1
threads = 2

uid = pi 
gid = pi
socket = /tmp/app.sock
chmod-socket = 777
vacuum = true

die-on-term = true

#
Test initialization

uwsgi --ini /home/Desktop/switch/uwsgi_config.ini

check that a file was created at /tmp/ with app.sock
#

Set uswgi to start after reboot
sudo vi /etc/rc.local

add this line after exit 0
/usr/local/bin/uwsgi --ini /home/pi/Desktop/switch/uwsgi_config.ini --uid pi --gid pi --daemonize /var/log/uwsgi.log

#
sudo rm /etc/nginx/sites-enabled/default
sudo service nginx start
sudo vim /etc/nginx/sites-available/app_proxy

server {
 listen 80;
 server_name localhost;

 location / { try_files $uri @app; }
 location @app {
 include uwsgi_params;
 uwsgi_pass unix:/tmp/app.sock;
 }
}

sudo ln -s /etc/nginx/sites-available/app_proxy /etc/nginx/sites_enabled

sudo service nginx restart

make sure there is an init call to uwsgi that creates the 777 socket
and check localhost:80
