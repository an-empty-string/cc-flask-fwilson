from fabric.api import env
from fabric.contrib.project import upload_project
from fabric.operations import put, run, sudo, local

env.hosts = ["{{ cookiecutter.app_deploy_target }}"]

def deploy():
    put("config/*.nginx.conf", "/etc/nginx/servers.d", use_sudo=True)
    put("config/*.supervisor.ini", "/etc/supervisor.d", use_sudo=True)

    sudo("rm -rf {{ cookiecutter.app_path }}/{{ cookiecutter.project_name }}")
    sudo("mkdir -p {{ cookiecutter.app_path }}/{{ cookiecutter.project_name }}")
    local("tar -czf /tmp/deploy.tar.gz app")
    put("/tmp/deploy.tar.gz", "/tmp/deploy.tar.gz")
    sudo("tar xzf /tmp/deploy.tar.gz -C {{ cookiecutter.app_path }}/{{ cookiecutter.project_name }}")
    local("rm /tmp/deploy.tar.gz")
    run("rm /tmp/deploy.tar.gz")
    sudo("chown -R {{ cookiecutter.app_user }} {{ cookiecutter.app_path }}/{{ cookiecutter.project_name }}")

    sudo("supervisorctl update")
    sudo("supervisorctl restart {{ cookiecutter.project_name }}")
    sudo("systemctl reload nginx")

def deprovision():
    sudo("supervisorctl stop {{ cookiecutter.project_name }}")
    sudo("rm /etc/nginx/servers.d/{{ cookiecutter.project_name }}.nginx.conf")
    sudo("rm /etc/supervisor.d/{{ cookiecutter.project_name }}.supervisor.ini")
    sudo("rm -rf {{ cookiecutter.app_path }}/{{ cookiecutter.project_name }}")
    sudo("supervisorctl update")
    sudo("systemctl reload nginx")

def ssl():
    sudo("certbot certonly --webroot --webroot-path /srv/web/static -d {{ cookiecutter.app_domain }}")
