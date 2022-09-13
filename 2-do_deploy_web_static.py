#!/usr/bin/python3
from fabric.api import run, env, put
from os import path


env.hosts = ['54.210.85.213', '54.91.141.251']
env.user = 'ubuntu'


def do_pack():
    """
    Funtion that compress a folder
    """
    try:
        local('mkdir -p versions')
        date = datetime.now()
        format = "%Y%m%d%H%M%S"
        path = 'versions/web_static_{}.tgz'.format(date.strftime(format))
        local('tar -cvzf {} web_static'.format(path))
        return path
    except Exception as error:
        return None


def do_deploy(archive_path):
    """Fabric script that deploys an archive to web servers"""
    if not path.exists(archive_path):
        return False

    try:
        file_path = archive_path.split('/')[1]
        filename = file_path.split('.')[0]
        put(archive_path, "/tmp/")
        run('mkdir -p /data/web_static/releases/{}'.format(filename))
        run('tar -zxf /tmp/{} -C /data/web_static/releases/{}/'
            .format(file, filename))
        run('rm /tmp/{}'.format(file))
        run('mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}/'.format(filename, filename))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(filename))
        run('rm -rf /data/web_static/current')
        run('ln -sf /data/web_static/releases/{}/ /data/web_static/current'
            .format(filename))
        print('New version deployed!')
        return True
    except Exception as e:
        return False
