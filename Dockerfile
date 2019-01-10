FROM python:3.6
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY . /crud-app
WORKDIR /crud-app

EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD [ "__main__.py"]