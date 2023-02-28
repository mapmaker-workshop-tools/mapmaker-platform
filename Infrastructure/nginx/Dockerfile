# This needs to be run from the root directory as you want to call files from src/static
# to do so use this build command: 
# docker build -t nginx:latest -f Infrastructure/nginx/Dockerfile .

FROM nginx:1.19.0-alpine

COPY static .kaartenmaker.nl/static
COPY kaartenmaker.nl ./kaartenmaker.nl
COPY kaartenmaker.nl/static ./static
COPY Infrastructure/nginx/default.conf ./etc/nginx/conf.d/default.conf

EXPOSE 80
