# build stage
FROM node:lts-alpine as build-stage

# install simple http server for serving static content
RUN npm install -g http-server
# make the 'app' folder the current working directory
WORKDIR /frontend
# copy both 'package.json' and 'package-lock.json'
COPY package*.json /frontend/
# install project dependencies
RUN npm install
# copy project files and folders to the current working directory
COPY . /frontend/

# build app for production with minification
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /frontend/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]