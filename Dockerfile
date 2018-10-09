FROM python:2.7-alpine

WORKDIR /gsuite

COPY ./ /gsuite/

RUN pip install -r requirements.txt

CMD ["python", "app.py"]