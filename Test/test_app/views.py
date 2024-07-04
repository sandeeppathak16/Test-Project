from django.shortcuts import render

from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from .models import Order, CurrentUser
from datetime import timedelta
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework.response import Response


# Create your views here.

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('user', 'amount', 'market')

    def validate(self, attrs):
        user = attrs.get('user')
        amount = attrs.get('amount')
        if amount > user.amount:
            raise APIException(
                detail="Insufficient balance",
                code=status.HTTP_400_BAD_REQUEST,
            )
        
        return amount
    
    def save(self, **kwargs):
        order = super().save(**kwargs)
        order.user.amount -= order.amount
        order.user.save()

        return order
    

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentUser
        fields = ('id', 'name', 'amount')



class PlaceOrderAPIVeiwset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @action(
        detail=True,
        methods=['post'],
        url_path='archive-export',
        url_name='archive-export',
    )
    def cancel(self, *args, **kwargs):
        order = self.get_object()
        if order.created < timezone.now() + timedelta(minutes=1):
            raise APIException(
                detail="Cancelation period is over",
                code=status.HTTP_400_BAD_REQUEST,
            )
        
        order.user.ammount += order.amamount
        order.user.save()
        order.delete()
        return Response({'message': 'order cancle successfull.'})
    
class CurrentUserAPIViewSet(viewsets.ModelViewSet):
    queryset = CurrentUser.objects.all()
    serializer_class = CurrentUserSerializer

