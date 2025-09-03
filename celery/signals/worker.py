from config import app

if __name__ == '__main__':
    print("Starting Celery Worker...")
    app.worker_main(argv=['worker', '--loglevel=info'])
