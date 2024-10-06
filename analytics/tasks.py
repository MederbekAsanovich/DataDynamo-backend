# Incorrect (causes the ImportError):
# from datadynamo.celery import shared_task

# Correct:
from celery import shared_task
from .models import DataAnalysisTask

@shared_task
def process_data_task(task_id):
    task = DataAnalysisTask.objects.get(id=task_id)
    task.start_task()

    # Simulate data processing (replace with real logic)
    result = f"Data processed for dataset {task.dataset.name}"

    task.complete_task(result)
