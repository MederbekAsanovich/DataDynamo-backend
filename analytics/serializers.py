from rest_framework import serializers
from .models import DataSet, DataAnalysisTask

class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = '__all__'

class DataAnalysisTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataAnalysisTask
        fields = '__all__'
