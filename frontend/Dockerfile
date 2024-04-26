FROM node:latest

EXPOSE 3000
WORKDIR /frontend/

COPY package.json /frontend/package.json
RUN npm install

COPY webpack.common.js /frontend/webpack.common.js
COPY webpack.dev.js /frontend/webpack.dev.js
COPY webpack.prod.js /frontend/webpack.prod.js
COPY babel.config.json /frontend/babel.config.json
COPY template.html /frontend/template.html
COPY src /frontend/src

CMD ["npm", "start"]
