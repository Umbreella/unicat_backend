from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from ..models.Feedback import Feedback
from ..permissions.CreateAnyButEditAdmin import CreateAnyButEditAdmin
from ..serializers.FeedbackSerializer import FeedbackSerializer


class FeedbackView(ModelViewSet):
    queryset = Feedback.objects.all()
    permission_classes = (CreateAnyButEditAdmin,)
    serializer_class = FeedbackSerializer
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('email',)
    ordering_fields = ('id', 'created_at',)
    ordering = ('id',)
