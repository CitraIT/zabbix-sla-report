FROM nginx


RUN mkdir -p /vol/app

# RUN /usr/bin rm -rf /etc/nginx/conf.d/default.conf
# COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

VOLUME /vol/app