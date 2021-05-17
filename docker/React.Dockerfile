FROM node:current as builder

# set working directory
WORKDIR /app
EXPOSE 3150

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH


COPY ./frontend/package.json ./
COPY ./frontend/package-lock.json ./

RUN ls -l

RUN npm install
# RUN npm run build

COPY ./frontend/ ./

RUN ls -l

CMD npm run build


FROM nginx:stable-alpine
COPY --from=builder /app /usr/share/nginx/html
EXPOSE 3150
CMD ["nginx", "-g", "daemon off;"]    