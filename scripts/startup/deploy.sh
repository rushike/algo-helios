#!/bin/bash
sudo apt-get update
sudo apt-get install -y apache2 python3-pip python3-venv libapache2-mod-wsgi-py3 certbot python-certbot-apache python3-dev libpq-dev
sudo mkdir /var/www/algonauts.in
sudo mkdir /var/www/algonauts.in/log
sudo git -C /var/www/algonauts.in clone ${HELIOS_GIT_SOURCE} -b ${HELIOS_DEPLOYMENT_BRANCH}

# creating virtual environment
sudo echo "-e git+${ALGONAUTS_UTILS_GIT_SOURCE}@${ALGONAUTS_UTILS_GIT_BRANCH}#egg=algonautsutils" >> /var/www/algonauts.in/helios/requirements.txt
sudo python3 -m venv /var/www/algonauts.in/venv
sudo /var/www/algonauts.in/venv/bin/pip install wheel psycopg2
sudo /var/www/algonauts.in/venv/bin/pip install -r /var/www/algonauts.in/helios/requirements.txt

# creating db configuration
sudo sed -i "s/HELIOS_POSTGRES_DB/${HELIOS_POSTGRES_DB}/" /var/www/algonauts.in/helios/helios/settings/common.py
sudo sed -i "s/HELIOS_POSTGRES_USER/${HELIOS_POSTGRES_USER}/" /var/www/algonauts.in/helios/helios/settings/common.py
sudo sed -i "s/HELIOS_POSTGRES_PASSWORD/${HELIOS_POSTGRES_PASSWORD}/" /var/www/algonauts.in/helios/helios/settings/common.py
sudo sed -i "s/HELIOS_POSTGRES_HOST/${HELIOS_POSTGRES_HOST}/" /var/www/algonauts.in/helios/helios/settings/common.py

# doing django migrate and enabling apache configuration
sudo /var/www/algonauts.in/venv/bin/python /var/www/algonauts.in/helios/manage.py migrate
sudo /var/www/algonauts.in/venv/bin/python /var/www/algonauts.in/helios/manage.py collectstatic
sudo cp /var/www/algonauts.in/helios/scripts/apache_helios.conf /etc/apache2/sites-available/apache_helios.conf

# restarting apache
sudo a2ensite apache_helios.conf
sudo a2dissite 000-default.conf
sudo service apache2 restart

# enabling certbot for ssl
sudo certbot --apache --domains ${HELIOS_DOMAIN_NAME} --email ${HELIOS_SSL_EMAIL} --agree-tos --non-interactive --redirect
