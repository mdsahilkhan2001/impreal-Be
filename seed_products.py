import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from products.models import Product

def seed_products():
    products_data = [
        {
            "name": "Luxury Silk Kaftan",
            "description": "Elegant handcrafted silk kaftan with intricate embroidery. Perfect for evening wear and special occasions.",
            "category": "kaftan",
            "sub_category": "Luxury Kaftan",
            "images": [
                "https://placehold.co/600x800/png?text=Luxury+Kaftan+Front",
                "https://placehold.co/600x800/png?text=Luxury+Kaftan+Back"
            ],
            "price_tiers": [
                {"minQty": 50, "maxQty": 100, "price": 45.00},
                {"minQty": 101, "maxQty": 500, "price": 40.00},
                {"minQty": 501, "maxQty": 1000, "price": 35.00}
            ],
            "colors": [
                {"name": "Emerald Green", "hex": "#50C878", "image": ""},
                {"name": "Royal Blue", "hex": "#4169E1", "image": ""}
            ],
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "moq": 50,
            "lead_time": "15-20 days",
            "customization": ["Logo", "Label", "Packaging"],
            "specifications": {
                "material": "100% Silk",
                "fabricType": "Woven",
                "technics": "Embroidered",
                "feature": "Breathable, Sustainable",
                "origin": "India"
            }
        },
        {
            "name": "Premium Abaya Dress",
            "description": "Modest and stylish Abaya dress made from high-quality Nida fabric. Comfortable for daily wear.",
            "category": "kaftan",
            "sub_category": "Abaya",
            "images": [
                "https://placehold.co/600x800/png?text=Abaya+Dress+Front",
                "https://placehold.co/600x800/png?text=Abaya+Dress+Side"
            ],
            "price_tiers": [
                {"minQty": 100, "maxQty": 500, "price": 25.00},
                {"minQty": 501, "maxQty": 1000, "price": 22.00}
            ],
            "colors": [
                {"name": "Black", "hex": "#000000", "image": ""},
                {"name": "Navy", "hex": "#000080", "image": ""}
            ],
            "sizes": ["Free Size"],
            "moq": 100,
            "lead_time": "10-15 days",
            "customization": ["Label", "Packaging"],
            "specifications": {
                "material": "Nida Fabric",
                "fabricType": "Knitted",
                "technics": "Plain Dyed",
                "feature": "Anti-Static, Anti-Wrinkle",
                "origin": "UAE"
            }
        },
        {
            "name": "Organic Cotton T-Shirt",
            "description": "Eco-friendly 100% organic cotton t-shirt. Soft, durable, and perfect for custom printing.",
            "category": "loungewear",
            "sub_category": "Cotton Tee",
            "images": [
                "https://placehold.co/600x800/png?text=Cotton+Tee+Front",
                "https://placehold.co/600x800/png?text=Cotton+Tee+Back"
            ],
            "price_tiers": [
                {"minQty": 500, "maxQty": 1000, "price": 5.50},
                {"minQty": 1001, "maxQty": 5000, "price": 4.80},
                {"minQty": 5001, "maxQty": 10000, "price": 4.20}
            ],
            "colors": [
                {"name": "White", "hex": "#FFFFFF", "image": ""},
                {"name": "Black", "hex": "#000000", "image": ""},
                {"name": "Grey", "hex": "#808080", "image": ""}
            ],
            "sizes": ["XS", "S", "M", "L", "XL", "XXL", "3XL"],
            "moq": 500,
            "lead_time": "20-25 days",
            "customization": ["Print", "Embroidery", "Label", "Packaging"],
            "specifications": {
                "material": "100% Organic Cotton",
                "fabricType": "Jersey",
                "technics": "Plain Dyed",
                "feature": "Eco-Friendly, Breathable",
                "origin": "Bangladesh"
            }
        }
    ]

    print("Seeding products...")
    for p_data in products_data:
        product, created = Product.objects.update_or_create(
            name=p_data['name'],
            defaults=p_data
        )
        if created:
            print(f"Created product: {product.name}")
        else:
            print(f"Updated product: {product.name}")
    print("Seeding complete!")

if __name__ == '__main__':
    seed_products()
