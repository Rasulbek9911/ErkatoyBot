from django.urls import path
from .views import CategoryListView,ContentListView,ContentDetailView

urlpatterns = [
    path("category/",CategoryListView.as_view()),
    path("content/",ContentListView.as_view()),
    path("content_detail/",ContentDetailView.as_view()),
]