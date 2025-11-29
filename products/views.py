from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import action
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
import uuid
from pathlib import Path


class ProductViewSet(viewsets.ModelViewSet):
    """
    Product API
    - List/Retrieve: public
    - Create: SELLER/ADMIN only (authenticated)
    - Update/Delete: SELLER/ADMIN only
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # we'll enforce create/update permissions manually
    filterset_fields = ['category', 'sub_category']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name', 'moq']

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user or not user.is_authenticated or getattr(user, 'role', '').upper() not in ['SELLER', 'ADMIN']:
            raise PermissionDenied(detail='Only seller or admin users can create products')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        user = request.user
        if not user or not user.is_authenticated or getattr(user, 'role', '').upper() not in ['SELLER', 'ADMIN']:
            raise PermissionDenied(detail='Only seller or admin users can update products')
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if not user or not user.is_authenticated or getattr(user, 'role', '').upper() not in ['SELLER', 'ADMIN']:
            raise PermissionDenied(detail='Only seller or admin users can delete products')
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='upload-image')
    def upload_image(self, request):
        """Upload product image(s) and return accessible URLs.

        Expects multipart/form-data with one or more files in `images`.
        Returns: {'success': True, 'urls': [url, ...]}
        """
        print(f"\n=== UPLOAD REQUEST ===")
        print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")
        print(f"Content-Type: {request.META.get('CONTENT_TYPE', 'NOT SET')}")
        print(f"FILES keys: {list(request.FILES.keys())}")
        print(f"FILES: {request.FILES}")
        
        # Get files from 'images' field
        files = request.FILES.getlist('images')
        print(f"Extracted {len(files)} files from 'images' field")
        
        if not files:
            print("No files - returning 400")
            return Response({'success': False, 'error': 'No files provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure media directory exists
        media_root = Path(settings.MEDIA_ROOT)
        products_dir = media_root / 'products'
        products_dir.mkdir(parents=True, exist_ok=True)

        saved_urls = []
        for f in files:
            if not f:
                continue
            try:
                # Generate unique filename to avoid overwrites
                ext = os.path.splitext(f.name)[1]
                unique_name = f"{uuid.uuid4()}{ext}"
                base_path = os.path.join('products', unique_name)
                
                # Save file
                path = default_storage.save(base_path, ContentFile(f.read()))
                
                # Build public URL (absolute)
                url = request.build_absolute_uri(settings.MEDIA_URL + path)
                saved_urls.append(url)
                print(f"✅ Saved: {f.name} -> {url}")
            except Exception as e:
                print(f"❌ Error saving {f.name}: {str(e)}")
                return Response({
                    'success': False,
                    'error': f'Failed to save file: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        print(f"✅ Success - saved {len(saved_urls)} images")
        print(f"URLs: {saved_urls}")
        print(f"=== END ===\n")
        return Response({'success': True, 'urls': saved_urls}, status=status.HTTP_201_CREATED)
