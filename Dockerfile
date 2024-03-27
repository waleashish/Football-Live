FROM python:3

RUN mkdir /app
WORKDIR /app

RUN pip install python-dotenv
RUN pip install pandas-gbq
RUN pip install tqdm
RUN pip install streamlit

COPY . /app/

ENTRYPOINT [ "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--theme.primaryColor=indigo" ]