"""
Return App Views
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from .serializers import ReturnLineitemShippingSerializer


class ReturnLineItemShippingView(APIView):
    """
    View to save shipping details against return line items
    """

    def post(self, request):  # pylint: disable=no-self-use
        """
        Method to handle post method
        """
        lineitems = request.data.pop('return_lineitems')
        shipping_details = request.data
        lineitem_shippingdetails_serializer = ReturnLineitemShippingSerializer(
            data={'shipping_details': shipping_details, 'lineitems': lineitems})
        lineitem_shippingdetails_serializer.is_valid(raise_exception=True)
        response = lineitem_shippingdetails_serializer.save()
        return Response(response['response'], status=HTTP_201_CREATED)
