#!/bin/sh

set -e

nginx -t -c /etc/nginx/nginx01.conf
nginx -t -c /etc/nginx/nginx02.conf
nginx -t -c /etc/nginx/nginx03.conf

haproxy -c -f /usr/local/etc/haproxy/haproxy.cfg

nginx -c /etc/nginx/nginx01.conf
nginx -c /etc/nginx/nginx02.conf
nginx -c /etc/nginx/nginx03.conf

exec haproxy -W -f /usr/local/etc/haproxy/haproxy.cfg
