# Creating image based on docker slim-buster python 3 image
FROM python:3.10.10-slim-buster
# Sets dumping log messages directly to stream instead of buffering
ENV PYTHONUNBUFFERED 1
# RUN mkdir /code
# WORKDIR /code
# Makes directory config in container and copies config/apprenticeship-backend directory's contents to the container's config directory

RUN mkdir /config
ADD config/declutter /config/
# need to add dependencies like GCC
# RUN apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev alpine-sdk
RUN apt-get update -y && apt-get install -y gcc && apt-get install -y python3-dev build-essential
RUN apt-get install -y default-libmysqlclient-dev


# need gcc to compile psycopg2
#RUN pip install psycopg2~=2.6
#RUN apt-get autoremove -y gcc
# ADD requirements.txt /code/
# Installing all python dependencies
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y default-mysql-client
RUN apt-get install -y awscli
RUN apt-get install -y poppler-utils


RUN pip3 install -r /config/requirements.txt
    # Open port 8000 to outside world
EXPOSE 8000
# ADD ./ /code/
# When container starts, this script will be executed.
# Note that it is NOT executed during building
# CMD ["chmod +x /config/on-container-start.sh", "sh", "/config/on-container-start.sh"]
CMD ["/bin/bash","-c","chmod +x /config/on-container-start.sh && /config/on-container-start.sh"]


# Creating and putting application inside container
# and setting it to working directory (meaning it is going to be default)
RUN mkdir /declutter
RUN mkdir /declutter/static
RUN mkdir /declutter/media
WORKDIR /declutter
ADD ./ /declutter/
RUN ls

#  CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]

