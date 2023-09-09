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
        # Gets the filename of the archieve
        arch_file = archive_path.split("/")[-1]
        filename = arch_file.split(".")[0]
        path = "/data/web_static/releases/{}".format(filename)

        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(path))
        # Decompresses all the items in the archieve directly to the required
        # folder without the parent folder of the archieve.
        run("sudo tar -xvzf /tmp/{}.tgz -C {}/ --strip-components=1".
            format(filename, path))
        run("sudo rm /tmp/{}.tgz".format(filename))
        # Removes the former symbolic link to the old deployed items
        run("sudo rm -rf /data/web_static/current")
        # Recreates a link to the newly deployed items
        run("sudo ln -s {}/ /data/web_static/current".format(path))
        return True
    except Exception as e:
        return False
