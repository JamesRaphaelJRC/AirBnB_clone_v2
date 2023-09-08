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
        arcFilnam = os.path.basename(archive_path).replace(".tgz", "")
        new_path = "/data/web_static/releases/{}".format(arcFilnam)

        put(archive_path, "/tmp/")
        run("rm -rf /data/web_static/releases/{}/".format(arcFilnam))
        run("mkdir -p {}".format(new_path))
        run("tar -xvzf /tmp/{}.tgz -C {} --strip-components=1".format(
                                                                    arcFilnam,
                                                                    new_path))
        run("rm /tmp/{}.tgz".format(arcFilnam))
        run("rm /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(new_path))
        return True
    except Exception as e:
        return False
