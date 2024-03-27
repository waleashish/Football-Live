# Football-Live
Live football updates application

## Streamlit in docker
Prerequisites:

Add files named `.env` and `credentials.json` at /config/ directory. The files contain authorization information needed to run streamlit. Please take a look at sample files provided at the mentioned location.

To build the application:
```shell
docker build -t football-live .
```

To run the application:
```shell
docker run -p 8501:8501 football-live  
```