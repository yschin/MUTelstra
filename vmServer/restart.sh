#! /bin/bash
# Script to Restart Nginx + Django Server
sudo nginx -s reload
sudo python ./manage.py runfcgi host=127.0.0.1 port=8080
