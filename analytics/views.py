from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import DataSet, DataAnalysisTask
from .serializers import DataSetSerializer, DataAnalysisTaskSerializer
from .tasks import process_data_task

class DataSetViewSet(viewsets.ModelViewSet):
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        dataset = self.get_object()
        task = DataAnalysisTask.objects.create(dataset=dataset)
        task.start_task()
        process_data_task.delay(task.id)  # Call Celery task
        return Response({'status': 'processing started'})


class DataAnalysisTaskViewSet(viewsets.ModelViewSet):
    queryset = DataAnalysisTask.objects.all()
    serializer_class = DataAnalysisTaskSerializer
