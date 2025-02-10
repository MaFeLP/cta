FROM nginx:alpine

#COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY *.py *.html pyscript.toml /usr/share/nginx/html/

# Expose port 80 for HTTP traffic (default Nginx port)
EXPOSE 80
