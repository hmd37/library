run:
	cd library && py manage.py runserver

migrate:
	cd library && py manage.py makemigrations 
	timeout 1
	cd library && py manage.py migrate

test:
	cd library && py manage.py test
