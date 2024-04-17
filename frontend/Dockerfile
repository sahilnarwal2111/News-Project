#node block
FROM node:16.17.1-buster-slim as nodework
WORKDIR /myapp
COPY package.json .
RUN npm install
COPY . .
RUN npm run build

#nginx block
FROM nginx:alpine 
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=nodework /myapp/build .
ENTRYPOINT ["nginx", "-g", "daemon off;"]
