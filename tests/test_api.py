import pytest

@pytest.mark.asyncio
async def test_debug_overrides(client):
    from src.main import app
    from src.db.build import get_async_db
    
    print(f"\n[DEBUG] App ID: {id(app)}")
    print(f"[DEBUG] Target Func ID: {id(get_async_db)}")
    print(f"[DEBUG] Overrides keys: {[id(k) for k in app.dependency_overrides.keys()]}")
    print(f"[DEBUG] Is override set? {get_async_db in app.dependency_overrides}")
    
    response = await client.post("/chats/", json={"title": "Test Chat"})
    assert response.status_code == 200