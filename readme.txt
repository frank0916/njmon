#njmon installation instruction on centos 8 with python3

1. install flask and gunicorn if they are not installed
pip3 install Flask 
pip3 install gunicorn

2.start guncorn
change current directory ~/njmon
./start.sh
#verify UI with browser for url http://localhost:8000

3. config nginx
sudo yum install nginx

#disable apached if it is running on port 80
sudo systemctl start httpd.service
sudo systemctl disable httpd.service

#replace the default server {} section with following block

copy following config setting to api_project
#################start
    server {
        listen       80;
        location / {
                proxy_pass http://127.0.0.1:8000;
        }
    }
###################end

#enable nginx service

sudo systemctl enable nginx
sudo systemctl start nginx

sudo setsebool httpd_can_network_connect on

4. set crontab task as following
0 * * * * ${HOME}/njmon/bin/copy.sh


