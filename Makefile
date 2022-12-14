sub_arto:
	python manage.py subscribe_arto


install:
	pip install -r requirements.txt


migrate:
	python manage.py makemigrations
	python manage.py migrate


run:
	python manage.py runserver 0.0.0.0:4670


target: sub_arto run


pipe:
	make install
	pip uninstall argparse -y
	make migrate
	make -j2 target
