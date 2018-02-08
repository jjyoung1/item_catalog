# Linux Server Configuration Project

## Project Documentation
The original documentation for the Item Catalog project is located [here](documentation/project.md)

## Site Information
Server Address: 18.218.247.187

DNS Name: http://ec2-18-218-247-187.us-east-2.compute.amazonaws.com

## Software Requirements
### Server Packages
* Apache2
* finger
* Uncomplicated Firewall (ufw)
* Apache2 with mod-wsgi for Python3
* Postgreql Version 10
*


## References
[Amazon Lightsail Documentation](https://lightsail.aws.amazon.com/ls/docs/all)

### Digital Ocean
https://www.digitalocean.com/community/tutorials/how-to-run-django-with-mod_wsgi-and-apache-with-a-virtualenv-python-environment-on-a-debian-vps

https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04

### Flask
[Flask running in Virtual Environments on Apache](http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/)

[Flask Web Development, 2nd Edition by Miguel Grinberg, O'Reilly Media, Inc., 2018](https://www.safaribooksonline.com/library/view/flask-web-development/9781491991725/part02.html)

### Postgres
[Postgres Documentation](https://www.postgresql.org/docs/10/static)

### SQLAlchemy
[SQL Alchemy Datanase Connections](http://docs.sqlalchemy.org/en/latest/dialects/postgresql.html)

[SQL Alchemy Virtual environments with wsgi](http://modwsgi.readthedocs.io/en/develop/user-guides/virtual-environments.html)

### Udacity
[Linux Server Configuration](https://classroom.udacity.com/nanodegrees/nd004/parts/ab002e9a-b26c-43a4-8460-dc4c4b11c379)

[Backend Databases and Applications](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0)



## Server Configuration
* Create Ubuntu 16.04 instance on Amazon Lightsail
* Update all packages installed
* Removed unusued packages
* Installed finger
* Installed ufw and configured it with the following rules

	To | Action | From
	---|--------|-----
	80/tcp |                    ALLOW |      Anywhere
	2200/tcp |                  ALLOW |      Anywhere
	123            |            ALLOW |      Anywhere
	80/tcp (v6)  |              ALLOW |      Anywhere (v6)
	2200/tcp (v6)  |            ALLOW  |     Anywhere (v6)
	123 (v6)     |              ALLOW  |     Anywhere (v6)

* Modified the Lightsail firewall to match the machine firewall rules
* Configured Apache to serve wsgi applications
* Installed Postgres
* Installed Git
* Created the virtual environment to run the application and installed
the python packages specified in the 'requirements.txt' file
* created a 'catalog' user
* cloned the git repository into the /home/catalog/public_wsgi directory
* Configured the Apache default VirtualHost to serve the catalog app within the virtual environment
* Created and installed rsa keys for users: jjyoung and grader
* Modified sshd to disallow password login and allow only key-based authentication
* Enabled 'sudo' for designated users


