#!/usr/bin/python3
# Generates a .tgz archive from the contents of a web_static folder
from fabric.api import local
from datetime import datetime
import os


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
