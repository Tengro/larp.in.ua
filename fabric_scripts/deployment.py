from fabric import Connection
from fabric import task


@task
def deploy(ctx):
    host = "161.35.78.186"
    user = "larpbot"
    project_dir = "/home/larpbot/larp.in.ua/api/"
    conn = Connection(f"{user}@{host}")
    with conn.cd(project_dir):
        conn.run("git pull --rebase origin main", pty=True)
        conn.run("source ~/.virtualenvs/larpbot/bin/activate && ./manage.py migrate")
        conn.run("sudo systemctl restart gunicorn celery nginx celerybeat", pty=True)
