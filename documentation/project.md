# item_catalog
Catalog app to manage item categories and items.  Implements both Web
and Restful interfaces

## Getting the source code
The source code is hosted on Github at:
https://github.com/jjyoung1/item_catalog

## Virtual Enviornment Creation
Python Version: 3.5.2

The requirements.txt file contains the information required to create
the virtual environment.  The following command will create the
appropriate virtual environmnet

* $ virtualenv --python='path to Python version 3.5.2' requirements.txt

## Startup
Execute catalog.py within the virutal environment to start program
By default, using the flask development server, the homepage is located
at http://localhost:5000/

## URL Summary
* / - homepage of Catalog App
* /auth/gdisconnect - Disconnect from Google OAuth login session
* /auth/fbdisconnect - Disconnect from Facebook OAuth login session
* /auth/login - Login page
* /auth/logout - Logout of any existing login sessions
* /category/new - create new category
* /catalog/\<category id\> - List items in specified category
* /catalog/\<category id\>/item/new - Create new item in category
* /item/\<item id\> - Item description
* /item/edit/\<item id\> - Edit item
* /catalog/\<category\>/\<item\>/delete - Delete item confirmation
* /site-map - For development purpose to check flask routing table
* /api/catalog - REST endpoint for reading the entire catalog

## Executing Self Tests
Within the directory containing **catalog.py** execute the following:
* $ source venv/bin/activate
* $ export FLASK_APP=catalog.py
* $ export FLASK_COVERAGE=1
* $ export FLASK_DEBUG=1
* $ flask test

## Development Notes
The basic architecture was derived from the information in the pre-release
version (available through [Safari Books Online](https://www.safaribooksonline.com/library/view/flask-web-development/9781491991725/)) of the book:

[Flask Web Development: Developing Web Applications with Python 2nd Edition
by Miguel Grinberg](https://www.amazon.com/Flask-Web-Development-Developing-Applications/dp/1491991739/ref=sr_1_2?ie=UTF8&qid=1515431839&sr=8-2&keywords=Flask+Web+Development)

The Google and Facebook login processes were updated from the methods provided
by Udacity to the current methods specified by the OAuth providers

The secure handling of redirection from the web pages has been implemented
using the method list [here](http://flask.pocoo.org/snippets/62/)

PEP8 has been purposely violated in some files w.r.t. line length exceeding
79 characters.  This is to improve readability in the code.

## TODO
* A basic REST api for reading the entire catalog is available.  Addition
api implementations need to be done
* Fix test comparisions related to Jinja encode/decode
* flask-wtf was used to auto-generate the form fields in the temple.
  However, this will be investigate as to whether manual generation of the
  template will provide greater flexibility and isolation between code
  and styling
