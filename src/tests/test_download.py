from src.logic.download_xlxs import current_date, get_data


async def test_current_date():
    day, month, year = await current_date()
    assert day is not None
    assert month is not None
    assert year is not None

async def test_get_data():
    await get_data()