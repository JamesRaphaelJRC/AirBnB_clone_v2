#!/usr/bin/python3
''' Deploys an archive file on my webservers

    USAGE:
    fab -f 2-do_deploy_web_static.py do_deploy:archive_path='the path'.tgz

'''
import os
from fabric.api import run, put, env


env.hosts = ['ubuntu@54.224.24.109', 'ubuntu@54.160.116.141']


def do_deploy(archive_path):
    ''' Deploys an archive to 2 webservers '''
    if not os.path.isfile(archive_path):
        return False

    try:
        arch_file = archive_path.split("/")[-1]
        filename = arch_file.split(".")[0]
        path = "/data/web_static/releases/{}".format(filename)

        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(path))
        run("sudo tar -xvzf /tmp/{}.tgz -C {}/ --strip-components=1".
            format(filename, path))
        run("sudo rm /tmp/{}.tgz".format(filename))
        run("sudo rm -rf {}/web_static".format(path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {}/ /data/web_static/current".format(path))
        return True
    except Exception as e:
        return False
