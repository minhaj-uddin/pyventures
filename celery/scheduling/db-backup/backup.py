import os
import subprocess
import datetime

DB_TYPE = "postgres"
DB_NAME = "mydatabase"
DB_USER = "myuser"
DB_PASSWORD = "mypassword"
DB_HOST = "localhost"
BACKUP_DIR = "backups"

os.makedirs(BACKUP_DIR, exist_ok=True)


def generate_backup_filename():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return os.path.join(BACKUP_DIR, f"{DB_NAME}_backup_{timestamp}.sql.gz")


def run_backup():
    backup_file = generate_backup_filename()
    env = os.environ.copy()
    env["PGPASSWORD"] = DB_PASSWORD

    if DB_TYPE == "postgres":
        command = f"pg_dump -U {DB_USER} -h {DB_HOST} {DB_NAME} | gzip > {backup_file}"
    elif DB_TYPE == "mysql":
        command = f"mysqldump -u{DB_USER} -p{DB_PASSWORD} -h {DB_HOST} {DB_NAME} | gzip > {backup_file}"
    else:
        raise ValueError("Unsupported DB_TYPE. Use 'postgres' or 'mysql'.")

    subprocess.run(command, shell=True, env=env, check=True)
    return backup_file
