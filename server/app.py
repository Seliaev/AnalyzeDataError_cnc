from flask import Flask, render_template, send_file, request
from analyzer.analyzer import ErrorDataAnalyzer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index() -> render_template:
    """
    Обработчик маршрута '/' для отображения стартовой страницы.

    Методы:
        - GET: Отображает стартовую страницу.
        - POST: Обрабатывает загрузку файла, анализирует данные и отображает результат.

    Returns:
        HTML страницу с формой для загрузки файла и результатом анализа данных.
    """
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            analyzer = ErrorDataAnalyzer(file)
            if analyzer.load_data():
                analyzer.visualize_data()
                basic_info = analyzer.get_basic_info()
                return render_template('index.html', basic_info=basic_info, histogram_path='histogram', pie_path='pie')
            else:
                load_data_error = analyzer.get_load_data_error()
                return render_template('index.html', load_data_error=load_data_error, basic_info=None,
                                       histogram_path=None, pie_path=None)

    return render_template('index.html', basic_info=None, histogram_path=None, pie_path=None)

@app.route('/plot/<path:filename>')
def plot(filename) -> send_file:
    """
    Обработчик маршрута '/plot/<filename>' для отображения графиков.

    Attributes:
        filename (str): Имя файла для построения графиков.

    Returns:
        PNG изображение с графиком.
    """
    return send_file(f'{filename}.png', mimetype='image/png')
