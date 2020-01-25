FROM python:3.7

ADD requirements.txt .
RUN pip install -r requirements.txt

RUN pip install psycopg2
ENV AIRFLOW_HOME='/usr/local/airflow'
ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN='postgresql://airflow:airflow@postgres/airflow'

WORKDIR /usr/local/airflow
