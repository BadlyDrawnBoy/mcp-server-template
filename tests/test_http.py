import httpx
import pytest

from bridge.app import create_app


@pytest.fixture()
def app():
    return create_app()


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
@pytest.mark.anyio
async def test_ping_and_version(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        ping = await client.get("/api/ping.json")
        assert ping.status_code == 200
        assert ping.json() == {"ok": True, "data": {"pong": True}, "errors": []}

        version = await client.get("/api/version.json")
        assert version.status_code == 200
        assert version.json() == {"ok": True, "data": {"version": "0.0.0"}, "errors": []}


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
@pytest.mark.anyio
async def test_openapi_schema(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert schema["info"]["title"] == "MCP Server Template API"
        assert "/api/ping.json" in schema["paths"]
        assert "/api/version.json" in schema["paths"]


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
@pytest.mark.anyio
async def test_sse_rejects_second_connection(app):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        from bridge.app import _BRIDGE_STATE, _STATE_LOCK

        async with _STATE_LOCK:
            _BRIDGE_STATE.active_sse_id = "testing"

        try:
            response = await client.get("/sse")
            assert response.status_code == 409
        finally:
            async with _STATE_LOCK:
                _BRIDGE_STATE.active_sse_id = None
