FROM node:latest

EXPOSE 3000
WORKDIR /react/

COPY package.json /react/package.json
RUN npm install

COPY src /react/src
COPY template.html /react/template.html
COPY babel.config.json /react/babel.config.json
COPY webpack.common.js /react/webpack.common.js
COPY webpack.dev.js /react/webpack.dev.js
COPY webpack.prod.js /react/webpack.prod.js

CMD ["npm", "start"]
