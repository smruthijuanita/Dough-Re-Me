"""Seed database with sample bakery products."""
from app.db.session import SessionLocal
from app.models.product import Product

def seed_products():
    """Add sample products to the database."""
    db = SessionLocal()
    
    # Check if products already exist
    existing_count = db.query(Product).count()
    if existing_count > 0:
        print(f"Database already has {existing_count} products. Skipping seed.")
        db.close()
        return
    
    products = [
        Product(
            name="Chocolate Brownie",
            description="Rich, fudgy chocolate brownie with walnuts",
            price=4.99,
            category="brownie",
            image_url="/static/images/brownie.jpeg",
            in_stock=True
        ),
        Product(
            name="Blueberry Crumble",
            description="Fresh blueberries with buttery crumble topping",
            price=5.99,
            category="cake",
            image_url="/static/images/blueberry_crumble.jpeg",
            in_stock=True
        ),
        Product(
            name="Banana Walnut Bread",
            description="Moist banana bread with crunchy walnuts",
            price=6.99,
            category="bread",
            image_url="/static/images/banana_walnut.jpeg",
            in_stock=True
        ),
        Product(
            name="Tiramisu",
            description="Classic Italian dessert with mascarpone and espresso",
            price=7.99,
            category="cake",
            image_url="/static/images/tiramisu.jpeg",
            in_stock=True
        ),
        Product(
            name="Mango Cheesecake",
            description="Creamy cheesecake with fresh mango topping",
            price=8.99,
            category="cake",
            image_url="/static/images/mango_cheesecake.jpeg",
            in_stock=True
        ),
        Product(
            name="Caramel Custard",
            description="Silky smooth custard with rich caramel sauce",
            price=5.49,
            category="dessert",
            image_url="/static/images/caramel_custard.jpeg",
            in_stock=True
        ),
    ]
    
    try:
        db.add_all(products)
        db.commit()
        print(f"✅ Successfully added {len(products)} products to the database!")
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_products()
