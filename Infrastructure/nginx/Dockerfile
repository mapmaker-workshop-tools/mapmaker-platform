# This needs to be run from the root directory as you want to call files from mapmaker/static
# to do so use this build command:
# docker build -t nginx:latest -f Infrastructure/nginx/Dockerfile .

FROM nginx:1-alpine
# Adding temp file for cache
RUN mkdir /tmp/nginx

#Adding Django Static files into nginx so they dont have to be answered by Django
COPY src/staticfiles/ ./static
COPY src/staticfiles/ ./staticfiles
#Specific settings so nginx works as a reverse proxy
COPY Infrastructure/nginx/default.conf ./etc/nginx/conf.d/default.conf

EXPOSE 80
