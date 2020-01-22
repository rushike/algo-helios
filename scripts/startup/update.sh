#!/bin/bash
sudo rm -rf /var/www/algonauts.in/helios
sudo git -C /var/www/algonauts.in clone ${HELIOS_GIT_SOURCE} -b ${HELIOS_DEPLOYMENT_BRANCH}
sudo /var/www/algonauts.in/venv/bin/pip install psycopg2
sudo /var/www/algonauts.in/venv/bin/pip install -r /var/www/algonauts.in/helios/requirements.txt
sudo /var/www/algonauts.in/venv/bin/python /var/www/algonauts.in/helios/manage.py migrate
sudo service apache2 restart
