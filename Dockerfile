FROM python:3.11-slim

RUN mkdir /service
WORKDIR /service

COPY . .

RUN python -m pip install --upgrade pip
RUN pip install pdm
RUN pdm self update
RUN pdm sync -v --global --project .

EXPOSE 8000
CMD uvicorn app.main:app --host=0.0.0.0 --port=8000
