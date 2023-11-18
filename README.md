# GlowUp [![pipeline status](https://gitlab.com/5theta/glowup/badges/master/pipeline.svg)](https://gitlab.com/5theta/glowup/commits/master) [![coverage report](https://gitlab.com/5theta/glowup/badges/master/coverage.svg)](https://gitlab.com/5theta/glowup/commits/master)

## Prerequisites

- git
- [asdf](https://asdf-vm.com/#/core-manage-asdf-vm)

[Install asdf](https://asdf-vm.com/#/core-manage-asdf-vm) into your pc and add python plugin.

```sh
$ asdf plugin-add python
$ asdf install python 3.8.7

* ubuntu
$ sudo apt-get install libmysqlclient-dev libssl-dev

* arch
pacman -S libmariadbclient

* fedora
dnf  install mariadb-devel

* opensuse
zypper in libmariadb-devel libssl48 mariadb-client python38-devel

```
First we have to clone the repository and create virtual environment for python.
To do so, execute following

```sh
$ asdf local python 3.8.7
$ pip install pipenv
$ asdf reshim python 
$ pipenv --pythoon 3.8.7 lock
$ pipenv --python 3.8.7 sync
```

Apply db migrations

```sh
$ pipenv run python manage.py makemigrations
$ pipenv run python manage.py migrate
```

```
pipenv run python manage.py createsuperuser

```

Run application

```sh
$ pipenv run python manage.py runserver
```

* log into /admin and create a new customer group

# on development
* set debug true
