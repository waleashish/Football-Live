# Football-Live
Live football updates application

## Prerequisites:

The application needs `docker compose` installed at the host machine. Everything else will be handled by the containers created after installing the application.

The application uses APIs provided by [football-data.org](https://www.football-data.org/) To create an API key, go to the above URL and register to get free, rate-limited API key.
You are free to get the premium membership for rate-unlimited access too. There is no change in the code for this. You can modify the `seed_tables_data.py` file located inside `installation/populate_tables` and get rid of the 60 sec wait time if you have rate-unlimited API access.

## Streamlit in docker

First, clone the repository at your local machine.

Add a `.env` file in the root directory where `docker-compose.yaml` is located. The `.env` file contains authorization information needed to connect to postgres database and football-data APIs. Please take a look at `.env.sample` file provided at the mentioned location.

To install the application:

```shell
sh install.sh
```

This will create the necessary containers (postgres, table population, etc.) and seed initial data
into the application.

To run the application server:
```shell
sh startup.sh
```

This will start the streamlit application at [http://0.0.0.0:8501](http://0.0.0.0:8501)


To stop the application server:
```shell
sh stopserver.sh
```

You can modify the code base to add additional functionalities. Feel free to fork :)