FROM python:3.8-slim

LABEL description="Dockerfile"


COPY . .

RUN pip3 install -r requirements

EXPOSE 5000

CMD ["python", "web.py"]
