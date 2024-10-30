# from celery import shared_task
# from django.core.management import call_command
#
# @shared_task
# def run_management_command(command):
#     try:
#         call_command(command)  # Execute the command
#     except Exception as e:
#         raise Exception(f"Error executing command {command}: {str(e)}")
