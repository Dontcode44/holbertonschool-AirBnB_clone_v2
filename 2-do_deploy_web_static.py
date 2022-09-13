#!/usr/bin/python3
"""Using Fabric to do things on servers"""

from threading import local
from fabric.api import run, env, put
from datetime import datetime 
import os


env.hosts = ['54.210.85.213', '54.91.141.251']


def do_pack():
    try:
        formato = "%Y%m%dT%H%M%S"
        created_at = date_now.created_at.strftime(formato)
        local("mkdir -p /versions")
        file_tgz = "web_static_{}.tgz".format(created_at)
        local("tar -cvzf versions/{}.tgz web_static".format(file_tgz))
        return file_tgz
    except:
        return None


def do_deploy(archive_path):
    if os.path.isfile(archive_path) is False:
        return False
    try:
        put(archive_path, "/tmp")
        id_file = archive_path.split("_")
        id_final = id_file[2][:-4]
        folder = "/data/web_static/releases/"
        run("mkdir -p {}web_static_{}/".format(folder, id_final))
        run("tar -xzf /tmp/web_static_{}.tgz -C {}web_static_{}/"
            .format(id_final, folder, id_final))
        run("rm /tmp/web_static_{}.tgz".format(id_final))
        run("mv {}web_static_{}/web_static/* {}web_static_{}/"
            .format(folder, id_final, folder, id_final))
        run("rm -rf {}web_static_{}/web_static".format(folder, id_final))
        run("rm -rf /data/web_static/current")
        run("ln -s {}web_static_{}/ /data/web_static/current"
            .format(folder, id_final))
        return True
    except:
        return False
