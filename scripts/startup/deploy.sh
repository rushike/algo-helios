#!/bin/bash
sudo apt-get update
sudo apt-get install -y apache2 python3-pip python3-venv libapache2-mod-wsgi-py3 certbot python-certbot-apache python3-dev libpq-dev
sudo mkdir /var/www/algonauts.in
sudo mkdir /var/www/algonauts.in/log
sudo git -C /var/www/algonauts.in clone ${HELIOS_GIT_SOURCE} -b ${HELIOS_DEPLOYMENT_BRANCH}
sudo python3 -m venv /var/www/algonauts.in/venv
sudo /var/www/algonauts.in/venv/bin/pip install wheel psycopg2
sudo /var/www/algonauts.in/venv/bin/pip install -r /var/www/algonauts.in/helios/requirements.txt
sudo /var/www/algonauts.in/venv/bin/python /var/www/algonauts.in/helios/manage.py migrate
sudo cp /var/www/algonauts.in/helios/scripts/apache_helios.conf /etc/apache2/sites-available/apache_helios.conf
sudo a2ensite apache_helios.conf
sudo a2dissite 000-default.conf
sudo service apache2 restart
sudo certbot --apache --domains ${HELIOS_DOMAIN_NAME} --email ${HELIOS_SSL_EMAIL} --agree-tos --non-interactive --redirect
