"""Product API endpoints (Supabase-backed)."""
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional

from app.db.supabase import get_client
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut

router = APIRouter()


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductCreate):
    """Create a new product in Supabase."""
    supa = get_client()
    resp = (
        supa.table("desserts")
        .insert(product_in.model_dump())
        .select("id,name,price,img,description,category,in_stock")
        .execute()
    )
    rows = resp.data or []
    if not rows:
        raise HTTPException(status_code=500, detail="Failed to insert product")
    row = rows[0]
    return ProductOut(
        id=row["id"],
        name=row.get("name"),
        price=float(row.get("price", 0)),
        img=row.get("img"),
        description=row.get("description"),
        category=row.get("category"),
        in_stock=bool(row.get("in_stock", True)),
    )


@router.get("/", response_model=List[ProductOut])
def list_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    in_stock: Optional[bool] = None,
):
    """Get list of products from Supabase with optional filters."""
    supa = get_client()
    qb = (
        supa.table("desserts")
        .select("id,name,price,img,description,category,in_stock")
        .order("id")
        .range(skip, max(skip, 0) + max(limit, 1) - 1)
    )
    if category:
        qb = qb.eq("category", category)
    if in_stock is not None:
        qb = qb.eq("in_stock", in_stock)
    resp = qb.execute()
    rows = resp.data or []
    return [
        ProductOut(
            id=row["id"],
            name=row.get("name"),
            price=float(row.get("price", 0)),
            img=row.get("img"),
            description=row.get("description"),
            category=row.get("category"),
            in_stock=bool(row.get("in_stock", True)),
        )
        for row in rows
    ]


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int):
    """Get a specific product by ID from Supabase."""
    supa = get_client()
    resp = (
        supa.table("desserts")
        .select("id,name,price,img,description,category,in_stock")
        .eq("id", product_id)
        .limit(1)
        .execute()
    )
    rows = resp.data or []
    if not rows:
        raise HTTPException(status_code=404, detail="Product not found")
    row = rows[0]
    return ProductOut(
        id=row["id"],
        name=row.get("name"),
        price=float(row.get("price", 0)),
        img=row.get("img"),
        description=row.get("description"),
        category=row.get("category"),
        in_stock=bool(row.get("in_stock", True)),
    )


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
):
    """Update a product in Supabase."""
    supa = get_client()
    update_data = product_in.model_dump(exclude_unset=True)
    resp = (
        supa.table("desserts")
        .update(update_data)
        .eq("id", product_id)
        .select("id,name,price,img,description,category,in_stock")
        .execute()
    )
    rows = resp.data or []
    if not rows:
        raise HTTPException(status_code=404, detail="Product not found")
    row = rows[0]
    return ProductOut(
        id=row["id"],
        name=row.get("name"),
        price=float(row.get("price", 0)),
        img=row.get("img"),
        description=row.get("description"),
        category=row.get("category"),
        in_stock=bool(row.get("in_stock", True)),
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    """Delete a product in Supabase."""
    supa = get_client()
    # Verify exists
    check = supa.table("desserts").select("id").eq("id", product_id).limit(1).execute()
    if not (check.data or []):
        raise HTTPException(status_code=404, detail="Product not found")
    supa.table("desserts").delete().eq("id", product_id).execute()
    return None
