FROM nginx:alpine

WORKDIR /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf
COPY public/ .

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
