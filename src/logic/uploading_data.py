from src.config.settings import settings
from src.logic.download_xlxs import get_data
from src.logic.extract_from_xlxs import ExcelExtractor
from src.database.models import Statistics
from src.database.session import get_session
from loguru import logger

async def upload_data():
    try:
        file_path = await get_data()
        extractor = ExcelExtractor(file_path)
        statistics = extractor.extract_statistics()
        statistics_models = [Statistics(**stat.model_dump()) for stat in statistics]
        async with get_session() as session:
            session.add_all(statistics_models)
            await session.commit()
        logger.success("Data uploaded successfully")
    except Exception as e:
        logger.error(f"Error uploading data: {e}")