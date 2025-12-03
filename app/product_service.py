from typing import List
from app.schemas.product import ProductOut
from app.db.supabase import get_client


def products_by_ids(ids: List[int]) -> List[ProductOut]:
    if not ids:
        return []
    supa = get_client()
    # Fetch by IDs using Supabase
    resp = (
        supa.table("desserts")
        .select("id,name,price,img,description,category,in_stock")
        .in_("id", ids)
        .execute()
    )
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
