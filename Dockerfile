FROM alpine:3.14

RUN apk add --update --no-cache \
    curl \
    bash \
    nginx \
    python3 \
    py3-pip \
    py3-virtualenv \
    postgresql-dev \
    musl-dev \
    python3-dev \
    linux-headers \
    gcc

# add user and create app
RUN adduser -D server
RUN mkdir /home/app/ && chown -R server:server /home/app
RUN mkdir -p /var/log/email-bot && touch /var/log/email-bot/email-bot.err.log && touch /var/log/email-bot/email-bot.out.log
RUN chown -R server:server /var/log/email-bot
RUN chown -RL server:server /var/lib/nginx
WORKDIR /home/app

# copy all the files to the container
COPY --chown=server:server nginx.conf /etc/nginx/nginx.conf
COPY --chown=server:server .pgpass /home/app/.pgpass
RUN chmod 600 /home/app/.pgpass
COPY --chown=server:server . .

# venv
ENV VIRTUAL_ENV=/home/app/venv
USER server

# python setup
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# define the port number the container should expose
EXPOSE 5000

STOPSIGNAL SIGQUIT

CMD ["bash", "start.sh"]