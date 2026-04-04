web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.api:app --bind 0.0.0.0:$PORT
pipeline-runner: python main.py pipeline --loop
