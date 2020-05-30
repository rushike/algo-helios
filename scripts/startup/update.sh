#!/bin/bash
rm -rf /var/www/algonauts.in/helios
git -C /var/www/algonauts.in clone ${HELIOS_GIT_SOURCE} -b ${HELIOS_DEPLOYMENT_BRANCH}

# Adding algonauts utils to requirements.txt
echo "-e git+${ALGONAUTS_UTILS_GIT_SOURCE}@${ALGONAUTS_UTILS_GIT_BRANCH}#egg=algonautsutils" >> /var/www/algonauts.in/helios/requirements.txt
/var/www/algonauts.in/venv/bin/pip install wheel psycopg2
/var/www/algonauts.in/venv/bin/pip install -r /var/www/algonauts.in/helios/requirements.txt

# creating db configuration
sed -i "s/HELIOS_POSTGRES_DB/${HELIOS_POSTGRES_DB}/" /var/www/algonauts.in/helios/helios/settings/common.py
sed -i "s/HELIOS_POSTGRES_USER/${HELIOS_POSTGRES_USER}/" /var/www/algonauts.in/helios/helios/settings/common.py
sed -i "s/HELIOS_POSTGRES_PASSWORD/${HELIOS_POSTGRES_PASSWORD}/" /var/www/algonauts.in/helios/helios/settings/common.py
sed -i "s/HELIOS_POSTGRES_HOST/${HELIOS_POSTGRES_HOST}/" /var/www/algonauts.in/helios/helios/settings/common.py

# using django migrate and restarting apache
/var/www/algonauts.in/venv/bin/python /var/www/algonauts.in/helios/manage.py migrate
/var/www/algonauts.in/venv/bin/python /var/www/algonauts.in/helios/manage.py collectstatic
service apache2 restart
