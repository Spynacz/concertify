FROM node:latest

EXPOSE 3000
WORKDIR /frontend/

COPY package.json /frontend/package.json
RUN npm install

COPY src /frontend/src
COPY template.html /frontend/template.html
COPY babel.config.json /frontend/babel.config.json
COPY webpack.common.js /frontend/webpack.common.js
COPY webpack.dev.js /frontend/webpack.dev.js
COPY webpack.prod.js /frontend/webpack.prod.js

CMD ["npm", "start"]
