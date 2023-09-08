#!/usr/bin/python3
''' Deploys an archive file on my webservers '''
import os
from fabric.api import run, put, env


env.hosts = ['ubuntu@54.224.24.109', 'ubuntu@54.160.116.141']


def do_deploy(archive_path):
    ''' Deploys an archive to 2 webservers '''

    if not os.path.isfile(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")
        archFileName = os.path.basename(archive_path).replace(".tgz", "")
        new_path = "/data/web_static/releases/{}".format(archFileName)
        run("mkdir -p {}".format(new_path))
        run("tar -xvzf /tmp/{}.tgz -C {}".format(archFileName, new_path))
        run("rm /tmp/{}.tgz".format(archFileName))
        run("rm /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(new_path))
        return True
    except Exception as e:
        return False
