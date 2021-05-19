FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Install cron
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y cron
RUN crontab <<< '# new crontab'

COPY . /app/

CMD python manage.py runserver 0.0.0.0:8000