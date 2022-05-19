FROM python:3.8

WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y default-libmysqlclient-dev
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
RUN chmod +x start.sh

EXPOSE 5000
ENTRYPOINT ["./start.sh"]