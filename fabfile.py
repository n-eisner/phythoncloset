# -*- coding: utf-8 -*-

import os
import datetime

from fabric.api import local, cd, sudo
from fabric.colors import green, red
from fabric.operations import put, prompt
# from fabric.decorators import runs_once, roles, task
from contextlib import contextmanager

# Import project settings
try:
    from fabconfig import *
except ImportError:
    import sys
    print "You need to define a fabconfig.py file with your project settings"
    sys.exit()


@contextmanager
def shell_env(**env_vars):
    orig_shell = env['shell']
    env_vars_str = ' '.join('{0}={1}'.format(key, value)
                           for key, value in env_vars.items())
    env['shell'] = '{0} {1}'.format(env_vars_str, orig_shell)
    yield
    env['shell'] = orig_shell

# SETUP


def setup_venv_local2():
    local('virtualenv --no-site-package -p python2.7 venv')
    local('source venv/bin/activate && pip install -r web/deploy/requirements.txt')


def setup_venv_local():
    local('virtualenv --no-site-packages --distribute -p python2.7 venv')
    local('virtualenv --relocatable venv')
    local('source venv/bin/activate && pip install -r web/deploy/requirements.txt')


def setup_django_local():
    local('source venv/bin/activate && cd web && ./manage.py syncdb && ./manage.py migrate')


def setup_submodules():
    local('git submodule update --init')


def setup_local():
    setup_venv_local()
    setup_django_local()


def import_securities():
    local('venv/bin/python web/manage.py import_securities')


def import_search_data():
    local('venv/bin/python web/manage.py import_search_data')


def vendor():
    local('cd vendor && make all')


def run():
    local('venv/bin/python web/manage.py runserver')


#####


def input_with_default(prompt, default, pwd=False):
    if pwd:
        x = getpass.getpass("%s (%s): " % (prompt, default))
    else:
        x = raw_input("%s (%s): " % (prompt, default))
    if not x:
        return default
    return x


def config():
    project_name = input_with_default("Project Name", "project")
    project_domain = input_with_default("Project Domain", "localhost")
    project_server_auth = input_with_default("Project Server/Auth", "root@localhost")

    with open('fabconfig.py', 'r+') as f:
        new_fabconfig = f.read().replace('{{ PROJECT_NAME }}', project_name).replace('{{ PROJECT_DOMAIN }}', project_domain).replace('{{ PROJECT_SERVER_AUTH }}', project_server_auth)
        f.seek(0)
        f.write(new_fabconfig)
        f.truncate()

    with open('web/deploy/nginx.conf', 'r+') as f:
        new_nginx = f.read().replace('{{ PROJECT_DOMAIN }}', project_domain).replace('{{ PROJECT_NAME }}', project_name)
        f.seek(0)
        f.write(new_nginx)
        f.truncate()

    print green("All set up!")
    print "now just run 'fab create_virtualenv' without quotes to create the initial virtualenv on the server and 'fab deploy' when you're ready to deploy"


def clean_venv():
    local('rm -rf venv')


def clean_pyc():
    local("find . -name '*.pyc' -print0|xargs -0 rm", capture=False)


########


def _get_commit_id():
    """
    Return the commit ID for the branch about to be deployed
    """
    return local('git rev-parse HEAD', capture=True)[:20]


def notify(msg):
    bar = '+' + '-' * (len(msg) + 2) + '+'
    print green('')
    print green(bar)
    print green("| %s |" % msg)
    print green(bar)
    print green('')

# Deployment tasks


def deploy():
    notify('Deploying to %s' % env.hosts)
    current = _get_commit_id()[0:7]
    env.version = prompt(red('Choose tag/commit to build from (%s): ' % current))
    if env.version is '':
        env.version = current

    pack()
    deploy_code(env.build_file)

    update_virtualenv()
    migrate()
    compress_files()
    install_cron()
    deploy_nginx_config()

    switch_symlink()

    reload()
    delete_old_builds()


def deploy_lite():
    notify('Deploying to %s' % env.hosts)
    env.version = _get_commit_id()[0:7]
    pack()
    deploy_code(env.build_file)
    migrate()
    compress_files()

    switch_symlink()
    reload_lite()
    delete_old_builds()


def set_ssh_user():
    if 'TANGENT_USER' in os.environ:
        env.user = os.environ['TANGENT_USER']
    else:
        env.user = prompt(red('Username for remote host? [default is current user] '))
    if not env.user:
        env.user = os.environ['USER']


def reload():
    reload_python_code()
    reload_nginx()
    enable()


def reload_lite():
    sudo('touch %(enabled_wsgi)s' % env)


def pack():
    notify("Building from refspec %s" % env.version)
    env.build_file = '/tmp/build-%s.tar.gz' % str(env.version)
    local('git archive --format tar %s %s | gzip > %s' % (env.version, env.web_dir, env.build_file))

    now = datetime.datetime.now()
    env.build_dir = '%s-%s' % (env.build, now.strftime('%Y-%m-%d-%H-%M'))
    env.code_dir = '%s/%s' % (env.builds_dir, env.build_dir)


def upload(local_path, remote_path=None):
    """
    Uploads a file
    """
    if not remote_path:
        remote_path = local_path
    notify("Uploading %s to %s" % (local_path, remote_path))
    put(local_path, remote_path)


def unpack(archive_path):
    notify('Unpacking files')
    sudo('mkdir -p %(builds_dir)s' % env)
    with cd(env.builds_dir):
        sudo('tar xzf %s' % archive_path)

        # Create new build folder
        sudo('if [ -d "%(build_dir)s" ]; then rm -rf "%(build_dir)s"; fi' % env)
        sudo('mv %(web_dir)s %(build_dir)s' % env)

        # Add file indicating Git commit
        sudo('echo -e "refspec: %s\nuser: %s" > %s/build-info' % (env.version, env.user, env.build_dir))

        # Remove archive
        sudo('rm %s' % archive_path)


def deploy_code(archive_file):
    upload(archive_file)
    unpack(archive_file)


def create_virtualenv():
    """
    create venv if it doesn't exist
    """
    notify('Creating venv')

    sudo('mkdir -p %(builds_dir)s' % env)
    with cd(env.project_dir):
        sudo('/usr/local/bin/virtualenv --no-site-packages --distribute venv')


def update_virtualenv():
    """
    Install the dependencies in the requirements file
    """
    notify('Updating venv')

    with cd(env.code_dir):
        sudo('source %s/bin/activate && pip install -r deploy/requirements.txt' % env.virtualenv)


def migrate():
    """
    Apply any schema alterations
    """
    notify("Applying database migrations")
    with cd(env.code_dir):
        with shell_env(DJANGO_CONF='conf.prod'):
            sudo('source %s/bin/activate && ./manage.py syncdb --noinput > /dev/null' % env.virtualenv)
            sudo('source %s/bin/activate && ./manage.py migrate --ignore-ghost-migrations' % env.virtualenv)


def update_security_data():
    """
    updates security data on the server
    """
    notify("updating security data")
    with cd(env.code_dir):
        with shell_env(DJANGO_CONF='conf.prod'):
            sudo('source %s/bin/activate && ./manage.py import_search_data' % env.virtualenv)


def compress_files():
    """
    run compressor
    """
    notify("compressing files")
    with cd(env.code_dir):
        with shell_env(DJANGO_CONF='conf.prod'):
            sudo('source %s/bin/activate && ./manage.py compress' % env.virtualenv)


def install_cron():
    with cd(env.code_dir):
        sudo('deploy/cron.d/install.sh')


def switch_symlink():
    notify("Switching symlinks")
    with cd(env.project_dir):
        # Create new symlink for build folder
        sudo('if [ -h current ]; then unlink current; fi' % env)
        sudo('ln -s %(builds_dir)s/%(build_dir)s current' % env)


def deploy_nginx_config():
    notify('Moving nginx config into place')
    with cd(env.code_dir):
        sudo('mv %(nginx_conf)s /etc/nginx/conf.d/%(project_code)s.conf' % env)


def reload_python_code():
    notify('Touching WSGI file to reload python code')
    with cd(env.builds_dir):
        sudo('if [ -h %(available_wsgi)s ]; then unlink %(available_wsgi)s; fi' % env)
        sudo('ln -s %(project_dir)s/current/%(wsgi)s %(available_wsgi)s' % env)
        sudo('touch %(available_wsgi)s' % env)


def reload_nginx():
    notify('Reloading nginx configuration')
    sudo('/etc/init.d/nginx force-reload')


def delete_old_builds():
    notify('Deleting old builds')
    with cd(env.builds_dir):
        sudo('find . -maxdepth 1 -type d -name "%(build)s*" | sort -r | sed "1,9d" | xargs rm -rf' % env)


def enable():
    """
    gets uwsgi to reload python code
    """
    notify('Enabling app')
    sudo('if [ ! -f %(enabled_wsgi)s ]; then ln -s %(available_wsgi)s %(enabled_wsgi)s; fi' % env)
    sudo('touch %(enabled_wsgi)s' % env)
