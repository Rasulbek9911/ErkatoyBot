from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Content
from .serializers import CategorySerializer, ContentSerializer, ContentSerializer2
from .pagination import CustomPagination


class CategoryListView(APIView):
    def get(self, request):
        lang = request.query_params.get('lang')
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)


class ContentListView(APIView):
    def get(self, request):
        paginator = CustomPagination()
        msg = request.query_params.get('msg')
        lang = request.query_params.get('lang')
        category = Category.objects.filter(name_uz=msg)[:1]
        if len(category) >= 1:
            content = Content.objects.filter(category=category, language=lang)
            result_page = paginator.paginate_queryset(content, request)
            serializer = ContentSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response({'msg': 'not found'})


class ContentDetailView(APIView):
    def get(self, request):
        id = request.query_params.get('id')
        content = Content.objects.filter(id=id)[:1]
        serializer = ContentSerializer2(content, many=True)
        return Response(serializer.data)
