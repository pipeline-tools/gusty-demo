# Introduction

The purpose of this repo is to provide a jumping-off point for others to use Airflow to set up their own data pipelines without having to configure Airflow from scratch.

The `ez-airflow` project has a few opinions:

- Data pipelines empower data workers to do three things, two of which `ez-airflow` addresses:

    1. **Ingesting data** - Data is ingested from different sources, through the use of user-defined operators. Ideally, one operator should be built to interface with one data source. This data is then stored in a central data warehouse. Ideally, each data source is stored in its own schema.
    2. **Transforming data** - Once raw data is ingested, it can be manipulated and rendered into **views**. These views are currently generated using a user-defined SQL operator. (In time, it would be nice to build in Python and R operators that could generate views, as well.) These views are stored back into the data warehouse, and it is ideal if these tables are stored in a schema named `views`. (In time, it would be nice to build in export tasks, that could export views to other destinations, like AWS S3.)
    3. **Machine learning** - Once data has been formatted into views and stored, users should be able to run machine learning jobs to create predictive models meant for production needs. `ez-airflow` does not handle this yet.

