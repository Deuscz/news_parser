FROM node:16.13.1-alpine

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install -g --silent
RUN npm install react-scripts@5.0.0 -g --silent
RUN npm install -g serve


# FROM node:16.13.1-alpine as build

# # set working directory
# WORKDIR /app

# # add `/app/node_modules/.bin` to $PATH
# ENV PATH /app/node_modules/.bin:$PATH

# # install app dependencies
# COPY package.json ./
# COPY package-lock.json ./
# RUN npm install -g --silent
# RUN npm install react-scripts@5.0.0 -g --silent
# RUN npm install -g serve
# COPY . ./
# RUN npm run build

# FROM nginx:stable-alpine
# COPY --from=build /app/build /usr/share/nginx/html

# COPY .nginx.default.conf /etc/nginx/conf.d/default.conf
