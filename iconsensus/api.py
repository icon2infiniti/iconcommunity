from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter

from .models import PrepProject

from .serializers import (
	PrepProjectsSerializer,
	PrepProjectSerializer,	
)

class PrepProjectsAPI(ListAPIView):
	""" prep projects api
	"""
	serializer_class = PrepProjectsSerializer
	filter_backends = [OrderingFilter]
	ordering_fields = ['created_date', ]	


	def get_queryset(self):
		queryset = self.serializer_class.Meta.model.objects.all()
		category = self.request.query_params.get('category', None)
		if category is not None:
			queryset = queryset.filter(category=category)

		status = self.request.query_params.get('status', None)
		if status is not None:
			queryset = queryset.filter(status=status)

		recent_activity = self.request.query_params.get('recent_activity', None)
		if recent_activity is '1':
			#CREATED IN THE LAST 7 DAYS
			queryset = queryset.filter(created_date__gte=datetime.now()-timedelta(days=7))			
		
		if recent_activity is '2':
			#UPDATE IN THE LAST 7 DAYS
			queryset = queryset.filter(updated_date__gte=datetime.now()-timedelta(days=7))					
		
		return queryset.order_by('?')        


class PrepProjectAPI(RetrieveAPIView):
	""" prep report api
	"""

	lookup_field = 'pk'
	queryset = PrepProject.objects.all()
	serializer_class = PrepProjectSerializer

class PrepProjectFiltersApi(ViewSet):
	""" filters api
	"""
	
	def get(self, *args, **kwargs):
		filters_data = {}
		filters_data['categories'] =  [{ 'name': category_name, 'id':category_id, 'count':PrepProject.objects.filter(category=category_id).count() }  for category_id, category_name in PrepProject.CATEGORIES ]
		filters_data['status'] =  [{ 'name': status_name, 'id':status_id, 'count':PrepProject.objects.filter(status=status_id).count() }  for status_id,status_name in PrepProject.STATUS ]

		return Response(filters_data, status=200)		

class PrepApi(ViewSet):
	""" filters api
	"""
	
	def get(self, *args, **kwargs):
		data = {}
		prep_address = kwargs.get('prep_address', None)		
		if prep_address:
			prep_project_categories = { category_name: PrepProject.objects.filter(prep_address=prep_address).filter(category=category_id).count() for category_id, category_name in PrepProject.CATEGORIES }
			prep_project_categories = {k: v for k, v in sorted(prep_project_categories.items(), key=lambda item: item[1], reverse=True)}
			main_category = list(prep_project_categories.keys())[0]
			if prep_project_categories[main_category] > 0:
				data['main_category'] = main_category

			sub_category = list(prep_project_categories.keys())[1]
			if prep_project_categories[sub_category] > 0:
				data['sub_category'] = sub_category

		return Response(data, status=200)		



class PrepFiltersApi(ViewSet):
	""" filters api
	"""
	
	def get(self, *args, **kwargs):
		filters_data = {}
		filters_data['categories'] =  [{ 'name': category_name, 'id':category_id, 'count':PrepProject.objects.distinct('prep_address', 'category').filter(category=category_id).count() }  for category_id, category_name in PrepProject.CATEGORIES ]

		return Response(filters_data, status=200)		







