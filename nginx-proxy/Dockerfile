FROM nginx:alpine

COPY ./nginx.conf /etc/nginx/nginx.conf
RUN  chmod g+rwx /var/cache/nginx /var/run /var/log/nginx && \
     chown nginx:root /var/cache/nginx /var/run /var/log/nginx
USER nginx:root
EXPOSE 8080