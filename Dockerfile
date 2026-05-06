FROM python:3.14-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache --virtual .build-requirements gcc musl-dev \
    && apk del .build-requirements

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn" ,"app.main:app","--reload","--host", "0.0.0.0","--port","8000"]