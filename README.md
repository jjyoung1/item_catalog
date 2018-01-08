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

## URL Summary
* / - homepage of Catalog App
* /auth/gdisconnect - Disconnect from Google OAuth login session
* /auth/fbdisconnect - Disconnect from Facebook OAuth login session
* /auth/login - Login page
* /auth/logout - Logout of any existing login sessions
* /catalog - homepage of Catalog App (Alias for '/')
* /catalog/category/new - create new category
* /catalog/category/edit - modify existing category
* /catalog/\<category\>/edit - Create new item in category
* /catalog/\<category\>/delete - delete existing category
* /catalog/\<category\> - List items in specified category
* /catalog/\<category\>/item/new - Create new item in category
* /catalog/\<category\>/\<item\> - Item description
* /catalog/\<category\>/\<item\>/edit - Edit item
* /catalog/\<category\>/\<item\>/delete - Delete item confirmation
* /

## Executing Self Tests
Within the directory containing **catalog.py** execute the following:
* $ source venv/bin/activate
* $ export FLASK_APP=catalog.py
* $ export FLASK_COVERAGE=1
* $ export FLASK_DEBUG=1
* $ flask test

