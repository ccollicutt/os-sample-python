# Flask Sample Application

This repository provides a sample Python web application implemented using the Flask web framework and hosted using ``gunicorn``. It is intended to be used to demonstrate deployment of Python web applications to OpenShift 3.

## Implementation Notes

This sample Python application relies on the support provided by the default S2I builder for deploying a WSGI application using the ``gunicorn`` WSGI server. The requirements which need to be satisfied for this to work are:

* The WSGI application code file needs to be named ``wsgi.py``.
* The WSGI application entry point within the code file needs to be named ``application``.
* The ``gunicorn`` package must be listed in the ``requirements.txt`` file for ``pip``.

In addition, the ``.s2i/environment`` file has been created to allow environment variables to be set to override the behaviour of the default S2I builder for Python.

* The environment variable ``APP_CONFIG`` has been set to declare the name of the config file for ``gunicorn``.

## Deployment Steps

To deploy this sample Python web application from the OpenShift web console, you should select ``python:2.7``, ``python:3.3``, ``python:3.4`` or ``python:latest``, when using _Add to project_. Use of ``python:latest`` is the same as having selected the most up to date Python version available, which at this time is ``python:3.4``.

The HTTPS URL of this code repository which should be supplied to the _Git Repository URL_ field when using _Add to project_ is:

* https://github.com/ccollicutt/os-sample-python.git

If using the ``oc`` command line tool instead of the OpenShift web console, to deploy this sample Python web application, you can run:

```
oc new-app https://github.com/ccollicutt/os-sample-python.git
```

In this case, because no language type was specified, OpenShift will determine the language by inspecting the code repository. Because the code repository contains a ``requirements.txt``, it will subsequently be interpreted as including a Python application. When such automatic detection is used, ``python:latest`` will be used.

If needing to select a specific Python version when using ``oc new-app``, you should instead use the form:

```
oc new-app python:2.7~https://github.com/ccollicutt/os-sample-python.git
```

## Test Locally

Create a virtual env and install required pip packages.

```
virtualenv ~/venv
. ~/venv/bin/activate
pip install -r requirements.txt
```

Run the webserver.

```
python wsgi.py
```

Curl localhost.

```
$ curl localhost:5000/healthcheck
{"status": "success", "timestamp": 1552333343.809602, "hostname": "ash", "results": [{"output": "ok", "checker": "check_health", "expires": 1552333370.809593, "passed": true, "timestamp": 1552333343.809593}]}
```

## Setup Local Database 

If on Fedora.

```
sudo dnf install mariadb-server
sudo systemctl start mariadb
```

Create db and setup user/password.

```
CREATE DATABASE os_sample_python;
GRANT ALL PRIVILEGES ON os_sample_python.* TO 'os_sample_python'@'localhost' IDENTIFIED BY 'P@ssw0rd';
```

Setup environment variables.

```
export MYSQL_USER=os_sample_python
export MYSQL_PASSWORD=P@ssw0rd
export MYSQL_DATABASE=os_sample_python
export MYSQL_SERVICE_HOST=localhost
```
