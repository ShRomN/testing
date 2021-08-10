from django.urls import path
# from . import views
from .views import user_login
from .views import AvailableTestsView
from .views import AdministerView
from .views import KettellQuestionView, KettellAnswerView
from .views import MMPIQuestionView, MMPIAnswerView
from .views import SCLQuestionView, SCLAnswerView
from .views import TSafetyQuestionView, TSafetyAnswerView
from .views import RPMQuestionView, RPMAnswerView
from .views import ComAnalogQuestionView, ComAnalogAnswerView

from .views import SummaryView
from .views import get_test_declaration, get_clarification_declaration
from .views import get_help

from .views import burdon

urlpatterns = [
    # Путь к странице со спискомдоступных тестов для тестирования
    path('list_available_tests', AvailableTestsView.as_view(), name='available_tests'),

    # Пути к тесту Кеттелла
    path('kettell_questions', KettellQuestionView.as_view(), name='questions'),
    path('kettell_answers/<id>', KettellAnswerView.as_view(), name='answers'),

    # Пути к тесту СМИЛ (MMPI)
    path('mmpi_questions', MMPIQuestionView.as_view(), name='questions'),
    path('mmpi_answers/<id>', MMPIAnswerView.as_view(), name='answers'),

    # Пути к тесту УСК
    path('scl_questions', SCLQuestionView.as_view(), name='questions'),
    path('scl_answers/<id>', SCLAnswerView.as_view(), name='answers'),

    # Пути к тесту прогрессивных матриц Равена
    path('rpm_questions', RPMQuestionView.as_view(), name='questions'),
    path('rpm_answers/<id>', RPMAnswerView.as_view(), name='answers'),

    # Пути к тесту сложных аналогий
    path('com_analog_questions', ComAnalogQuestionView.as_view(), name='questions'),
    path('com_analog_answers/<id>', ComAnalogAnswerView.as_view(), name='answers'),



    # Пути к тесту Бурдона
    path('burdon', burdon, name='burdon'),



    # Пути к тесту для подразделений транспортной безопасности
    path('tsafety_questions', TSafetyQuestionView.as_view(), name='questions'),
    path('tsafety_answers/<id>', TSafetyAnswerView.as_view(), name='answers'),

    # Путь к сводной таблицы по анализу всех пройденных тестов
    path('summary/<login>', SummaryView.as_view(), name='summary'),

    # Путь к странице администрирования приложения тестирования
    path('administer', AdministerView.as_view(), name='administer'),

    # Путь к генерации заявление на тестирование.
    path('testdocs/test_declaration/<user_id>', get_test_declaration, name='test_declaration'),

    # Путь к генерации заявления о разъяснении
    path('testdocs/clarification_declaration/<user_id>', get_clarification_declaration, name='clarification_declaration'),

    # Путь к генерации страницы с помощью
    path('help', get_help, name='help'),


    path('', user_login, name='index'),
]