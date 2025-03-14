from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response

from courses.models import Category,Course,Lesson
from courses import serializer
from courses import paginators

class CategoryViewset(viewsets.ViewSet,generics.ListAPIView):
    queryset = Category.objects.filter(active = True)
    serializer_class = serializer.CategorySerializer

class CourseViewset(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active = True)
    serializer_class = serializer.CourseSerializer
    pagination_class = paginators.CoursePaginater

    def get_queryset(self):
        queryset = self.queryset
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(subject__icontains = q)
        cate_id = self.request.query_params.get('cate_id')
        if cate_id:
            queryset = queryset.filter(category_id = cate_id)
        return queryset

    @action(detail=True, methods=['get'],url_path="lessons")
    def lessons(self, request, pk=None):
        lessons = self.get_object().lessons.filter(active=True)
        return Response(serializer.LessonSerializer(lessons,many=True).data, status= status.HTTP_200_OK)


#prefetch_related() lấy truocws các tags hệu suất hơn
class LessonViewset(viewsets.ViewSet,generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related().filter(active =True)  # Sửa get() -> all()
    serializer_class = serializer.LessonDetailSerializer