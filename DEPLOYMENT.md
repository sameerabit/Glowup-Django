```sh
$ git clone <repo-url> <clone-location>
$ cd <clone-location>
```

```sh
$ asdf local python 3.8.7
$ pip install pipenv
$ asdf reshim python 
$ pipenv lock
$ pipenv sync
$ pipenv install --dev
```

Apply db migrations

```sh
$ pipenv run python manage.py makemigrations
$ pipenv run python manage.py migrate
```

Create super user
```
pipenv run python manage.py createsuperuser
```

create `/etc/systemd/system/glowup.service` and put the following content
```
[Unit]
Description=Glowup
After=network.target

[Service]
Type=idle
User=ubuntu
Group=ubuntu
ExecStart=/path/to/gunicorn --workers 3 --bind unix:/path/to/glowup.sock --chdir /path/to/project project.wsgi --reload
TimeoutStartSec=600
TimeoutStopSec=600

[Install]
WantedBy=multi-user.target
```

```
sudo systemctl enable glowup.service
sudo systemctl start glowup.service
```