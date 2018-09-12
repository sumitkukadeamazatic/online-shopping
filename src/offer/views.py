"""
Offer app views
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Offer
from .filters import OfferFilterBackend
from .serializers import OfferSerializer, OfferValidateSerializer
from .permissions import OfferPermission


class OfferViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    Offer related views
    """
    queryset = Offer.objects.all()
    filter_backends = (OfferFilterBackend,)
    serializer_class = OfferSerializer
    permission_classes = (OfferPermission,)

    @action(methods=['post'], detail=False)
    def validate(self, request):
        data = dict(request.data.items())
        if request.auth:
            data.update({'user_id': request.user.id})
        serializer = OfferValidateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=200)
