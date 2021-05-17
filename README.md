# fastapi-react-auth-app

Simple example of auth app which built on Fastapi + React.js


![Demo](https://github.com/Kel0/fastapi-react-auth-app/blob/master/demo/demo.gif)


## Installation
* **Copy repo.**
```shell
git clone https://github.com/Kel0/fastapi-react-auth-app.git
```

* **Install requires**
```shell
pip install -r ./backend/requirements.txt
```

* **Migrate models**
```shell
cd ./backend && inv migrate
```

* **Install react dependencies**
```shell
cd ./fronend && npm install
```

## Start app
* **Run api**
```shell
cd ./backend && uvicorn clubhouse.api:app --reload --port 5000
```

* **Run celery**
```shell
cd ./backend && celery -A clubhouse.tasks worker -B --loglevel=info
```

* **Run react**
```shell
cd ./frontend && npm start
```

## Start app via Docker
* **Run api**
```
docker-compose up -d --build
```
Api will run under 4150 port

* **Run react**
```shell
cd ./frontend && npm start
```