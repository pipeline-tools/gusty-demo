This is a demo of how the [gusty package](https://github.com/chriscardillo/gusty) works with [Airflow](https://airflow.apache.org/) to assist in the organization, construction, and management of DAGs, tasks, dependencies, and operators.

## Running the demo

### Generate secrets

Using the `cryptography` package, generate Fernet keys using the following line. (You will need two)

```
from cryptography.fernet import Fernet
Fernet.generate_key().decode()
```

These keys will be used to encrypt passwords in our connections, and power the Airflow webserver.

### Create a .env

Save the generated keys and a default user/password in a `.env` file in the same directory as your `docker-compose.yml`. The `.env` file should look like this:

```
DEFAULT_USER='your_username'
DEFAULT_PASSWORD='your_password'
FERNET_KEY='a_fernet_key'
SECRET_KEY='another_fernet_key'
```

### Build and run

Build with the following (this may take some time):

```
docker-compose build
```

Then run with the following:

```
docker-compose up
```
