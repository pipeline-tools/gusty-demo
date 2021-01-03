This is a demo of how the [gusty package](https://github.com/chriscardillo/gusty) works with [Airflow](https://airflow.apache.org/) to assist in the organization, construction, and management of DAGs, tasks, dependencies, and operators. It requires that you have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.

## Running the demo

Note: this demo takes some time to build, and a little effort up front. If you are in a hurry, please check out [gusty-demo-lite](https://github.com/chriscardillo/gusty-demo-lite).

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
DEFAULT_USER=your_username
DEFAULT_PASSWORD=your_password
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

### Explore

Airflow should be available for you at `localhost:8080`. You can log in with the `DEFAULT_USER` and `DEFAULT_PASSWORD` from your `.env`.

After you turn on the example DAGs and let them run, you can connect to the the containerized Postgres database with a URI akin to `postgresql://DEFAULT_USER:DEFAULT_PASSWORD@localhost:5678/datawarehouse`. A reminder all tables are housed under the schema `views`.

Please feel free to create issues, or fork and use to start your own gusty pipeline. Your feedback is very important. Hope you consider using gusty in your data pipeline projects.
