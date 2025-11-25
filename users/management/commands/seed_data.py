"""
Django management command to seed initial data
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from leads.models import Lead
from suppliers.models import Supplier
from products.models import Product

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds database with initial data'
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Create users
        self.create_users()
        
        # Create suppliers
        self.create_suppliers()
        
        # Create products
        self.create_products()
        
        # Create leads
        self.create_leads()
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
    
    def create_users(self):
        if User.objects.count() > 0:
            self.stdout.write('Users already exist, skipping...')
            return
        
        users = [
            {'email': 'admin@example.com', 'username': 'admin', 'password': 'password123', 
             'role': 'ADMIN', 'first_name': 'Admin', 'last_name': 'User'},
            {'email': 'buyer@example.com', 'username': 'buyer', 'password': 'password123',
             'role': 'BUYER', 'first_name': 'Buyer', 'last_name': 'User'},
            {'email': 'seller@example.com', 'username': 'seller', 'password': 'password123',
             'role': 'SELLER', 'first_name': 'Seller', 'last_name': 'User'},
            {'email': 'designer@example.com', 'username': 'designer', 'password': 'password123',
             'role': 'DESIGNER', 'first_name': 'Designer', 'last_name': 'User'},
        ]
        
        for user_data in users:
            User.objects.create_user(**user_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users'))
    
    def create_suppliers(self):
        if Supplier.objects.count() > 0:
            self.stdout.write('Suppliers already exist, skipping...')
            return
        
        suppliers = [
            {
                'name': 'Fabrics R Us',
                'contact_person': 'Mike Ross',
                'email': 'mike@fabricsrus.com',
                'phone': '9876543210',
                'address': '123 Textile Market, Surat',
                'category': 'FABRIC',
                'total_billed': 5000,
                'total_paid': 2000,
                'balance': 3000
            },
            {
                'name': 'Premium Trims',
                'contact_person': 'Sarah Lee',
                'email': 'sarah@premiumtrims.com',
                'phone': '9123456789',
                'address': '456 Button Street, Delhi',
                'category': 'TRIMS',
                'total_billed': 1000,
                'total_paid': 1000,
                'balance': 0
            }
        ]
        
        for supplier_data in suppliers:
            Supplier.objects.create(**supplier_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(suppliers)} suppliers'))
    
    def create_products(self):
        if Product.objects.count() > 0:
            self.stdout.write('Products already exist, skipping...')
            return
        
        products = [
            {
                'name': 'Premium Cotton Linen Resort Shirt',
                'description': 'Experience the ultimate comfort with our Premium Cotton Linen Resort Shirt.',
                'category': 'Men Clothing',
                'sub_category': 'Shirts',
                'images': [
                    'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?q=80&w=1000',
               ],
                'price_tiers': [
                    {'minQty': 50, 'maxQty': 199, 'price': 18.50},
                    {'minQty': 200, 'maxQty': 499, 'price': 16.50},
                    {'minQty': 500, 'price': 15.00}
                ],
                'colors': [
                    {'name': 'Classic White', 'hex': '#FFFFFF'},
                    {'name': 'Sky Blue', 'hex': '#87CEEB'},
                ],
                'sizes': ['S', 'M', 'L', 'XL', 'XXL'],
                'moq': 50,
                'lead_time': '20-25 days',
                'customization': ['Logo Embroidery', 'Custom Buttons'],
                'specifications': {
                    'material': '60% Cotton, 40% Linen',
                    'fabricType': 'Woven',
                    'origin': 'India'
                }
            }
        ]
        
        for product_data in products:
            Product.objects.create(**product_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(products)} products'))
    
    def create_leads(self):
        if Lead.objects.count() > 0:
            self.stdout.write('Leads already exist, skipping...')
            return
        
        buyer_user = User.objects.filter(role='BUYER').first()
        
        leads = [
            {
                'name': 'John Doe',
                'email': 'john@example.com',
                'phone': '+1234567890',
                'country': 'USA',
                'product_type': 'Resort Wear',
                'quantity': 500,
                'budget': '15000',
                'message': 'Looking for high quality silk kaftans.',
                'status': 'NEW',
                'user': buyer_user
            },
            {
                'name': 'Jane Smith',
                'email': 'jane@boutique.co.uk',
                'phone': '+447700900077',
                'country': 'UK',
                'product_type': 'Loungewear',
                'quantity': 200,
                'budget': '5000',
                'message': 'Need cotton loungewear sets.',
                'status': 'QUALIFIED',
                'user': buyer_user
            }
        ]
        
        for lead_data in leads:
            Lead.objects.create(**lead_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(leads)} leads'))
