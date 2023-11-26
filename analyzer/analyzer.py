from typing import Dict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.use('Agg')  # Используем Agg для работы с matplotlib без GUI

class ErrorDataAnalyzer:
    """
    Класс для анализа файла с ошибками.

    Parameters:
        _filename (str): Путь к файлу с данными.

    Attributes:
        _filename (str): Путь к файлу с данными.
        _df (pd.DataFrame): DataFrame для хранения загруженных данных.
        _most_common_errors (pd.Series): Серия с самыми часто встречающимися ошибками.
        _histogram_path (str): Путь к сохраненному графику гистограммы.
        _pie_path (str): Путь к сохраненному графику круговой диаграммы.
        _load_data_error (str): Сообщение об ошибке при загрузке данных.
    """
    __slots__ = ['_filename', '_df', '_most_common_errors', 'histogram_path', 'pie_path', '_load_data_error']

    def __init__(self, filename):
        self._filename: str = filename
        self._df: pd.DataFrame = None
        self._most_common_errors: pd.Series = None
        self.histogram_path: str = None
        self.pie_path: str = None
        self._load_data_error: str = None

    def load_data(self) -> bool:
        """
        Загружает данные из Excel файла, преобразует столбец 'Error Code' в числовой тип данных.

        Returns:
            bool: True, если данные успешно загружены, False в противном случае.
        """
        try:
            self._df = pd.read_excel(self._filename)
            self._df['Error Code'] = pd.to_numeric(self._df['Error Code'], errors='coerce')
            return True
        except ValueError as e:
            self._load_data_error = f"ValueError: {e}"
        except KeyError as e:
            self._load_data_error = f"KeyError: {e}"
        return False

    def get_basic_info(self) -> Dict[str, str]:
        """
        Возвращает основную информацию о данных в виде HTML таблицы.

        Returns:
            Dict[str, str]: Словарь с данными, включая первые строки, количество уникальных кодов ошибок и
                самые часто встречающиеся ошибки.
        """
        if self._df is not None:
            basic_info = {
                'first_rows': self._df.head().to_html(index=False),
                'unique_error_codes': self._df['Error Code'].nunique(),
                'most_common_errors': self._get_most_common_errors_info()
            }
            return basic_info
        return None

    def _get_most_common_errors_info(self) -> str:
        """
        Возвращает информацию о самых часто встречающихся ошибках.

        Returns:
            str: HTML-представление информации о самых часто встречающихся ошибках.
        """
        most_common_errors_info = self._most_common_errors.to_frame(name='Count').reset_index()
        most_common_errors_info.columns = ['Error Code', 'Count']
        return most_common_errors_info.to_html(index=False)

    def visualize_data(self) -> pd.Series:
        """
        Визуализирует данные в виде гистограммы и круговой диаграммы, сохраняет графики в файлы.

        Returns:
            pd.Series: Самые часто встречающиеся ошибки.
        """
        if self._df is not None:
            plt.figure(figsize=(10, 6))
            sns.histplot(data=self._df, x='Error Code', bins=20, kde=True)
            plt.title('Error frequency histogram')
            plt.xlabel('Error code')
            plt.ylabel('Frequency')
            self.histogram_path = 'server/histogram.png'
            plt.savefig(self.histogram_path)
            plt.close()

            plt.figure(figsize=(8, 8))
            self._most_common_errors = self._df['Error Code'].value_counts().head(3)
            self._most_common_errors.plot.pie(autopct='%1.1f%%', startangle=90)
            plt.title('The most common mistakes')
            plt.ylabel('')
            self.pie_path = 'server/pie.png'
            plt.savefig(self.pie_path)
            plt.close()

            return self._most_common_errors
        return None

    def get_load_data_error(self) -> str | None:
        """
        Возвращает сообщение об ошибке при загрузке данных.

        Returns:
            str: Сообщение об ошибке при загрузке данных или None, если ошибки нет.
        """
        return self._load_data_error
