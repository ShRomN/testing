from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
import json
from datetime import datetime

# Модели
from .models import InformationTestUser
from .models import KettellQuestion, KettellAnswer
from .models import MMPIQuestion, MMPIAnswer
from .models import SCLQuestion, SCLAnswer
from .models import TSafetyQuestion, TSafetyAnswer
from .models import RPMQuestion, RPMAnswer
from .models import ComAnalogQuestion, ComAnalogAnswer

from django.views.generic import View

# Авторизация
from .forms import UserLoginForm
from django.contrib.auth import login, logout

from django.contrib.auth.models import User

import os

# Загрузка вспомогательных ф-ций
from .utils import check_answers
from .utils import get_kettell_results
from .utils import get_mmpi_results
from .utils import get_scl_results
from .utils import get_rpm_results

from .utils import arr_reshape
from .utils import save_to_docx

import sys
sys.path.append("..")
from djapp.settings import BASE_DIR, MEDIA_ROOT

# from django.db.models import Q

# Подключения миксина для реализации различных разрешений
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

# Для выгрузки файлов заявлений
import io
from django.http import FileResponse 

# переменная для хранения каталога - tests в зависимости
# от режима запуска локальная отладка или продакшен
TESTS_DIR = os.environ.get("TESTS_DIR", default="djapp/")


def user_login(request):
    """Функция отображения стартовой страницы с авторизацией.

    """
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request=request, user=user)
            # Если пользователь 
            if user.is_staff:
                return redirect('/administer')
            else:
                return redirect('/list_available_tests')
    
    else:
        form = UserLoginForm()

    return render(
        request,
        'tests/login.html',
        context = {
            "title": "Вход",
            "form": form
        }
    )



class AvailableTestsView(View):
    """Класс обработки авторизационной страницы.

    """
    def get(self, request):

        # print(request.user.informationtestuser.get_user_name())

        # Если пользователь не залогинился переводим его на страницу входа
        if not request.user.is_authenticated:
            return redirect('/')

        # Варианты тестов:
        #   Тест Кеттелла
        #   Тест СМИЛ
        #   Тест УСК
        #   Тест для прогрессивных матриц Равена
        #   Тест для сложных аналогий
        #   Тест для подразделений транспортной безопасности

        # Если пользователь авторизован, то запрашиваем доступные для него тесты
        avalable_tests = request.user.informationtestuser.available_tests

        return render(
            request,
            'tests/list-tests.html',
            context = {
                "user_name": request.user.informationtestuser.get_user_name(),
                "title": "Список тестов",
                "avalable_tests": avalable_tests
            }
        )


# =================  Тест Кеттелла 16 PF  =================

class KettellQuestionView(View):
    """Класс обработки страницы вопросов теста Кеттелла.

    """
    def get(self, request):
        questions = KettellQuestion.objects.all().order_by("number")

        return render(
            request, 'tests/kettell.html', 
            context = {
                "user_name": request.user.informationtestuser.get_user_name(),
                "title": "Тест Кеттелла",
                'question_list': questions[:len(questions) - 1],
                'end_question': questions[len(questions) - 1]
            }
        )
    
    def post(self, request):

        user = InformationTestUser.objects.get(user_id=request.user)

        # Обрабатываем (проверяем) полученные ответы
        raw_answers = json.loads(request.POST['data'])

        # Создаем запись об ответе пользователя.
        answers = KettellAnswer(
            user_id=user,
            start_testing_dtime=datetime.fromtimestamp(float(request.POST['start_testing_dtime'])),
            end_testing_dtime=datetime.fromtimestamp(float(request.POST['end_testing_dtime'])),
            answers=json.loads(request.POST['data']),
            results=get_kettell_results(raw_answers)
        )
        # Сохраняем запись в БД.
        answers.save()

        # Запрашиваем данные о пользователе из модели - InformationTestUser
        user = answers.user_id
        
        # Отмечаем прохождение теста в модели - InformationTestUser
        # проходя по всем доступным тестам ища Тест Кеттелла
        tests = user.available_tests
        for test in tests:
            if test["name_test"] == "Тест Кеттелла":
                test["ended"] = True
                test["answer_id"] = answers.id

        # Сохраняем изменения в моделе - InformationTestUser в отношении пользователя
        user.save()

        # Разлогинивание пользователя
        logout(request)

        return HttpResponse(answers.id)

        
class KettellAnswerView(UserPassesTestMixin, View):
    """Класс обработки страницы ответов теста Кеттелла.

    """
    permission_denied_message = 'Доступ запрещен!'
    raise_exception = True


    def test_func(self):
        """Переопределение ф-ции - test_func из класса - UserPassesTestMixin
        для тестирования пользователя на значение поля - staff (является ли он
        пресоналом и на основании этого выполнять разрешение на запрос входа
        на данную страницу.

        """
        return self.request.user.is_staff


    def get(self, request, id):

        # Запрашиваем ответы из БД
        answer = KettellAnswer.objects.get(id__exact=id)


        # Удалить, это для отладки алгоритма расчетов
        # -------------------------------------------------
        answer.results = get_kettell_results(answer.answers)
        answer.save()
        # -------------------------------------------------

        
        out_list = list()
        # Перебираем массив ответов
        for key, value in answer.answers.items():

            question = KettellQuestion.objects.get(number__exact=int(key[2:]))

            text_answer = ""
            if (value == 'a'):
                text_answer = question.answer_a
            elif (value == 'b'):
                text_answer = question.answer_b
            else:
                text_answer = question.answer_c

            out_list.append([
                int(key[2:]),
                question.question,
                value,
                text_answer
            ])

        # if not answer.report:
        #     # Формируем имя выходного файла (с именем подкатолога - docx)
        #     out_filename = "docx/kettell_" + \
        #         answer.start_testing_dtime.strftime("%y-%m-%d_%H-%M") + \
        #         '_' + answer.user_id.user_id.username + ".docx"

        #     save_to_docx(
        #         TESTS_DIR + 'tests/docx_templates/kettell_template',
        #         MEDIA_ROOT / out_filename,
        #         context={
        #             'id': answer.user_id.uuid,
        #             'start_testing_dtime': answer.start_testing_dtime,
        #             'end_testing_dtime': answer.end_testing_dtime,
        #             'answers': arr_reshape(out_list, 6),
        #             'results': answer.results
        #         }
        #     )

        #     answer.report = out_filename
        #     answer.save()


        # Удалить, это для отладки алгоритма расчетов и раскоментировать предыдущий блок - if
        # -------------------------------------------------
        # Формируем имя выходного файла (с именем подкатолога - docx)
        out_filename = "docx/kettell_" + \
            answer.start_testing_dtime.strftime("%y-%m-%d_%H-%M") + \
            '_' + answer.user_id.user_id.username + ".docx"
        save_to_docx(
            TESTS_DIR + 'tests/docx_templates/kettell_template',
            MEDIA_ROOT / out_filename,
            context={
                'id': answer.user_id.uuid,
                'start_testing_dtime': answer.start_testing_dtime,
                'end_testing_dtime': answer.end_testing_dtime,
                'answers': arr_reshape(out_list, 6),
                'results': answer.results
            }
        )
        answer.report = out_filename
        answer.save()
        # -------------------------------------------------

        return render(
            request,
            # 'tests/kettell-answ.html',
            'tests/_kettell-answ.html',
            context={
                "user_name": "Администратор (" + request.user.username + ")",
                "title": "Ответы теста Кеттелла",
                'last_name': answer.user_id.last_name,
                'first_name': answer.user_id.first_name,
                'patronymic': answer.user_id.patronymic,
                'start_testing_dtime': answer.start_testing_dtime,
                'end_testing_dtime': answer.end_testing_dtime,
                'results': answer.results,
                'answers': out_list,
                'docx_url': answer.report.url
            }
        )

# =========================================================


# ===================  Тест СМИЛ (MMPI)  ==================

class MMPIQuestionView(View):
    """Класс обработки страницы вопросов теста СМИЛ (MMPI).

    """
    def get(self, request):
        questions = MMPIQuestion.objects.filter(
            gender=request.user.informationtestuser.gender
        ).order_by("number")

        return render(
            request, 'tests/mmpi.html', 
            context = {
                "user_name": request.user.informationtestuser.get_user_name(),
                "title": "Тест СМИЛ",
                'question_list': questions[:len(questions) - 1],
                'end_question': questions[len(questions) - 1]
            }
        )
    
    def post(self, request):

        user = InformationTestUser.objects.get(user_id=request.user)

        # Обрабатываем (проверяем) полученные ответы
        raw_answers = json.loads(request.POST['data'])

        # Определяем пол пользователя для последующей фильтрации по полу
        gender_user = request.user.informationtestuser.gender

        # Создаем запись об ответе пользователя.
        answers = MMPIAnswer(
            user_id=user,
            start_testing_dtime=datetime.fromtimestamp(float(request.POST['start_testing_dtime'])),
            end_testing_dtime=datetime.fromtimestamp(float(request.POST['end_testing_dtime'])),
            answers=json.loads(request.POST['data']),
            results=get_mmpi_results(raw_answers, gender_user)
        )

        # Сохраняем запись в БД.
        answers.save()

        # Запрашиваем данные о пользователе из модели - InformationTestUser
        user = answers.user_id
        
        # Отмечаем прохождение теста в модели - InformationTestUser
        # проходя по всем доступным тестам ища Тест Кеттелла
        tests = user.available_tests
        for test in tests:
            if test["name_test"] == "Тест СМИЛ":
                test["ended"] = True
                test["answer_id"] = answers.id
       
        # Сохраняем изменения в моделе - InformationTestUser в отношении пользователя
        user.save()

        # Разлогинивание пользователя
        logout(request)

        return HttpResponse(answers.id)

        
class MMPIAnswerView(UserPassesTestMixin, View):
    """Класс обработки страницы ответов теста СМИЛ (MMPI).

    """
    permission_denied_message = 'Доступ запрещен!'
    raise_exception = True


    def test_func(self):
        """Переопределение ф-ции - test_func из класса - UserPassesTestMixin
        для тестирования пользователя на значение поля - staff (является ли он
        пресоналом и на основании этого выполнять разрешение на запрос входа
        на данную страницу.

        """
        return self.request.user.is_staff


    def get(self, request, id):

        # Запрашиваем ответы из БД
        answer = MMPIAnswer.objects.get(id__exact=id)

        # Запрашиваем набор вопросов с фильтрацией в зависимости от пола
        questions = MMPIQuestion.objects.filter(
            gender=answer.user_id.gender
        )


        # Удалить, это для отладки алгоритма расчетов
        # -------------------------------------------------
        answer.results = get_mmpi_results(answer.answers, answer.user_id.gender)
        answer.save()
        # -------------------------------------------------


        out_list = list()
        # Перебираем массив ответов
        for key, value in answer.answers.items():
            question = questions.get(number__exact=int(key[2:]))

            text_answer = ""
            if (int(value) == 1):
                text_answer = "верно"
            else:
                text_answer = "неверно"

            out_list.append([
                int(key[2:]),
                question.question,
                value,
                text_answer
            ])

        # if not answer.report:
        #     # Формируем имя выходного файла (с именем подкатолога - docx)
        #     out_filename = "docx/mmpi_" + \
        #         answer.start_testing_dtime.strftime("%y-%m-%d_%H-%M") + \
        #         '_' + answer.user_id.user_id.username + ".docx"

        #     save_to_docx(
        #         TESTS_DIR + 'tests/docx_templates/mmpi_template',
        #         MEDIA_ROOT / out_filename,
        #         context={
        #             'id': answer.user_id.uuid,
        #             'start_testing_dtime': answer.start_testing_dtime,
        #             'end_testing_dtime': answer.end_testing_dtime,
        #             'answers': arr_reshape(out_list, 5),
        #             'results': answer.results
        #         }
        #     )

        #     answer.report = out_filename
        #     answer.save()


        # Удалить, это для отладки алгоритма расчетов и раскоментировать предыдущий блок - if
        # -------------------------------------------------
        # Формируем имя выходного файла (с именем подкатолога - docx)
        out_filename = "docx/mmpi_" + \
            answer.start_testing_dtime.strftime("%y-%m-%d_%H-%M") + \
            '_' + answer.user_id.user_id.username + ".docx"
        save_to_docx(
            TESTS_DIR + 'tests/docx_templates/mmpi_template',
            MEDIA_ROOT / out_filename,
            context={
                'id': answer.user_id.uuid,
                'start_testing_dtime': answer.start_testing_dtime,
                'end_testing_dtime': answer.end_testing_dtime,
                'answers': arr_reshape(out_list, 5),
                'results': answer.results
            }
        )
        answer.report = out_filename
        answer.save()
        # -------------------------------------------------

        return render(
            request,
            # 'tests/mmpi-answ.html',
            'tests/_mmpi-answ.html',
            context={
                "user_name": "Администратор (" + request.user.username + ")",
                'title': "Ответы теста СМИЛ",
                'last_name': answer.user_id.last_name,
                'first_name': answer.user_id.first_name,
                'patronymic': answer.user_id.patronymic,
                'start_testing_dtime': answer.start_testing_dtime,
                'end_testing_dtime': answer.end_testing_dtime,
                'results': answer.results,
                'answers': out_list,
                'docx_url': answer.report.url
            }
        )

# =========================================================


# =========  Тест УСК (Subjective Control Level)  =========

class SCLQuestionView(View):
    """Класс обработки страницы вопросов теста УСК.

    """
    def get(self, request):
        questions = SCLQuestion.objects.all().order_by("number")

        return render(
            request, 'tests/scl.html', 
            context = {
                "user_name": request.user.informationtestuser.get_user_name(),
                "title": "Тест УСК",
                'question_list': questions[:len(questions) - 1],
                'end_question': questions[len(questions) - 1]
            }
        )
    
    def post(self, request):

        user = InformationTestUser.objects.get(user_id=request.user)

        # Обрабатываем (проверяем) полученные ответы
        raw_answers = json.loads(request.POST['data'])

        # Создаем запись об ответе пользователя.
        answers = SCLAnswer(
            user_id=user,
            start_testing_dtime=datetime.fromtimestamp(float(request.POST['start_testing_dtime'])),
            end_testing_dtime=datetime.fromtimestamp(float(request.POST['end_testing_dtime'])),
            answers=json.loads(request.POST['data']),
            results=get_scl_results(raw_answers)
        )

        # Сохраняем запись в БД.
        answers.save()

        # Запрашиваем данные о пользователе из модели - InformationTestUser
        user = answers.user_id
        
        # Отмечаем прохождение теста в модели - InformationTestUser
        # проходя по всем доступным тестам ища Тест Кеттелла
        tests = user.available_tests
        for test in tests:
            if test["name_test"] == "Тест УСК":
                test["ended"] = True
                test["answer_id"] = answers.id

        # Сохраняем изменения в моделе - InformationTestUser в отношении пользователя
        user.save()

        # Разлогинивание пользователя
        logout(request)

        return HttpResponse(answers.id)

        
class SCLAnswerView(UserPassesTestMixin, View):
    """Класс обработки страницы ответов теста УСК.

    """
    permission_denied_message = 'Доступ запрещен!'
    raise_exception = True


    def test_func(self):
        """Переопределение ф-ции - test_func из класса - UserPassesTestMixin
        для тестирования пользователя на значение поля - staff (является ли он
        пресоналом и на основании этого выполнять разрешение на запрос входа
        на данную страницу.

        """
        return self.request.user.is_staff


    def get(self, request, id):

        # Запрашиваем ответы из БД
        answer = SCLAnswer.objects.get(id__exact=id)
        
        out_list = list()
        # Перебираем массив ответов
        for key, value in answer.answers.items():
            question = SCLQuestion.objects.get(number__exact=int(key[2:]))

            text_answer = ""
            if (int(value) == 1):
                text_answer = "верно"
            else:
                text_answer = "неверно"

            out_list.append([
                int(key[2:]),
                question.question,
                value,
                text_answer
            ])


        # Удалить, это для отладки алгоритма расчетов
        # -------------------------------------------------
        answer.results = get_scl_results(answer.answers)
        answer.save()
        # -------------------------------------------------

        # if not answer.report:
        #     # Формируем имя выходного файла (с именем подкатолога - docx)
        #     out_filename = "docx/scl_" + \
        #         answer.start_testing_dtime.strftime("%y-%m-%d_%H-%M") + \
        #         '_' + answer.user_id.user_id.username + ".docx"

        #     save_to_docx(
        #         TESTS_DIR + 'tests/docx_templates/scl_template',
        #         MEDIA_ROOT / out_filename,
        #         context={
        #             'id': answer.user_id.uuid,
        #             'start_testing_dtime': answer.start_testing_dtime,
        #             'end_testing_dtime': answer.end_testing_dtime,
        #             'answers': out_list,
        #             'results': answer.results
        #         }
        #     )

        #     answer.report = out_filename
        #     answer.save()


        # Удалить, это для отладки алгоритма расчетов и раскоментировать предыдущий блок - if
        # -------------------------------------------------
        # Формируем имя выходного файла (с именем подкатолога - docx)
        out_filename = "docx/scl_" + \
            answer.start_testing_dtime.strftime("%y-%m-%d_%H-%M") + \
            '_' + answer.user_id.user_id.username + ".docx"
        save_to_docx(
            TESTS_DIR + 'tests/docx_templates/scl_template',
            MEDIA_ROOT / out_filename,
            context={
                'id': answer.user_id.uuid,
                'start_testing_dtime': answer.start_testing_dtime,
                'end_testing_dtime': answer.end_testing_dtime,
                'answers': out_list,
                'results': answer.results
            }
        )
        answer.report = out_filename
        answer.save()
        # -------------------------------------------------


        return render(
            request,
            # 'tests/scl-answ.html',
            'tests/_scl-answ.html',
            context={
                "user_name": "Администратор (" + request.user.username + ")",
                'title': "Ответы теста УСК",
                'last_name': answer.user_id.last_name,
                'first_name': answer.user_id.first_name,
                'patronymic': answer.user_id.patronymic,
                'start_testing_dtime': answer.start_testing_dtime,
                'end_testing_dtime': answer.end_testing_dtime,
                'results': answer.results,
                'answers': out_list,
                'docx_url': answer.report.url
            }
        )

# =========================================================


# ===========  Тест прогрессивных матриц Равена ===========

class RPMQuestionView(View):
    """Класс обработки страницы вопросов теста для прогрессивных матриц Равена.

    """
    def get(self, request):
        questions = RPMQuestion.objects.all().order_by("number")

        return render(
            request, 'tests/rpm.html', 
            context = {
                "user_name": request.user.informationtestuser.get_user_name(),
                "title": "Матрицы Равена",
                'question_list': questions[:len(questions) - 1],
                'end_question': questions[len(questions) - 1]
            }
        )

    
    def post(self, request):

        # Формируем словарь правельных ответов
        true_answers = {}
        questions = RPMQuestion.objects.all().order_by("number")
        for question in questions:
            true_answers.update({'a_' + str(question.number): question.correct_answer})

        # Обрабатываем (проверяем) полученные ответы
        raw_answers = json.loads(request.POST['data'])

        # Проверяем данные пользователем ответы на правильность
        # checked_answers = check_answers(raw_answers, true_answers)


        # Запрашиваем данные о пользователе 
        user = InformationTestUser.objects.get(user_id=request.user)

        # Создаем запись об ответе пользователя.
        answers = RPMAnswer(
            user_id=user,
            start_testing_dtime=datetime.fromtimestamp(float(request.POST['start_testing_dtime'])),
            end_testing_dtime=datetime.fromtimestamp(float(request.POST['end_testing_dtime'])),
            # answers=checked_answers[0],
            answers=raw_answers,
            results=get_rpm_results(raw_answers)
        )

        # Сохраняем запись в БД.
        answers.save()

        # Запрашиваем данные о пользователе из модели - InformationTestUser
        user = answers.user_id
        
        # Отмечаем прохождение теста в модели - InformationTestUser
        # проходя по всем доступным тестам ища Тест для прогрессивных матриц Равена
        tests = user.available_tests
        for test in tests:
            if test["name_test"] == "Тест для прогрессивных матриц Равена":
                test["ended"] = True
                test["answer_id"] = answers.id
       
        # Сохраняем изменения в моделе - InformationTestUser в отношении пользователя
        user.save()

        # Разлогинивание пользователя
        logout(request)

        return HttpResponse(answers.id)

        
class RPMAnswerView(UserPassesTestMixin, View):
    """Класс обработки страницы ответов теста для прогрессивных матриц Равена.

    """
    permission_denied_message = 'Доступ запрещен!'
    raise_exception = True


    def test_func(self):
        """Переопределение ф-ции - test_func из класса - UserPassesTestMixin
        для тестирования пользователя на значение поля - staff (является ли он
        пресоналом и на основании этого выполнять разрешение на запрос входа
        на данную страницу.

        """
        return self.request.user.is_staff


    def get(self, request, id):

        # Запрашиваем ответы из БД
        answer = RPMAnswer.objects.get(id__exact=id)

        # out_list = list()
        # # Перебираем массив ответов
        # for key, value in answer.answers.items():
        #     question = RPMQuestion.objects.get(number__exact=int(key[2:]))

        #     out_list.append([
        #         int(key[2:]),
        #         question.group,
        #         int(value['answer']),
        #         value['is_true']
        #     ])


        # Удалить, это для отладки алгоритма расчетов
        # -------------------------------------------------
        answer.results = get_rpm_results(answer.answers)
        answer.save()
        # -------------------------------------------------


        if not answer.report:
            # Формируем имя выходного файла (с именем подкатолога - docx)
            out_filename = "docx/rpm_" + \
                answer.start_testing_dtime.strftime("%y-%m-%d_%H-%M") + \
                '_' + answer.user_id.user_id.username + ".docx"

            save_to_docx(
                TESTS_DIR + 'tests/docx_templates/rpm_template',
                MEDIA_ROOT / out_filename,
                context={
                    'id': answer.user_id.uuid,
                    'start_testing_dtime': answer.start_testing_dtime,
                    'end_testing_dtime': answer.end_testing_dtime,
                    # 'answers': arr_reshape(out_list, 12),
                    'results': answer.results
                }
            )

            answer.report = out_filename
            answer.save()


        # # Удалить, это для отладки алгоритма расчетов и раскоментировать предыдущий блок - if
        # # -------------------------------------------------
        # # Формируем имя выходного файла (с именем подкатолога - docx)
        # out_filename = "docx/rpm_" + \
        #     answer.start_testing_dtime.strftime("%y-%m-%d_%H-%M") + \
        #     '_' + answer.user_id.user_id.username + ".docx"
        # save_to_docx(
        #     TESTS_DIR + 'tests/docx_templates/rpm_template',
        #     MEDIA_ROOT / out_filename,
        #     context={
        #         'id': answer.user_id.uuid,
        #         'start_testing_dtime': answer.start_testing_dtime,
        #         'end_testing_dtime': answer.end_testing_dtime,
        #         'answers': arr_reshape(out_list, 12),
        #         'results': answer.results
        #     }
        # )
        # answer.report = out_filename
        # answer.save()
        # # -------------------------------------------------


        return render(
            request,
            # 'tests/rpm-answ.html',
            'tests/_rpm-answ.html',
            context={
                "user_name": "Администратор (" + request.user.username + ")",
                'title': 'Ответы теста прогрессивных матриц Равена',
                'last_name': answer.user_id.last_name,
                'first_name': answer.user_id.first_name,
                'patronymic': answer.user_id.patronymic,
                'start_testing_dtime': answer.start_testing_dtime,
                'end_testing_dtime': answer.end_testing_dtime,
                # 'answers': out_list,
                # 'answers': answer.answers,
                'results': answer.results,
                'docx_url': answer.report.url
            }
        )

# =========================================================


# ================  Тест сложные аналогии =================

class ComAnalogQuestionView(View):
    """Класс обработки страницы вопросов теста для сложных аналогий.

    """
    def get(self, request):
        questions = ComAnalogQuestion.objects.all().order_by("number")

        return render(
            request, 'tests/com-analog.html', 
            context = {
                "user_name": request.user.informationtestuser.get_user_name(),
                "title": "Сложнае аналогии",
                'question_list': questions[:len(questions) - 1],
                'end_question': questions[len(questions) - 1]
            }
        )
    
    def post(self, request):

        # Формируем словарь правельных ответов
        true_answers = {}
        questions = ComAnalogQuestion.objects.all().order_by("number")
        for question in questions:
            true_answers.update({'a_' + str(question.number): question.correct_answer})

        # Обрабатываем (проверяем) полученные ответы
        raw_answers = json.loads(request.POST['data'])

        # Проверяем данные пользователем ответы на правильность
        checked_answers = check_answers(raw_answers, true_answers)

        # Запрашиваем данные о пользователе 
        user = InformationTestUser.objects.get(user_id=request.user)

        # Создаем запись об ответе пользователя.
        answers = ComAnalogAnswer(
            user_id=user,
            start_testing_dtime=datetime.fromtimestamp(float(request.POST['start_testing_dtime'])),
            end_testing_dtime=datetime.fromtimestamp(float(request.POST['end_testing_dtime'])),
            answers=checked_answers[0],
            results={
                'total_answers': len(checked_answers[0]),
                'total_correct_answers': checked_answers[1]
            }
        )

        # Сохраняем запись в БД.
        answers.save()

        # Запрашиваем данные о пользователе из модели - InformationTestUser
        user = answers.user_id
        
        # Отмечаем прохождение теста в модели - InformationTestUser
        # проходя по всем доступным тестам ища Тест для сложных аналогий
        tests = user.available_tests
        for test in tests:
            if test["name_test"] == "Тест для сложных аналогий":
                test["ended"] = True
                test["answer_id"] = answers.id
       
        # Сохраняем изменения в моделе - InformationTestUser в отношении пользователя
        user.save()

        # Разлогинивание пользователя
        logout(request)

        return HttpResponse(answers.id)

        
class ComAnalogAnswerView(UserPassesTestMixin, View):
    """Класс обработки страницы ответов теста для сложных аналогий.

    """
    permission_denied_message = 'Доступ запрещен!'
    raise_exception = True


    def test_func(self):
        """Переопределение ф-ции - test_func из класса - UserPassesTestMixin
        для тестирования пользователя на значение поля - staff (является ли он
        пресоналом и на основании этого выполнять разрешение на запрос входа
        на данную страницу.

        """
        return self.request.user.is_staff


    def get(self, request, id):

        # Запрашиваем ответы из БД
        answer = ComAnalogAnswer.objects.get(id__exact=id)

        out_list = list()
        # Перебираем массив ответов
        for key, value in answer.answers.items():
            question = ComAnalogQuestion.objects.get(number__exact=int(key[2:]))
            
            text_answer = ""
            if (value['answer'] == 'А'):
                text_answer = "Овца-стадо"
            elif (value['answer'] == "Б"):
                text_answer = "Малина-ягода"
            elif (value['answer'] == "В"):
                text_answer = "Море-океан"
            elif (value['answer'] == "Г"):
                text_answer = "Свет-темнота"
            elif (value['answer'] == "Д"):
                text_answer = "Отравление-смерть"
            else:
                text_answer = "Враг-неприятель"

            out_list.append([
                int(key[2:]),
                question.question,
                text_answer,
                value['answer'],
                value['is_true']
            ])

        if not answer.report:
            # Формируем имя выходного файла (с именем подкатолога - docx)
            out_filename = "docx/com_analog_" + \
                answer.start_testing_dtime.strftime("%y-%m-%d_%H-%M") + \
                '_' + answer.user_id.user_id.username + ".docx"

            # save_to_docx(
            #     TESTS_DIR + 'tests/docx_templates/com_analog_template',
            #     MEDIA_ROOT / out_filename,
            #     context={
            #         'id': answer.user_id.last_name,
            #         'first_name': answer.user_id.first_name,
            #         'patronymic': answer.user_id.patronymic,
            #         'start_testing_dtime': answer.start_testing_dtime,
            #         'end_testing_dtime': answer.end_testing_dtime,
            #         'answers': out_list,
            #         'total_answers': answer.results['total_answers'],
            #         'total_correct_answers': answer.results['total_correct_answers']
            #     }
            # )

            save_to_docx(
                TESTS_DIR + 'tests/docx_templates/com_analog_template',
                MEDIA_ROOT / out_filename,
                context={
                    'id': answer.user_id.uuid,
                    'start_testing_dtime': answer.start_testing_dtime,
                    'end_testing_dtime': answer.end_testing_dtime,
                    'answers': out_list,
                    'total_answers': answer.results['total_answers'],
                    'total_correct_answers': answer.results['total_correct_answers']
                }
            )

            answer.report = out_filename
            answer.save()

        return render(
            request,
            'tests/com-analog-answ.html',
            context={
                "user_name": "Администратор (" + request.user.username + ")",
                'title': "Ответы теста сложных аналогий",
                'last_name': answer.user_id.last_name,
                'first_name': answer.user_id.first_name,
                'patronymic': answer.user_id.patronymic,
                'start_testing_dtime': answer.start_testing_dtime,
                'end_testing_dtime': answer.end_testing_dtime,
                'answers': out_list,
                'total_answers': answer.results['total_answers'],
                'total_correct_answers': answer.results['total_correct_answers'],
                'docx_url': answer.report.url
            }
        )

# =========================================================


def burdon(request):
    """Ф-ция генерирующая тест Бурдона.

    """
    text = "Lorem ipsum — классический текст-«рыба» (условный, зачастую бессмысленный текст-заполнитель, вставляемый в макет страницы). Является искажённым отрывком из философского трактата Марка Туллия Цицерона «О пределах добра и зла», написанного в 45 году до н. э. на латинском языке, обнаружение сходства приписывается Ричарду МакКлинтоку[1]. Распространился в 1970-х годах из-за трафаретов компании Letraset, a затем — из-за того, что служил примером текста в программе PageMaker. Испорченный текст, вероятно, происходит от его издания в Loeb Classical Library 1914 года, в котором слово dolorem разбито переносом так, что страница 36 начинается с lorem ipsum… (do- осталось на предыдущей)"
    return render(
        request,
        'tests/burdon.html',
        context={
            'text':text
        }
    )





# ===  Тест для подразделений транспортной безопасности ===

class TSafetyQuestionView(View):
    """Класс обработки страницы вопросов теста для подразделений транспортной безопасности.

    """
    def get(self, request):
        # Запрашиваем все вопросы из теста
        # questions = TSafetyQuestion.objects.all().order_by("number")


        # kwargs = {
        #     '{0}__{1}'.format('name', 'startswith'): 'A',
        #     '{0}__{1}'.format('name', 'endswith'): 'Z'
        # }

        # Person.objects.filter(**kwargs)
        # questions = TSafetyQuestion.objects.get(Q(number__exact=5) | Q(number__exact=10)).order_by("number")
        
        # question_1 = questions.filter(Q(number__exact=2) | Q(number__exact=5))


        # Запрашиваем данные о пользователе 
        user = InformationTestUser.objects.get(user_id=request.user)

        # проходя по всем доступным тестам ища Тест для подразделений транспортной безопасности
        tests = user.available_tests

        list_questions = []
        for test in tests:
            if test["name_test"] == "Тест для подразделений транспортной безопасности":
                list_questions = test["numbers_questions"]

        # Формируем часть строки SQL запроса на основании массива требуемых вопросов
        out_str = ''
        for item in list_questions:
            out_str += 'number = ' + str(item) + ' OR '

        # print(out_str[:-4])
        # Запрашиваем вопросы из базы формируя полную строку SQL запроса
        questions = TSafetyQuestion.objects.raw(
            'SELECT * FROM tests_tsafetyquestion WHERE ' + out_str[:-4]
        )

        return render(
            request, 'tests/tsafety.html', 
            context = {
                "user_name": request.user.informationtestuser.get_user_name(),
                "title": "Транспортная безопасность",
                'question_list': questions[:len(questions) - 1],
                'end_question': questions[len(questions) - 1]
            }
        )

    
    def post(self, request):
        # Запрашиваем данные о пользователе 
        user = InformationTestUser.objects.get(user_id=request.user)

        # проходя по всем доступным тестам ища Тест для подразделений транспортной безопасности
        tests = user.available_tests

        list_questions = []
        for test in tests:
            if test["name_test"] == "Тест для подразделений транспортной безопасности":
                list_questions = test["numbers_questions"]

        # Формируем часть строки SQL запроса на основании массива требуемых вопросов
        out_str = ''
        for item in list_questions:
            out_str += 'number = ' + str(item) + ' OR '

        # print(out_str[:-4])
        # Запрашиваем вопросы из базы формируя полную строку SQL запроса
        questions = TSafetyQuestion.objects.raw(
            'SELECT * FROM tests_tsafetyquestion WHERE ' + out_str[:-4]
        )

        # Формируем словарь правельных ответов
        true_answers = {}
        # questions = TSafetyQuestion.objects.all().order_by("number")

        for question in questions:
            true_answers.update({'a_' + str(question.number): question.correct_answer})

        # Обрабатываем (проверяем) полученные ответы
        raw_answers = json.loads(request.POST['data'])

        # Проверяем данные пользователем ответы на правильность
        checked_answers = check_answers(raw_answers, true_answers)

        # Запрашиваем данные о пользователе 
        user = InformationTestUser.objects.get(user_id=request.user)

        # Создаем запись об ответе пользователя.
        answers = TSafetyAnswer(
            user_id=user,
            start_testing_dtime=datetime.fromtimestamp(float(request.POST['start_testing_dtime'])),
            end_testing_dtime=datetime.fromtimestamp(float(request.POST['end_testing_dtime'])),
            answers=checked_answers[0],
            results={
                'total_answers': len(checked_answers[0]),
                'total_correct_answers': checked_answers[1]
            }
        )

        # Сохраняем запись в БД.
        answers.save()

        # Запрашиваем данные о пользователе из модели - InformationTestUser
        user = answers.user_id
        
        # Отмечаем прохождение теста в модели - InformationTestUser
        # проходя по всем доступным тестам ища Тест для подразделений транспортной безопасности
        tests = user.available_tests
        for test in tests:
            if test["name_test"] == "Тест для подразделений транспортной безопасности":
                test["ended"] = True
                test["answer_id"] = answers.id
       
        # Сохраняем изменения в моделе - InformationTestUser в отношении пользователя
        user.save()

        # Разлогинивание пользователя
        logout(request)

        return HttpResponse(answers.id)

        
class TSafetyAnswerView(UserPassesTestMixin, View):
    """Класс обработки страницы ответов теста для подразделений транспортной безопасности.

    """
    permission_denied_message = 'Доступ запрещен!'
    raise_exception = True


    def test_func(self):
        """Переопределение ф-ции - test_func из класса - UserPassesTestMixin
        для тестирования пользователя на значение поля - staff (является ли он
        пресоналом и на основании этого выполнять разрешение на запрос входа
        на данную страницу.

        """
        return self.request.user.is_staff


    def get(self, request, id):

        # Запрашиваем ответы из БД
        answer = TSafetyAnswer.objects.get(id__exact=id)

        out_list = list()
        # Перебираем массив ответов
        for key, value in answer.answers.items():
            question = TSafetyQuestion.objects.get(number__exact=int(key[2:]))

            text_answer = ""
            if (int(value['answer']) == 1):
                text_answer = question.answer_1
            elif (int(value['answer']) == 2):
                text_answer = question.answer_2
            elif (int(value['answer']) == 3):
                text_answer = question.answer_3
            else:
                text_answer = question.answer_4

            out_list.append([
                int(key[2:]),
                question.question,
                int(value['answer']),
                text_answer,
                value['is_true']
            ])

        return render(
            request,
            'tests/tsafety-answ.html',
            context={
                "user_name": "Администратор (" + request.user.username + ")",
                'title': "Ответы теста транспортной безопасности",
                'last_name': answer.user_id.last_name,
                'first_name': answer.user_id.first_name,
                'patronymic': answer.user_id.patronymic,
                'start_testing_dtime': answer.start_testing_dtime,
                'end_testing_dtime': answer.end_testing_dtime,
                'answers': out_list,
                'total_answers': answer.results['total_answers'],
                'total_correct_answers': answer.results['total_correct_answers']
            }
        )

# =========================================================


# ==  Сводная таблица по анализу всех пройденных тестов  ==

class SummaryView(UserPassesTestMixin, View):
    """Класс обработки страницы со сводной таблицей по анализу
    всех пройденных тестов.

    """
    permission_denied_message = 'Доступ запрещен!'
    raise_exception = True


    def test_func(self):
        """Переопределение ф-ции - test_func из класса - UserPassesTestMixin
        для тестирования пользователя на значение поля - staff (является ли он
        пресоналом и на основании этого выполнять разрешение на запрос входа
        на данную страницу.

        """
        return self.request.user.is_staff


    def get(self, request, login):

        # Запрашиваем список доступных для тестирования данных из
        # модели - InformationTestUser для пользователя имя которого
        # передано как параметр (login) в запросе.
        user = User.objects.get(username=login)
        # print(user)
        tests = user.informationtestuser.available_tests
        # print(tests)
        # print(user.informationtestuser.user_id)
        # print(KettellAnswer.objects.get(user_id=1))

        kettel_answ = 0
        mmpi_answ = 0
        scl_answ = 0
        rpm_answ = 0
        com_analog_answ = 0
        t_safety_answ = 0

        # for test in tests:
        #     if test["name_test"] == "Тест Кеттелла" and test["ended"]:
        #         kettel_answ = KettellAnswer.objects.filter(user_id=user.id).order_by("-id")[0]
        #     elif test["name_test"] == "Тест СМИЛ" and test["ended"]:
        #         mmpi_answ = MMPIAnswer.objects.filter(user_id=user.id).order_by("-id")[0]
        #     elif test["name_test"] == "Тест УСК" and test["ended"]:
        #         scl_answ = SCLAnswer.objects.filter(user_id=user.id).order_by("-id")[0]
        #     elif test["name_test"] == "Тест для прогрессивных матриц Равена" and test["ended"]:
        #         rpm_answ = RPMAnswer.objects.filter(user_id=user.id).order_by("-id")[0]
        #     elif test["name_test"] == "Тест для сложных аналогий" and test["ended"]:
        #         com_analog_answ = ComAnalogAnswer.objects.filter(user_id=user.id).order_by("-id")[0]
        #     elif test["name_test"] == "Тест для подразделений транспортной безопасности" and test["ended"]:
        #         t_safety_answ = TSafetyAnswer.objects.filter(user_id=user.id).order_by("-id")[0]

        for test in tests:
            if test["name_test"] == "Тест Кеттелла" and test["ended"]:
                kettel_answ = KettellAnswer.objects.get(id=test["answer_id"])
            elif test["name_test"] == "Тест СМИЛ" and test["ended"]:
                mmpi_answ = MMPIAnswer.objects.get(id=test["answer_id"])
            elif test["name_test"] == "Тест УСК" and test["ended"]:
                scl_answ = SCLAnswer.objects.get(id=test["answer_id"])
            elif test["name_test"] == "Тест для прогрессивных матриц Равена" and test["ended"]:
                rpm_answ = RPMAnswer.objects.get(id=test["answer_id"])
            elif test["name_test"] == "Тест для сложных аналогий" and test["ended"]:
                com_analog_answ = ComAnalogAnswer.objects.get(id=test["answer_id"])
            elif test["name_test"] == "Тест для подразделений транспортной безопасности" and test["ended"]:
                t_safety_answ = TSafetyAnswer.objects.get(id=test["answer_id"])

        # # Общая таблица по результатам всех тестов
        # return render(
        #     request,
        #     'tests/summary.html',
        #     context={
        #         'user': user.informationtestuser,
        #         'kettel': kettel_answ,
        #         'mmpi': mmpi_answ,
        #         'scl': scl_answ,
        #         'rpm': rpm_answ,
        #         'com_analog': com_analog_answ,
        #         't_safety': t_safety_answ
        #     }
        # )

        return render(
            request,
            'tests/summary-2.html',
            context={
                "user_name": "Администратор (" + request.user.username + ")",
                'user': user.informationtestuser,
                'kettel': kettel_answ,
                'mmpi': mmpi_answ,
                'scl': scl_answ,
                'com_analog': com_analog_answ,
                'rpm': rpm_answ
            }
        )

# =========================================================


# ==  Страница администрирования приложения тестирования  ==

class AdministerView(UserPassesTestMixin, View):
    """Класс обработки страницы администрирования приложения тестирования.

    """
    permission_denied_message = 'Доступ запрещен!'
    raise_exception = True


    def test_func(self):
        """Переопределение ф-ции - test_func из класса - UserPassesTestMixin
        для тестирования пользователя на значение поля - staff (является ли он
        пресоналом и на основании этого выполнять разрешение на запрос входа
        на данную страницу.

        """
        return self.request.user.is_staff


    def get(self, request):

        users = InformationTestUser.objects.all()

        return render(
            request,
            'tests/administer.html',
            context={
                "user_name": "Администратор (" + request.user.username + ")",
                'users': users
            }
        )
# ==========================================================


def get_test_declaration(request, user_id):
    """Ф-ция генерирующая заявление на тестирование.

    """
    user = InformationTestUser.objects.get(user_id=user_id)
    # Формируем имя выходного файла (с именем подкатолога - docx)
    out_filename = "docx/test_declaration_" + \
        user.user_id.username + ".docx"

    save_to_docx(
        TESTS_DIR + 'tests/docx_templates/test_declaration_template',
        MEDIA_ROOT / out_filename,
        context={
            'id': user.uuid
        }
    )

    return FileResponse(open(MEDIA_ROOT / out_filename, 'rb'))


def get_clarification_declaration(request, user_id):
    """Ф-ция генерирующая заявление о разъяснении.

    """
    user = InformationTestUser.objects.get(user_id=user_id)
    # Формируем имя выходного файла (с именем подкатолога - docx)
    out_filename = "docx/clarification_declaration_" + \
        user.user_id.username + ".docx"

    save_to_docx(
        TESTS_DIR + 'tests/docx_templates/clarification_declaration_template',
        MEDIA_ROOT / out_filename,
        context={
            'id': user.uuid
        }
    )

    return FileResponse(open(MEDIA_ROOT / out_filename, 'rb'))


def get_help(request):
    """Ф-ция генерирующая страницу помощи.

    """
    return render(
        request,
        'tests/help.html',
        context={
            'title': 'Помощь'
        }
    )
# ==========================================================