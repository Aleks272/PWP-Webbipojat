FROM nginx:alpine

COPY ./nginx.conf /etc/nginx/nginx.conf
RUN adduser --no-create-home --system www-data
USER www-data
EXPOSE 80