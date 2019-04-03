Running:
 1. ```cd fronted``` and run command ```npm install```
 2. create vevn with **python3** and run command ```pip install -r requirements.txt```
 3. run ```./manage.py migrate```
 4. run ```./manage.py runserver```
 5. run ```celery -A jelly_chat worket -l info```
 6. run ```uwsgi --http :8081 --gevent 100 --module websocket --gevent-monkey-patch --master --processes 4```
 7. run ```npm run dev```

Open the browser tab and go to localhost:8080