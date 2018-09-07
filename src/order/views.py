"""
   Contact App Views
"""
from order.models import Cart, CartProduct, Order
from order.serializers import  CartProductSerializer, CartProductPostSerializer, OrderSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response

class OrderViewset(viewsets.ViewSet):
    def list(self, request):
        try:
            user = self.request.user
            queryset = Order.objects.filter(cart=Cart.objects.get(user=user,is_cart_processed=False))
            serializer = OrderSerializer(queryset, many=True)
            return Response(serializer.data)
        except TypeError:
            return Response({'Error':'Add Token To request Heder'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except Cart.DoesNotExist:
            return Response({'Error':'No Any Product added in cart'},status=status.HTTP_204_NO_CONTENT)
        
    
class CartViewset(viewsets.ViewSet):
    def list(self, request):
        try:
            user = self.request.user
            queryset = CartProduct.objects.filter(cart=Cart.objects.get(user=user,is_cart_processed=False))
            serializer = CartProductSerializer(queryset, many=True)
            return Response(serializer.data)
        except TypeError:
            return Response({'Error':'Add Token To request Heder'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except Cart.DoesNotExist:
            return Response({'Error':'No Any Product added in cart'},status=status.HTTP_204_NO_CONTENT)
        

    def partial_update(self, request, pk=None):
        try:
            user = self.request.user
            cp = CartProduct.objects.get(cart=Cart.objects.get(user=user,is_cart_processed=False),pk=pk)
            serializer = CartProductSerializer(cp,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({'Error':'Not valid data'})
        except Cart.DoesNotExist:
            return Response({'Error':'No Any Product added in cart'},status=status.HTTP_204_NO_CONTENT)
        except CartProduct.DoesNotExist:
            return Response({'Error':'No Product avlable in cart'},status=status.HTTP_204_NO_CONTENT)
        except TypeError:
            return Response({'Error':'Add Token To request Heder'},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'Error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        

    def create(self, request):
        try:
            data = {}
            user = self.request.user
            
            cart=Cart.objects.get_or_create(user=user,is_cart_processed=False)[0]
            data['quantity'] = request.data['quantity']
            data['product_seller'] = request.data['product_seller']
            data['is_order_generated'] = False
            data['cart'] = cart.id
            
            serializer = CartProductPostSerializer(data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except TypeError:
            return Response({'Error':'Add Token To request Heder'},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'Error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        
    def destroy(self, request, pk=None):
        try:
            res = CartProduct.objects.get(pk=pk,cart=Cart.objects.get(user=self.request.user,is_cart_processed=False)).delete()
            return Response({"Msage":"deleted  sussesfully"},status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({'Error':'No Any Product added in cart'},status=status.HTTP_204_NO_CONTENT)
        except CartProduct.DoesNotExist:
            return Response({'Error':'No Product avlable in cart'},status=status.HTTP_204_NO_CONTENT)
        except TypeError:
            return Response({'Error':'Add Token To request Heder'},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'Error':str(e)},status=status.HTTP_400_BAD_REQUEST)