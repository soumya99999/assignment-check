open docker
docker start my-redis-server

cd assignment_checker_project
myenv\Scripts\activate
celery -A assignment_checker_project worker --loglevel=info --pool=solo

cd assignment_checker_project
myenv\Scripts\activate
python manage.py runserver


Frontend 

cd frontend
npm run dev