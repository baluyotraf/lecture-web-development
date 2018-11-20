# AdU Online Technology Project

## Installation Instructions

1.   Clone the repository using the following command ```git clone https://github.com/baluyotraf/AdU_Online_Tech.git```
2.   Go the cloned folder and run the containers using ```docker-compose up -d --build```. Wait for a few minutes so that the mysql container can create the database
3.   Initialize the backend tables by running ```docker-compose exec backend python manage.py create-db```
4.   Visit the website on ```localhost``` on native docker installation or on ```192.168.99.100``` on docker toolbox installation
