# myapp/tasks.py
from celery import shared_task
from django.core.management import call_command

@shared_task
def run_command_task(command):
    call_command(command)
    return f"{command} executed successfully."
