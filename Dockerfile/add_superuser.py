from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
from sqlalchemy.exc import IntegrityError

user = PasswordUser(models.User())
user.username = 'test'
user.email = 'test@someone.org'
user.password = 'test'
user.superuser= True
session = settings.Session()
session.add(user)
try:
    session.commit()
except IntegrityError:
    pass
finally:
    session.close()
