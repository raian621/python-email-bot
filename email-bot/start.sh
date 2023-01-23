#!/bin/bash

# start nginx in the background
nginx -g 'daemon off;'&

# start uwsgi server using uwsgi.ini file
uwsgi uwsgi.ini