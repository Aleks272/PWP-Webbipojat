FROM nginx:alpine

COPY ./nginx.conf /etc/nginx/nginx.conf
# taken from https://github.com/UniOulu-Ubicomp-Programming-Courses/sensorhub-nginx-sidecar/blob/master/Dockerfile
# lines 4,5
RUN  chmod g+rwx /var/cache/nginx /var/run /var/log/nginx && \
     chown nginx:root /var/cache/nginx /var/run /var/log/nginx
USER nginx:root
EXPOSE 8080