pkill gunicorn
gunicorn -D -b 0.0.0.0:5000 --log-level=DEBUG run:fantasticsearch --reload
