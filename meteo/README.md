#Meteo

Comment fait-il à UrLab ? Ce projet est intimement lié à UrLab/HAL, qui envoie
les données à cette application par une queue RabbitMQ.

## Setup
Il faut un serveur RabbitMQ quelque part.

`cp config.py.example config.py`; 
remplir config.py avec le bon user, pass, host, vhost RabbitMQ.

Ensuite `manage.py feed_meteo`.
