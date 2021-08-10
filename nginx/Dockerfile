# формирование образа на базе официального образа с Dockerhub - nginx:1.19.0-alpine
FROM nginx:1.19.6-alpine

# удаляем из контейнера дефолтный файл конфигурации Web-сервера
RUN rm /etc/nginx/conf.d/default.conf
# копируем конфигурационный файл (nginx.conf) в контейнер
COPY default.conf /etc/nginx/conf.d
