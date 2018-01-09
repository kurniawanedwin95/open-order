# open-order
Displays lists of currently received order, currently processed order, and production output

Uses Python 2.7, Django 1.11.7

Don't forget to apt-get install "libmysqlclient-dev" and pip install "mysql-python" and "sqlparse" if running migration asks for "did you install MySQLdb or whatever"

----------------------------------------------------------------------------------------
if this error appears "ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)"
do the following:
1) Stop the mysql demon process using this command :

sudo /etc/init.d/mysql stop
2) Start the mysqld demon process using the --skip-grant-tables option with this command

sudo /usr/sbin/mysqld --skip-grant-tables --skip-networking &

ANOTHER METHOD:

sudo mysqld_safe

-----------------------------------------------------------------------------------------

Start by running "python manage.py runserver"

Comments are written in Indonesian
