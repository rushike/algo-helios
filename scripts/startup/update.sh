#!/bin/bash
sudo rm -rf /var/www/algonauts.in/helios
sudo git -C /var/www/algonauts.in clone ${HELIOS_GIT_SOURCE} -b ${HELIOS_DEPLOYMENT_BRANCH}

# Adding algonauts utils to requirements.txt
echo "-e git+${ALGONAUTS_UTILS_GIT_SOURCE}@${ALGONAUTS_UTILS_GIT_BRANCH}#egg=algonautsutils" >> /var/www/algonauts.in/janus/configs/requirements.txt
sudo /var/www/algonauts.in/venv/bin/pip install wheel psycopg2
sudo /var/www/algonauts.in/venv/bin/pip install -r /var/www/algonauts.in/helios/requirements.txt

# creating db configuration
sudo sed -i "s/HELIOS_POSTGRES_DB/${HELIOS_POSTGRES_DB}/" /var/www/algonauts.in/helios/helios/settings/common.py
sudo sed -i "s/HELIOS_POSTGRES_USER/${HELIOS_POSTGRES_USER}/" /var/www/algonauts.in/helios/helios/settings/common.py
sudo sed -i "s/HELIOS_POSTGRES_PASSWORD/${HELIOS_POSTGRES_PASSWORD}/" /var/www/algonauts.in/helios/helios/settings/common.py
sudo sed -i "s/HELIOS_POSTGRES_HOST/${HELIOS_POSTGRES_HOST}/" /var/www/algonauts.in/helios/helios/settings/common.py

# using django migrate and restarting apache
sudo /var/www/algonauts.in/venv/bin/python /var/www/algonauts.in/helios/manage.py migrate
sudo /var/www/algonauts.in/venv/bin/python /var/www/algonauts.in/helios/manage.py collectstatic
sudo service apache2 restart
