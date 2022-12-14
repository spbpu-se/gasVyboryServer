FROM python:3.9

ARG mongo_ip
ARG mongo_port

ENV mongo_ip=$mongo_ip
ENV mongo_port=$mongo_port

COPY . .
RUN  pip install -r ./requirements.txt

ENTRYPOINT ["python", "main.py"]
