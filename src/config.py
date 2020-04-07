import os

class BaseConfig:
	POSTGRES_SETTINGS = {
		'username': os.getenv('POSTGRES_USER', 'postgres'),
		'password': os.getenv('POSTGRES_PASSWORD', '0oBSTinatenEss#maRyl7uMbeL0@3162'),
		'database': os.getenv('POSTGRES_DATABASE', 'postgres'),
		'hostname': os.getenv('POSTGRES_HOSTNAME', 'postgres'),
		'port': os.getenv('POSTGRES_PORT', '5432')
	}

	AUDIT_DIR = os.path.abspath('../../adump/*.xml')