from sqlalchemy.ext.declarative import declarative_base

'''
Base needs to be globally defined so it can be used as a base class
for the ORM models
'''
Base = declarative_base()

# Session is the factory for SQLAlchemy sessions.  It's created in the
# Model init_app() function
Session = None