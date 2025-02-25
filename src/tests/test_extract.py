from src.config.settings import settings
from src.logic.extract_from_xlxs import ExcelExtractor

async def test_extract_from_xlxs():
    path = './Report.xlsx 25.02.2025.xlsx'
    extractor = ExcelExtractor(path)
    statistics = extractor.extract_statistics()
    print(statistics)