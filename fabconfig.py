# -*- coding: utf-8 -*-

"""
Project-specific environment information.

This module provides configuration for the fabfile to run with.  The idea is
that the fabfile is project-agnostic and all configuration takes place within
this file.

In reality, this won't be entirely true as each project will evolve specific
deployment needs.  Nevertheless, this still provides a good starting point.
"""
from fabric.api import env

# Many things are configured using the client and project code
env.client = ''
env.domain = 'pennapps.rohunbansal.com'
env.project_code = 'pennapps2013s'

# This is the name of the folder within the repo which houses all code
# to be deployed.
env.web_dir = 'web'

# Environment-agnostic folders
env.project_dir = '/data/web/apps/%(project_code)s' % env
env.builds_dir = '%(project_dir)s/builds' % env
env.available_wsgi = '/data/web/apps-available/%(project_code)s.ini' % env
env.enabled_wsgi = '/data/web/apps-enabled/%(project_code)s.ini' % env


def _configure(build_name):
    env.build = build_name
    env.virtualenv = '%(project_dir)s/venv/' % env
    env.code_dir = '%(project_dir)s/current/' % env
    env.nginx_conf = 'deploy/nginx.conf' % env
    env.wsgi = 'deploy/wsgi.ini' % env


def test():
    _configure('test')
    env.hosts = ['test.%(project_code)s.%(client)s.%(domain)s'] % env


def prod():
    _configure('prod')
    # Production hosts needs filling in
    env.hosts = ['root@66.175.220.170']
