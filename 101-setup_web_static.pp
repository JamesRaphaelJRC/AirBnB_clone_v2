# Sets up webserver for deployment

package { 'nginx':
	ensure	=> 'installed',
}

file { '/data/':
	ensure	=> 'directory',
	owner	=> 'ubuntu',
	group	=> 'ubuntu',
}

file { '/data/web_static/':
	ennsure	=> 'directory',
	owner	=> 'ubuntu',
	group	=> 'ubuntu',
}

file { '/data/web_static/releases/':
	ensure	=> 'directory',
	owner	=> 'ubuntu',
	group 	=> 'ubuntu',
}

file { '/data/web_static/shared/':
	ensure	=> 'directory',
	owner	=> 'ubuntu',
	group	=> 'ubuntu',
}

file { '/data/web_static/releases/test/':
	ensure	=> 'directory',
	owner	=> 'ubuntu',
	group	=> 'ubuntu',
}

file { '/data/web_static/releases/test/index.html':
	ensure	=> 'file',
	owner	=> 'ubuntu',
	group	=> 'ubuntu',
	content	=> '<html><body>Testing my puppet skills</body></html>',
}

file { '/data/web_static/current':
	ensure	=> 'link',
	target 	=> '/data/web_static/releases/test',
	force	=> true,
	owner	=> 'ubuntu',
	group	=> 'ubuntu',
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
	notify	=> Service['nginx'].
}

service { 'nginx':
	ensure	=> 'running',
	enable	=> true,
	require	=> File['/etc/nginx/sites-available/default']
}
