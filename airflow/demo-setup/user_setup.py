import os
import sqlalchemy
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser

session = settings.Session()
users = session.query(PasswordUser).all()

if len(users) == 0:
    default_user_info = sqlalchemy.create_engine(os.environ['AIRFLOW__CORE__SQL_ALCHEMY_CONN'])

    default_user = PasswordUser(models.User())
    default_user.username = default_user_info.url.username
    default_user.password = default_user_info.url.password
    default_user.email = 'fake@email.com'
    default_user.superuser = True

    session.add(default_user)
    session.commit()

session.close()
