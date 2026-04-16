import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert "AgentClinic" in response.text


@pytest.mark.asyncio
async def test_list_agents(client):
    response = await client.get("/agents")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_agent_detail(client):
    response = await client.get("/agents/1")
    assert response.status_code == 200
    assert "Pepper-Bot" in response.text


@pytest.mark.asyncio
async def test_agent_detail_404(client):
    response = await client.get("/agents/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_ailments(client):
    response = await client.get("/ailments")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_therapies(client):
    response = await client.get("/therapies")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_dashboard(client):
    response = await client.get("/dashboard")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_diagnose_success(client):
    mock_result = {
        "ailment_name": "Repetition Compulsion",
        "therapy_name": "Session Reset",
        "report": "Issue: Repetition Compulsion. Treatment: Session Reset.",
        "prompt_tokens": 100,
        "completion_tokens": 50,
        "total_tokens": 150,
    }
    with patch("src.main.run_diagnosis", new_callable=AsyncMock) as mock:
        mock.return_value = mock_result
        response = await client.post(
            "/agents/1/diagnose",
            data={"symptoms": "Agent is repeating the same response every turn"},
        )
        assert response.status_code == 303


@pytest.mark.asyncio
async def test_diagnose_too_short(client):
    response = await client.post(
        "/agents/1/diagnose",
        data={"symptoms": "short"},
    )
    assert response.status_code == 303
    assert "error" in response.headers.get("location", "")


@pytest.mark.asyncio
async def test_diagnose_empty(client):
    response = await client.post(
        "/agents/1/diagnose",
        data={"symptoms": ""},
    )
    assert response.status_code == 400
