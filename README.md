# item_catalog
Catalog app to manage item categories and items.  Implements both Web
and Restful interfaces

## Startup
Execute catalog.py to start program

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

## Testing
### Environment Variables to be set
* FLASK_APP=catalog.py
* FLASK_COVERAGE=1
* FLASK_DEBUG=1

### Execution of Tests
Within the directory containing **catalog.py** execute:

*flask test*

