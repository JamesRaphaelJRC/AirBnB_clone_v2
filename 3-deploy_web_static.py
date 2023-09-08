#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ['ubuntu@54.224.24.109', 'ubuntu@54.160.116.141']


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    my_file = "web_static_{}.tgz".format(now)

    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(my_file)).failed is True:
        return None
    return my_file


def do_deploy(archive_path):
    """ Distributes an archive to a web server."""
    if os.path.isfile(archive_path) is False:
        return False
    _file = archive_path.split("/")[-1]
    name = _file.split(".")[0]

    try:
        put(archive_path, "/tmp/{}".format(_file))
        run("rm -rf /data/web_static/releases/{}/".format(name))
        run("mkdir -p /data/web_static/releases/{}/".format(name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
            format(_file, name))
        ("rm /tmp/{}".format(_file))
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(name, name))
        run("rm -rf /data/web_static/releases/{}/web_static".format(name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
            format(name))
        return True
    except Exception as e:
        return False


def deploy():
    """Create and distribute an archive to a web server."""
    archive_file = do_pack()
    if archive_file is None:
        return False
    return do_deploy(archive_file)
