FROM python:alpine3.19

COPY requirements.txt /requirements.txt
RUN apk --no-cache add --virtual build-dependencies build-base gcc libc-dev libffi-dev mariadb-dev
RUN pip3 install --upgrade -r /requirements.txt
COPY . /crud-app
WORKDIR /crud-app

EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD [ "__main__.py"]