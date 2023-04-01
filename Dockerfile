FROM python:3.10-alpine as build

RUN apk add --no-cache --virtual .build-deps gcc g++ musl-dev
RUN apk add --no-cache ffmpeg

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.10-alpine

RUN apk add --no-cache ffmpeg

COPY --from=build /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

WORKDIR /app

COPY . .

EXPOSE 8000

ENV NAME World

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

