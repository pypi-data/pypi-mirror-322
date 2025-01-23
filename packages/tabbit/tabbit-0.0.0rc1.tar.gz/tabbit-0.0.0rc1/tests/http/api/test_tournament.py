from __future__ import annotations

import http

import httpx
import pytest
from fastapi import FastAPI


@pytest.mark.asyncio
async def test_api_tournament_crud(app: FastAPI) -> None:
    name = "World Universities Debating Championships 2025"
    abbreviation = "WUDC 2025"

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        # Create
        response = await client.post("/v1/tournaments/create", json={"name": name})
        assert response.status_code == http.HTTPStatus.OK
        tournament_id = response.json()["id"]

        # Read
        response = await client.get(f"/v1/tournaments/{tournament_id}")
        assert response.status_code == http.HTTPStatus.OK
        assert response.json() == {
            "id": tournament_id,
            "name": name,
            "abbreviation": None,
        }

        # Update
        response = await client.patch(
            f"/v1/tournaments/{tournament_id}",
            json={"abbreviation": abbreviation},
        )
        assert response.status_code == http.HTTPStatus.OK
        assert response.json() == {
            "id": tournament_id,
            "name": name,
            "abbreviation": abbreviation,
        }

        # Read (to check the update persists)
        response = await client.get(f"/v1/tournaments/{tournament_id}")
        assert response.status_code == http.HTTPStatus.OK
        assert response.json() == {
            "id": tournament_id,
            "name": name,
            "abbreviation": abbreviation,
        }

        # Update with None (cf. unset)
        response = await client.patch(
            f"/v1/tournaments/{tournament_id}",
            json={"abbreviation": None},
        )
        assert response.status_code == http.HTTPStatus.OK
        assert response.json() == {
            "id": tournament_id,
            "name": name,
            "abbreviation": None,
        }

        # Read (to check the update persists)
        response = await client.get(f"/v1/tournaments/{tournament_id}")
        assert response.status_code == http.HTTPStatus.OK
        assert response.json() == {
            "id": tournament_id,
            "name": name,
            "abbreviation": None,
        }

        # Delete
        response = await client.delete(f"/v1/tournaments/{tournament_id}")
        assert response.status_code == http.HTTPStatus.NO_CONTENT

        # Read (to check the deleted tournament cannot be found)
        response = await client.get(f"/v1/tournaments/{tournament_id}")
        assert response.status_code == http.HTTPStatus.NOT_FOUND

        # Update (to check the deleted tournament cannot be found)
        response = await client.patch(
            f"/v1/tournaments/{tournament_id}",
            json={"abbreviation": None},
        )
        assert response.status_code == http.HTTPStatus.NOT_FOUND

        # Delete (to check the deleted tournament cannot be found)
        response = await client.delete(f"/v1/tournaments/{tournament_id}")
        assert response.status_code == http.HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_api_tournament_list_empty(app: FastAPI) -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/v1/tournaments/")
        assert response.status_code == http.HTTPStatus.OK
        assert response.json() == []


@pytest.mark.asyncio
async def test_api_tournament_list(app: FastAPI) -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/v1/tournaments/create",
            json={"name": "Imperial IV"},
        )
        tournament_id = response.json()["id"]
        response = await client.get("/v1/tournaments/")
        assert response.json() == [
            {"id": tournament_id, "name": "Imperial IV", "abbreviation": None}
        ]


@pytest.mark.asyncio
async def test_api_tournament_list_offset(app: FastAPI) -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        _ = await client.post(
            "/v1/tournaments/create",
            json={"name": "Imperial Open 2021"},
        )
        response = await client.post(
            "/v1/tournaments/create",
            json={"name": "Imperial Open 2022"},
        )
        last_id = response.json()["id"]
        response = await client.get("/v1/tournaments/", params={"offset": 1})
        assert response.json() == [
            {"id": last_id, "name": "Imperial Open 2022", "abbreviation": None}
        ]


@pytest.mark.parametrize(
    ("insert_n", "limit", "expect_n"),
    [
        (0, 0, 0),
        (0, 1, 0),
        (1, 0, 0),
        (1, 2, 1),
        (2, 1, 1),
        (1, 1, 1),
    ],
)
@pytest.mark.asyncio
async def test_tournament_list_limit(
    app: FastAPI,
    insert_n: int,
    limit: int,
    expect_n: int,
) -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        for idx in range(insert_n):
            _ = await client.post(
                "/v1/tournaments/create",
                json={"name": f"Imperial IV {idx}"},
            )
        response = await client.get("/v1/tournaments/", params={"limit": limit})
        assert len(response.json()) == expect_n


@pytest.mark.parametrize(
    ("insert_names", "name_filter", "expect_names"),
    [
        ([], "", []),
        ([], "Foo", []),
        (["Foo"], "", ["Foo"]),
        (["Foo", "Bar"], "Foo", ["Foo"]),
        (["Foo", "Bar"], "foo", ["Foo"]),
        (["Oxford IV", "LSE Open", "LSE IV"], "LSE", ["LSE Open", "LSE IV"]),
        (["Oxford IV", "LSE Open", "LSE IV"], "IV", ["Oxford IV", "LSE IV"]),
    ],
)
@pytest.mark.asyncio
async def test_tournament_list_name_filter(
    app: FastAPI,
    insert_names: list[str],
    name_filter: str,
    expect_names: list[str],
) -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        for name in insert_names:
            _ = await client.post(
                "/v1/tournaments/create",
                json={"name": name},
            )
        response = await client.get("/v1/tournaments/", params={"name": name_filter})
        names = [tournament["name"] for tournament in response.json()]
        assert names == expect_names
