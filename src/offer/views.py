"""
Offer app views
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from .models import Offer
from .filters import OfferFilterBackend
from .serializers import OfferSerializer, OfferValidateSerializer
from rest_framework.permissions import IsAuthenticated


class OfferViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    Offer related views
    """
    queryset = Offer.objects.all()
    filter_backends = (OfferFilterBackend,)
    serializer_class = OfferSerializer
    permission_classes = (IsAuthenticated,)

    @action(methods=['post'], detail=False)
    def validate(self, request):  # pylint: disable=no-self-use
        """
        View to validate offer, and calculate related amounts
        """
        data = dict(request.data.items())
        if request.auth:
            data.update({'user_id': request.user.id})
        serializer = OfferValidateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=HTTP_200_OK)
