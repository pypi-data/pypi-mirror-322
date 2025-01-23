from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tabbit.database.operations import tournament as crud
from tabbit.schemas.tournament import ListTournamentsQuery
from tabbit.schemas.tournament import Tournament
from tabbit.schemas.tournament import TournamentCreate
from tabbit.schemas.tournament import TournamentPatch


@pytest.mark.asyncio
async def test_tournament_crud(session: AsyncSession) -> None:
    name = "European Universities Debating Championships 2024"
    abbreviation = "eudc2024"

    # Create
    tournament_create = TournamentCreate(name=name, abbreviation=None)
    tournament_id = await crud.create_tournament(session, tournament_create)

    # Read
    tournament = await crud.get_tournament(session, tournament_id)
    assert tournament is not None
    assert tournament.name == name
    assert tournament.abbreviation is None

    # Update
    patch = TournamentPatch(id=tournament_id, abbreviation=abbreviation)
    tournament = await crud.patch_tournament(session, tournament_id, patch)
    assert tournament is not None
    assert tournament.name == name
    assert tournament.abbreviation == abbreviation

    # Read (to check the update persists)
    tournament = await crud.get_tournament(session, tournament_id)
    assert tournament is not None
    assert tournament.name == name
    assert tournament.abbreviation == abbreviation

    # Update with None (cf. unset)
    patch = TournamentPatch(id=tournament_id, abbreviation=None)
    tournament = await crud.patch_tournament(session, tournament_id, patch)
    assert tournament is not None
    assert tournament.name == name
    assert tournament.abbreviation is None

    # Read (to check the update persists)
    tournament = await crud.get_tournament(session, tournament_id)
    assert tournament is not None
    assert tournament.name == name
    assert tournament.abbreviation is None

    # Delete
    deleted_tournament = await crud.delete_tournament(session, tournament_id)
    assert deleted_tournament == tournament_id

    # Read (to check the deleted tournament cannot be found)
    tournament = await crud.get_tournament(session, tournament_id)
    assert tournament is None, "Expected tournament to be deleted."

    # Update (to check the deleted tournament cannot be found)
    patch = TournamentPatch(id=tournament_id, abbreviation=abbreviation)
    tournament = await crud.patch_tournament(session, tournament_id, patch)
    assert tournament is None, "Expected tournament to be deleted."

    # Delete (to check the deleted tournament cannot be found)
    deleted_tournament = await crud.delete_tournament(session, tournament_id)
    assert deleted_tournament is None, "Expected tournament to be deleted."


@pytest.mark.asyncio
async def test_tournament_list_empty(session: AsyncSession) -> None:
    tournaments = await crud.list_tournaments(
        session,
        list_tournaments_query=ListTournamentsQuery(),
    )
    assert tournaments == []


@pytest.mark.asyncio
async def test_tournament_list(session: AsyncSession) -> None:
    tournament_name = "Manchester IV"
    tournament_create = TournamentCreate(name=tournament_name)
    tournament_id = await crud.create_tournament(session, tournament_create)
    tournament = Tournament(id=tournament_id, name=tournament_name)

    result = await crud.list_tournaments(
        session,
        list_tournaments_query=ListTournamentsQuery(),
    )

    assert result == [tournament]


@pytest.mark.asyncio
async def test_tournament_list_offset(session: AsyncSession) -> None:
    _ = await crud.create_tournament(session, TournamentCreate(name="First"))
    last_id = await crud.create_tournament(session, TournamentCreate(name="Last"))

    result = await crud.list_tournaments(
        session,
        list_tournaments_query=ListTournamentsQuery(offset=1),
    )

    assert len(result) == 1
    assert result[0].id == last_id
    assert result[0].name == "Last"


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
    session: AsyncSession,
    insert_n: int,
    limit: int,
    expect_n: int,
) -> None:
    for idx in range(insert_n):
        _ = await crud.create_tournament(
            session,
            TournamentCreate(name=f"Tournament {idx}"),
        )
    result = await crud.list_tournaments(
        session,
        list_tournaments_query=ListTournamentsQuery(limit=limit),
    )
    assert len(result) == expect_n


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
    session: AsyncSession,
    insert_names: list[str],
    name_filter: str,
    expect_names: list[str],
) -> None:
    for name in insert_names:
        _ = await crud.create_tournament(
            session,
            TournamentCreate(name=name),
        )
    result = await crud.list_tournaments(
        session,
        list_tournaments_query=ListTournamentsQuery(name=name_filter),
    )
    names = [tournament.name for tournament in result]
    assert names == expect_names
