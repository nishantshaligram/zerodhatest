FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /backend

COPY requirements.txt /backend/
RUN pip install -r requirements.txt

# Install cron
RUN apt-get -y update && apt-get install -y cron 
# RUN crontab <<< '# new crontab'
# RUN service cron start
#install chrome

# We need wget to set up the PPA and xvfb to have a virtual screen and unzip to install the Chromedriver
RUN apt-get install -y wget xvfb unzip

# Set up the Chrome PPA
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Update the package list and install chrome
RUN apt-get update -y
RUN apt-get install -y google-chrome-stable

# Set up Chromedriver Environment variables
ENV CHROMEDRIVER_VERSION 2.19
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR

# Download and install Chromedriver
RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

# Put Chromedriver into the PATH
ENV PATH $CHROMEDRIVER_DIR:$PATH

COPY . /backend/
# CMD "service cron start && python manage.py crontab add && python manage.py runserver 0.0.0.0:8000"
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]