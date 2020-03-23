FROM python:2.7.15-jessie

WORKDIR /gsuite

COPY ./ /gsuite/

RUN pip install -r requirements.txt

CMD ["python", "-u", "app.py"]
