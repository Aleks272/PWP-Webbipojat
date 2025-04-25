FROM nginx:alpine

COPY ./nginx.conf /etc/nginx/nginx.conf
RUN adduser --no-create-home --system www-data && \
    chown www-data:www-data /var/cache/nginx /var/log/nginx /var/run
USER www-data
EXPOSE 80