FROM node:14.17 as build-stage

RUN npm install -g http-server

WORKDIR /app

COPY package*.json ./

RUN npm install --verbose

COPY . .

RUN npm run lint -- --fix && npm run build


# Preparing production Docker container

FROM nginx:stable-alpine

COPY --from=build-stage /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
