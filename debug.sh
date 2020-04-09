export FLASK_DEBUG=1
export FLASK_ENV=development
export FLASK_APP=njmon
export PYTHONPATH=/home/frank/njmon/njmon
#nohup gunicorn njmin:app > log/log.txt &

flask run
