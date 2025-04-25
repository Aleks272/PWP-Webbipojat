FROM node:23-alpine3.20 AS builder
COPY . .
RUN npm install && \
    npm run build

FROM nginx:1.27.5-alpine
COPY --from=builder /dist /usr/share/nginx/html
COPY ./configs/nginx.conf /etc/nginx/nginx.conf
RUN adduser --no-create-home --system www-data && \
    chown -R www-data /usr/share/nginx/html
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]