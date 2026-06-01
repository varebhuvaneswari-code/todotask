FROM python:3.13

WORKDIR /app
COPY ..
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

EXPOSE 10000

CMD ["gunicorn","to_do_task.wsgi:application","--bind","0.0.0.0:10000"]


