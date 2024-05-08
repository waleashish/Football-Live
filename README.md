# Football-Live
Live football updates application

## Streamlit in docker
Prerequisites:

Add a `.env` in the root directory where `docker-compose.yaml` is located. The `.env` file contains authorization information needed to connect to postgres database and football-org api. Please take a look at sample file provided at the mentioned location.

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