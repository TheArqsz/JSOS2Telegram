FROM python:3.8-slim AS builder

RUN apt-get update

RUN apt-get install -y --no-install-recommends build-essential gcc

RUN useradd -ms /bin/false user

USER user

RUN python -m venv /home/user/venv

ENV PATH="/home/user/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install -r requirements.txt

FROM ubuntu AS build-image

RUN apt-get update && apt-get install -y firefox firefox-geckodriver python3 python3-dev

RUN ln -s /usr/bin/python3 /usr/local/bin/python

RUN useradd -ms /bin/false user

COPY --from=builder /home/user/venv /home/user/venv

USER user

WORKDIR /app

COPY . /app

ENV PATH="/home/user/venv/bin:$PATH"

ENTRYPOINT ["python", "jsos2telegram.py"]

CMD ["-h"]