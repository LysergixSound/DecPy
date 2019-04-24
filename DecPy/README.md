[*SETUP* Database #UBUNTU]
	- install mariadb server and client
		[TERMINAL] sudo apt -y install mariadb-server mariadb-client

	- login to MariaDB (try empty password as default)
		[TERMINAL] sudo mariadb -u root -p

	- change root password
		[MYSQL] use mysql
		[MYSQL] UPDATE mysql.user SET Password=PASSWORD('NEW-PASSWORD') WHERE User='root';
		[MYSQL] FLUSH PRIVILEGES;
		[MYSQL] exit

	- create database and user
		[TERMINAL] sudo mariadb -u root -p
		[MYSQL] create database statefree;
		[MYSQL] GRANT ALL PRIVILEGES ON statefree.* to USERNAME@'%' IDENTIFIED BY 'PASSWORD';
		[MYSQL] GRANT ALL PRIVILEGES ON statefree.* to USERNAME@'localhost' IDENTIFIED BY 'PASSWORD';
		[MYSQL] exit

	- create tables
		[TERMINAL] sudo mariadb -u USERNAME -p statefree
			[MYSQL] 
				CREATE TABLE data(
				id INT NOT NULL AUTO_INCREMENT,
				blockHash VARCHAR(255) NOT NULL,
				sender VARCHAR(255) NOT NULL,
				receiver VARCHAR(255) NOT NULL,
				message MEDIUMTEXT NOT NULL,
				proof INT NOT NULL,
				difficulty INT NOT NULL,
				expiration VARCHAR(255) NOT NULL,
				timestamp INT NOT NULL,
				PRIMARY KEY ( id )
				);
			[MYSQL] 
				CREATE TABLE neighbours(
				id INT NOT NULL AUTO_INCREMENT,
				alias VARCHAR(255) NOT NULL,
				address VARCHAR(255) NOT NULL,
				PRIMARY KEY ( id )
				);
			[MYSQL] exit

[*PYTHON* Dependencies]
	- pip install requests
	- pip install twisted
	- pip install klein
	- pip install mysql-connector
