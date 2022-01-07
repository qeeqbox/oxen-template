from celery import Celery
from os import environ
from random import randint
from time import sleep
from json import load

json_settings = {}

with open('/shared/settings.json') as f:
    json_settings = load(f)

if not len(json_settings) > 0:
    exit()

CELERY = Celery(json_settings[environ["project_env"]]["celery_settings"]["name"],
                broker=json_settings[environ["project_env"]]["celery_settings"]["celery_broker_url"],
                backend=json_settings[environ["project_env"]]["celery_settings"]["celery_result_backend"])

while True:
    _task = CELERY.send_task(json_settings[environ["project_env"]]["worker"]["name"],args=[{"task":"{}".format(randint(1000000,2000000)),"privileged":True,"task_logic_timeout":10}],queue=json_settings[environ["project_env"]]["worker"]["queue"])
    sleep(randint(1,5))