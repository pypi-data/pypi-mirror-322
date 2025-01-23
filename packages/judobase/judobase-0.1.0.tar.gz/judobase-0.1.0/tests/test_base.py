import pytest
from aioresponses import aioresponses
from aiohttp import ClientSession

from judobase.base import _Base
from judobase.schemas import Competition, Competitor, Contest


@pytest.mark.asyncio
async def test_aenter_aexit():
    """Test that the context manager properly creates and closes the session."""

    async with _Base() as client:
        assert isinstance(client._session, ClientSession)
        assert not client._session.closed
    assert client._session.closed


@pytest.mark.asyncio
async def test_get_json_success():
    """Test _get_json with a successful API response."""

    async with _Base() as client:
        params = {"key": "value"}
        mock_response = {"data": "test"}

        with aioresponses() as mock:
            mock.get(client.base_url + "get_json", payload=mock_response, status=200)

            result = await client._get_json(params)
            assert result == mock_response


@pytest.mark.asyncio
async def test_get_json_failure():
    """Test _get_json with a failed API response."""

    async with _Base() as client:
        params = {"key": "value"}

        with aioresponses() as mock:
            mock.get(client.base_url + "get_json", status=500)

            with pytest.raises(ConnectionError) as exc_info:
                await client._get_json(params)

            assert "500" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_competition_list():
    """Test _get_competition_list method."""

    async with _Base() as client:
        params = {
            "params[action]": "competition.get_list",
            "params[year]": "2023",
            "params[month]": "01",
            "params[sort]": -1,
            "params[limit]": 5000,
        }

        mock_response = [{"id": 1, "name": "Competition 1"}]
        expected_result = [Competition(id=1, name="Competition 1")]

        with aioresponses() as mock:
            mock.get(client.base_url + "get_json", payload=mock_response, status=200)

            result = await client._get_competition_list(years="2023", months="01")
            assert result == expected_result


@pytest.mark.asyncio
async def test_find_contests():
    """Test _find_contests method."""

    async with _Base() as client:
        params = {
            "params[action]": "contest.find",
            "params[id_competition]": "123",
            "params[id_weight]": "",
            "params[id_person]": "",
            "params[order_by]": "cnum",
            "params[limit]": 5000,
        }

        mock_response = {"contests": [{"id": 1, "name": "Contest 1"}]}
        expected_result = [Contest(id=1, name="Contest 1")]

        with aioresponses() as mock:
            mock.get(client.base_url + "get_json", payload=mock_response, status=200)

            result = await client._find_contests(id_competition="123")
            assert result == expected_result


@pytest.mark.asyncio
async def test_competitor_info():
    """Test competitor_info method."""

    async with _Base() as client:
        params = {
            "params[action]": "competitor.info",
            "params[id_person]": "456",
        }

        mock_response = [{"id": 456, "name": "Competitor 1"}]
        expected_result = [Competitor(id=456, name="Competitor 1")]

        with aioresponses() as mock:
            mock.get(client.base_url + "get_json", payload=mock_response, status=200)

            result = await client.competitor_info(id_competitor="456")
            assert result == expected_result
