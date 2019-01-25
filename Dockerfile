FROM python:2.7-alpine

RUN apk add --update curl gcc g++

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

WORKDIR /gsuite

COPY ./ /gsuite/

RUN pip install -r requirements.txt

CMD ["python", "app.py"]