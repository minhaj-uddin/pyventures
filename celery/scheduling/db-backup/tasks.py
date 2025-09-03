import logging
from app import app
from backup import run_backup


@app.task
def backup_database():
    try:
        backup_path = run_backup()
        logging.info(f"✅ Backup successful: {backup_path}")
        return f"Backup saved to: {backup_path}"
    except Exception as e:
        logging.error(f"❌ Backup failed: {str(e)}")
        raise
