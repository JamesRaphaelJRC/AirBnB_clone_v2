#!/usr/bin/env bash
# Sets up my webservers for the deployment of web_static.

if [ ! -x "$(command -v nginx)" ]; then
	apt-get update
	apt-get install -y nginx
fi

dir1="/data/web_static/releases/test/"
dir2="/data/web_static/shared/"

if [ ! -d "$dir1" ]; then
	mkdir -p "$dir1"
fi

if [ ! -d "$dir2" ]; then
	mkdir -p "$dir2"
fi

touch /data/web_static/releases/test/index.html

printf %s "<html>
<head>
</head>
<body>
  Hello world!
</body>
</html>
" >  /data/web_static/releases/test/index.html

target="/data/web_static/releases/test/"
link="/data/web_static/current"

if [ -L "$link" ]; then
	rm -f "$link"
fi

ln -s "$target" "$link"

chown -R ubuntu:ubuntu /data/

printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}
" > /etc/nginx/sites-available/default

service nginx restart
