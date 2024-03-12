FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY main.py /code/
COPY requirements.txt /code/
COPY myway /code/myway
RUN apt-get update
RUN apt-get -y install gettext dos2unix
RUN pip install -r requirements.txt
COPY boot.sh /code/
RUN dos2unix -o /code/boot.sh
CMD /code/boot.sh