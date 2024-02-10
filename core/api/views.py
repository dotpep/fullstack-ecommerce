from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Product
from recommend.models import Review

from .serializers import ProductSerializer, ProductDetailtSerializer, ReviewSerializer
from .permissions import IsAdminOrReadOnly
from .pagination import StandardResultsSetPagination


class ProductListAPIView(generics.ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').order_by('id')


class ProductDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductDetailtSerializer
    lookup_field = "pk"


class ReviewCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        product_id = self.request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        existing_review = Review.objects.filter(
            product=product, created_by=self.request.user).exists()
        if existing_review:
            raise ValidationError("You have already reviewed this product.")
            
        serializer.save(created_by=self.request.user, product=product)
