from rest_framework import viewsets
from rest_framework import filters

#from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import ScopedRateThrottle
#from rest_framework.pagination import PageNumberPagination
#from rest_framework.pagination import LimitOffsetPagination
from .pagination import CatsPagination
from .throttling import WorkingHoursRateThrottle
from .permissions import OwnerOrReadOnly, ReadOnly
from .models import Achievement, Cat, User
from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend



class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    #throttle_classes = (AnonRateThrottle,)
    throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle)
    throttle_scope = 'low_request'
    #pagination_class = PageNumberPagination
    #pagination_class = LimitOffsetPagination
    #pagination_class = CatsPagination
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ('color', 'birth_year')
    #search_fields = ('^name',)
    search_fields = ('achievements__name', 'owner__username') #для связанных моделей
    ordering_fields = ('name', 'birth_year')
    ordering = ('birth_year',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
