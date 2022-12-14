FROM python:3.9

ARG mongo_ip
ARG mongo_port
ARG mongo_usr
ARG mongo_pwd
ARG kafka_port

ENV mongo_ip=$mongo_ip
ENV mongo_port=$mongo_port
ENV mongo_usr=$mongo_usr
ENV mongo_pwd=$mongo_pwd
ENV kafka_port=$kafka_port

COPY . .
RUN  pip install -r ./requirements.txt

ENTRYPOINT ["python", "consumer.py"]
