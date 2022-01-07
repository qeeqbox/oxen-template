'''
    __G__ = "(G)bd249ce4"
    backend -> worker
'''

from os import environ
from time import sleep
from docker import from_env
from binascii import hexlify
from pickle import dumps as pdumps
from celery import Celery
from logger import cancel_task_logger, log_string, setup_task_logger
from json import load

json_settings = {}

with open('/shared/settings.json') as f:
    json_settings = load(f)

if not len(json_settings) > 0:
    exit()

DOCKER_CLIENT = from_env()
CELERY = Celery(json_settings[environ["project_env"]]["celery_settings"]["name"],
                broker=json_settings[environ["project_env"]]["celery_settings"]["celery_broker_url"],
                backend=json_settings[environ["project_env"]]["celery_settings"]["celery_result_backend"])

CELERY.conf.update(
    CELERY_ACCEPT_CONTENT=["json"],
    CELERY_TASK_SERIALIZER="json",
    CELERY_RESULT_SERIALIZER="json",
    CELERY_TIMEZONE="America/Los_Angeles"
)

def clean_up():
    for container in DOCKER_CLIENT.containers.list():
        if "oxen_box" in container.name:
            container.stop()

@CELERY.task(bind=True, name=json_settings[environ["project_env"]]["worker"]["name"], queue=json_settings[environ["project_env"]]["worker"]["queue"], soft_time_limit=json_settings[environ["project_env"]]["worker"]["overall_task_time_limit"], time_limit=json_settings[environ["project_env"]]["worker"]["overall_task_time_limit"] + 10, max_retries=0, default_retry_delay=5)
def start_task(self, options):
    log_string(str(options), task=options['task'])
    setup_task_logger(options)
    temp_container = None
    try:
        temp_container = DOCKER_CLIENT.containers.run("oxen_box", command=[hexlify(pdumps(options)).decode()], volumes={json_settings[environ["project_env"]]["output_folder"]: {'bind': json_settings[environ["project_env"]]["task_logs"]["box_output"], 'mode': 'rw'}}, detach=True, network=json_settings[environ["project_env"]]["docker_network"], privileged=options['privileged'])
        temp_logs = ""
        counter = 0
        temp_logs_list = []
        for item in range(1, options['task_logic_timeout']):
            temp_logs = temp_container.logs()
            if len(temp_logs) > 1:
                if len(temp_logs.split(b"\n")) > counter:
                    if counter == 0:
                        temp_logs_list = temp_logs.split(b"\n")[counter:]
                    else:
                        temp_logs_list = temp_logs.split(b"\n")[counter-1:]
                    for item in temp_logs_list:
                        counter += 1
                        if len(item) > 0:
                            log_string(item.decode("utf-8"), task=options['task'])
            if temp_logs.endswith(b"Done!!\n"):
                break
            sleep(1)
        temp_container.stop()
        log_string("Parsing output", task=options['task'])
    except Exception as e:
        log_string("Error -> {}".format(e), task=options['task'])
    try:
        if temp_container is not None:
            temp_container.stop()
            temp_container.remove()
    except Exception as e:
        log_string("Error -> {}".format(e), task=options['task'])
    cancel_task_logger(options)