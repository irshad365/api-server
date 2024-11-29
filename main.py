from fastapi import FastAPI, APIRouter, HTTPException, Depends

app = FastAPI()

# Authentication Dependency
def verify_token(token: str):
    # Dummy token verification logic
    if token != "valid_token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"username": "test_user"}

router = APIRouter()

# In-memory data storage
data = []

@router.get("/")
def read_items(user=Depends(verify_token)):
    return {"data": data}

@router.post("/")
def create_item(item: str, user=Depends(verify_token)):
    data.append(item)
    return {"message": "Item added", "item": item}

@router.patch("/{index}")
def update_item(index: int, new_item: str, user=Depends(verify_token)):
    if index < 0 or index >= len(data):
        raise HTTPException(status_code=404, detail="Item not found")
    old_item = data[index]
    data[index] = new_item
    return {"message": "Item updated", "old_item": old_item, "new_item": new_item}

@router.delete("/{index}")
def delete_item(index: int, user=Depends(verify_token)):
    if index < 0 or index >= len(data):
        raise HTTPException(status_code=404, detail="Item not found")
    removed_item = data.pop(index)
    return {"message": "Item deleted", "item": removed_item}

app.include_router(router, prefix="/items", tags=["items"])
