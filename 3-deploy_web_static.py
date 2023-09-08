#!/usr/bin/python3
''' Generates a .tgz archive from the contents of a web_static folder '''
from datetime import datetime
from fabric.api import local, run, put, env
import os


env.hosts = ['ubuntu@54.224.24.109', 'ubuntu@54.160.116.141']


def do_pack():
    ''' Cretes a .tgz file from all contents of the directory 'web_static' '''
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    my_file = "web_static_{}.tgz".format(now)

    if not os.path.isdir("versions"):
        local("mkdir versions")
    status = local("tar -czvf versions/{} web_static".format(my_file))
    if status.failed:
        return None
    return my_file


'''
    Deploys an archive file on my webservers

    USAGE:
    fab -f 2-do_deploy_web_static.py do_deploy:archive_path='the path'.tgz

'''


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


def deploy():
    ''' Creates and distribute an archive file to webservers in the env.hosts
    '''
    archive_file = do_pack()
    if archive_file is None:
        return False
    return do_deploy(archive_file)
