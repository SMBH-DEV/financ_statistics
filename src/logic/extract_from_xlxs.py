from src.schemas.statistic import Statistic
import pandas as pd
from typing import List
from datetime import datetime
import os

class ExcelExtractor:
    def __init__(self, file_path: str):
        """
        Инициализация экстрактора Excel файлов
        
        Args:
            file_path (str): Путь к Excel файлу
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден")
            
        if not file_path.endswith(('.xlsx', '.xls')):
            raise ValueError("Файл должен быть формата .xlsx или .xls")
            
        self.file_path = file_path

    def extract_statistics(self) -> List[Statistic]:
        """
        Чтение данных из Excel файла и преобразование их в список объектов Statistic
        
        Returns:
            List[Statistic]: Список объектов статистики
        """
        try:
            # Чтение Excel файла
            df = pd.read_excel(self.file_path)
            
            # Преобразование каждой строки в объект Statistic
            statistics = []
            for _, row in df.iterrows():
                # Пропускаем итоговую строку и проверяем валидность даты
                date_str = row.iloc[0]
                if date_str == 'Total:' or pd.isna(date_str):
                    continue

                # Преобразование даты в ISO формат
                if isinstance(date_str, str):
                    date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                    iso_date = date_obj.strftime('%Y-%m-%d')
                else:
                    iso_date = date_str

                # Создание объекта Statistic, используя индексы колонок
                statistic = Statistic(
                    created_at=iso_date,          # Date (UTC)
                    organization=row.iloc[1],       # Organization
                    object_=row.iloc[2],           # Object
                    spent=row.iloc[3],             # Spent, EUR
                    impressions=row.iloc[4],       # Impressions
                    clicks=row.iloc[5],            # Clicks
                    goals=row.iloc[6],             # Goals
                    ctr=row.iloc[7],              # CTR,%
                    cpm=row.iloc[8],              # CPM, EUR
                    cpc=row.iloc[9],              # Cost per click (CPC), EUR
                    cps=row.iloc[10]              # Cost per subscriber (CPS), EUR
                )
                statistics.append(statistic)
                
            return statistics
            
        except Exception as e:
            raise Exception(f"Ошибка при чтении данных из Excel файла: {str(e)}")

