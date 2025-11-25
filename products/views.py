from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public API for product catalog
    List and Retrieve only (no create/update/delete via API)
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Public access
    filterset_fields = ['category', 'sub_category']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name', 'moq']
