FROM cypress/included:13.6.0

WORKDIR /app

COPY package.json .
COPY cypress.config.js .

RUN npm install

COPY cypress ./cypress

CMD ["npm", "run", "test"]