FROM python:3.10-slim

WORKDIR /app

ENV PYTHONPATH=/app/src
ENV GECKODRIVER_VER v0.33.0
ENV FIREFOX_VER 87.0

# Install required packages for selenium
RUN set -x \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
        firefox-esr \
    && apt-get install -y \
        curl \
    && apt-get install -y \
        bzip2 

# Add latest FireFox
RUN set -x \
    && apt install -y \
        libx11-xcb1 \
        libdbus-glib-1-2 \
    && curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VER}/linux-x86_64/en-US/firefox-${FIREFOX_VER}.tar.bz2 \
    && tar -jxf firefox-* \
    && mv firefox /opt/ \
    && chmod 755 /opt/firefox \
    && chmod 755 /opt/firefox/firefox

# Add geckodriver
RUN set -x \
    && curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
    && tar zxf geckodriver-*.tar.gz \
    && mv geckodriver /usr/bin/

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]