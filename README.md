# indicadores
Indicadores de gestión

Una vez abierto la base de datos, el archivo populate, la carga
con un set de datos inicial

Ejecución:
Para ejecutar se necesita py solver.py
El .pbix debería encontrar el .db: Para que esto suceda hay que instalarse un driver que permita al powerbi conectarse con el sqlite a través de una conexión odbc.  Esta última debe crearse con un dsn

para conteinizar:
Sacar pywin32==301 del requirements.txt

docker build --tag python-docker .
docker run -d -p 5000:5000 --name powerMyKpi python-docker


Create volume for mysql
$ docker volume create mysql
$ docker volume create mysql_config

Create a network
docker network create mysqlnet

docker run --rm -d -v mysql:/var/lib/mysql -v mysql_config:/etc/mysql -p 3306:3306 --network mysqlnet --name mysqldb -e MYSQL_ROOT_PASSWORD=p@ssw0rd1 mysql

docker exec -ti mysqldb mysql -u root -p

Correr el contenedor junto a la base de datos

docker run --rm -d --network mysqlnet --name rest-server -p 5000:5000  python-docker-dev


para usar composer.. 
docker-compose -f docker-compose.dev.yml up --build
