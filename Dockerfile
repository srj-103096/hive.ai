FROM mkassaian/docker-challenge

COPY nginx01.conf /etc/nginx/nginx01.conf
COPY nginx02.conf /etc/nginx/nginx02.conf
COPY nginx03.conf /etc/nginx/nginx03.conf

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg

COPY index.html /var/www/html/index.html

COPY entrypoint.sh /entrypoint.sh
COPY solution.txt /solution.txt

RUN chmod +x /entrypoint.sh

CMD ["/bin/sh", "/entrypoint.sh"]
