"""Order API endpoints (Supabase-backed)."""
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional

from app.db.supabase import get_client
from app.schemas.order import OrderCreate, OrderOut

router = APIRouter()


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(order_in: OrderCreate):
    """Create a new order in Supabase."""
    supa = get_client()
    total_amount = 0.0
    items_payload = []
    # Validate products and compute totals via Supabase
    for item in order_in.items:
        p_resp = (
            supa.table("desserts")
            .select("id,name,price,in_stock")
            .eq("id", item.product_id)
            .limit(1)
            .execute()
        )
        rows = p_resp.data or []
        if not rows:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")
        prod = rows[0]
        if not bool(prod.get("in_stock", True)):
            raise HTTPException(status_code=400, detail=f"Product '{prod.get('name')}' is out of stock")
        price = float(prod.get("price", 0))
        total_amount += price * item.quantity
        items_payload.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": price,
        })

    # Create order (insert), then read back with a separate select (Option A)
    insert_payload = {
        "customer_name": order_in.customer_name,
        "customer_email": order_in.customer_email,
        "customer_phone": order_in.customer_phone,
        "total_amount": total_amount,
        "status": "pending",
    }
    supa.table("orders").insert(insert_payload).execute()

    # Read back the inserted order by customer_email (most recent)
    sel_resp = (
        supa.table("orders")
        .select("id,customer_name,customer_email,customer_phone,total_amount,status,created_at")
        .eq("customer_email", order_in.customer_email)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    sel_rows = sel_resp.data or []
    if not sel_rows:
        raise HTTPException(status_code=500, detail="Failed to create order")
    order = sel_rows[0]
    order_id = order["id"]

    if items_payload:
        supa.table("order_items").insert([
            {"order_id": order_id, **it} for it in items_payload
        ]).execute()

    return order


@router.get("/", response_model=List[OrderOut])
def list_orders(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    customer_email: Optional[str] = None,
):
    """Get list of orders from Supabase with optional filters."""
    supa = get_client()
    qb = (
        supa.table("orders")
        .select("id,customer_name,customer_email,customer_phone,total_amount,status,created_at")
        .order("id")
        .range(skip, max(skip, 0) + max(limit, 1) - 1)
    )
    if status_filter:
        qb = qb.eq("status", status_filter)
    if customer_email:
        qb = qb.eq("customer_email", customer_email)
    resp = qb.execute()
    return resp.data or []


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int):
    """Get a specific order by ID from Supabase."""
    supa = get_client()
    resp = (
        supa.table("orders")
        .select("id,customer_name,customer_email,customer_phone,total_amount,status,created_at")
        .eq("id", order_id)
        .limit(1)
        .execute()
    )
    rows = resp.data or []
    if not rows:
        raise HTTPException(status_code=404, detail="Order not found")
    return rows[0]


@router.patch("/{order_id}/status")
def update_order_status(order_id: int, new_status: str):
    """Update order status in Supabase."""
    valid_statuses = ["pending", "confirmed", "completed", "cancelled"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    supa = get_client()
    resp = (
        supa.table("orders")
        .update({"status": new_status})
        .eq("id", order_id)
        .select("id,customer_name,customer_email,customer_phone,total_amount,status,created_at")
        .execute()
    )
    rows = resp.data or []
    if not rows:
        raise HTTPException(status_code=404, detail="Order not found")
    return rows[0]
