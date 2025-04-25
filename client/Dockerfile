FROM node:23-alpine3.20 AS builder
COPY . .
RUN npm install && \
    npm run build

FROM nginx:1.27.5-alpine
COPY --from=builder /dist /usr/share/nginx/html
COPY ./configs/nginx.conf /etc/nginx/nginx.conf
RUN chmod g+rwx /var/cache/nginx /var/run /var/log/nginx && \
    chown nginx:root /var/cache/nginx /var/run /var/log/nginx && \
    chown -R nginx:root /usr/share/nginx/html
EXPOSE 3000
USER nginx:root
CMD ["nginx", "-g", "daemon off;"]