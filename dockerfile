FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

# ENV FLASK_APP /app/server.py

EXPOSE 8080

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

# FROM golang:latest AS build
# WORKDIR /app
# COPY . .
# RUN go build -o app .

# FROM ubuntu AS bin
# COPY --from=build /app/app /
# EXPOSE 8080
# CMD ["./app"]