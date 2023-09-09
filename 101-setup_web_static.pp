# Sets up webserver for deployment

package { 'nginx':
	ensure	 => 'present',
	provider => 'apt'
}

file { '/data/':
	ensure	=> 'directory'
}

file { '/data/web_static/':
	ennsure	=> 'directory'
}

file { '/data/web_static/releases/':
	ensure	=> 'directory'
}

file { '/data/web_static/shared/':
	ensure	=> 'directory'
}

file { '/data/web_static/releases/test/':
	ensure	=> 'directory'
}

file { '/data/web_static/releases/test/index.html':
	ensure	=> 'file',
	content	=> '<html><body>Testing my puppet skills</body></html>'
}

file { '/data/web_static/current':
	ensure	=> 'link',
	target 	=> '/data/web_static/releases/test',
	force	=> true
}

exec { 'chown -R ubuntu:ubuntu /data/':
	path	=> '/usr/bin:/usr/local/bin/:/bin/'
}

file { '/var/www':
	ensure	=> 'directory'
}

file { '/var/www/html':
	ensure	=> 'directory'
}

file { '/var/www/html/index.html':
	ensure	=> 'present',
	content	=> "Hello world from /var/www/index.html***\n"
}

file { '/var/www/html/404.html':
	ensure	=> 'present',
	content	=> "Ceci n'est pas une page - Error page\n"
}

file { '/etc/nginx/sites-availabe/default':
	ensure	=> 'file',
	content	=> "
server {
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
        return 301 http://google.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}
",
	require => Package['nginx'],
	notify	=> Service['nginx']
}

exec { 'nginx restart':
	path => '/etc/init.d/'
}
