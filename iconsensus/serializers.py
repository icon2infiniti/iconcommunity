import os
from rest_framework import serializers

from .models import PrepProject

class PrepProjectsSerializer(serializers.ModelSerializer):
	category = serializers.CharField(source='get_category_display')
	progress = serializers.CharField(source='get_progress_display')
	status = serializers.CharField(source='get_status_display')

	class Meta:
		model = PrepProject
		fields = ('id','slug', 'name', 'prep_address', 'created_date', 'updated_date', 'start_date', 'end_date', 'description', 'category', 'progress', 'status', 'display')

class PrepProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrepProject
        fields = '__all__'