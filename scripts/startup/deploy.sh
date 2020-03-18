#!/bin/bash
apt-get update
apt-get install -y apache2 python3-pip python3-venv libapache2-mod-wsgi-py3 certbot python-certbot-apache python3-dev libpq-dev
mkdir /var/www/algonauts.in
mkdir /var/www/algonauts.in/log
git -C /var/www/algonauts.in clone ${HELIOS_GIT_SOURCE} -b ${HELIOS_DEPLOYMENT_BRANCH}

# creating virtual environment
echo "-e git+${ALGONAUTS_UTILS_GIT_SOURCE}@${ALGONAUTS_UTILS_GIT_BRANCH}#egg=algonautsutils" >> /var/www/algonauts.in/helios/requirements.txt
python3 -m venv /var/www/algonauts.in/venv
/var/www/algonauts.in/venv/bin/pip install wheel psycopg2
/var/www/algonauts.in/venv/bin/pip install -r /var/www/algonauts.in/helios/requirements.txt

# creating db configuration
sed -i "s/HELIOS_POSTGRES_DB/${HELIOS_POSTGRES_DB}/" /var/www/algonauts.in/helios/helios/settings/common.py
sed -i "s/HELIOS_POSTGRES_USER/${HELIOS_POSTGRES_USER}/" /var/www/algonauts.in/helios/helios/settings/common.py
sed -i "s/HELIOS_POSTGRES_PASSWORD/${HELIOS_POSTGRES_PASSWORD}/" /var/www/algonauts.in/helios/helios/settings/common.py
sed -i "s/HELIOS_POSTGRES_HOST/${HELIOS_POSTGRES_HOST}/" /var/www/algonauts.in/helios/helios/settings/common.py

# doing django migrate and enabling apache configuration
/var/www/algonauts.in/venv/bin/python /var/www/algonauts.in/helios/manage.py migrate
/var/www/algonauts.in/venv/bin/python /var/www/algonauts.in/helios/manage.py collectstatic
cp /var/www/algonauts.in/helios/scripts/apache_helios.conf /etc/apache2/sites-available/apache_helios.conf

# restarting apache
a2ensite apache_helios.conf
a2dissite 000-default.conf
service apache2 restart

# enabling certbot for ssl
certbot --apache --domains ${HELIOS_DOMAIN_NAME} --email ${HELIOS_SSL_EMAIL} --agree-tos --non-interactive --redirect
