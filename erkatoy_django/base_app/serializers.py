from .models import Content, Category
from rest_framework.serializers import ModelSerializer


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ContentSerializer(ModelSerializer):
    class Meta:
        model = Content
        fields = ("id", 'title','rasm')


class ContentSerializer2(ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"