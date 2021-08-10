from django.db import models
from django.utils import timezone

from django.conf import settings
from django.contrib.auth.models import User

import uuid

GENDER = [
    (1, 'МУЖСКОЙ'),
    (2, 'ЖЕНСКИЙ')
]

class InformationTestUser(models.Model):
    """Класс перечня доступных для пользователя тестов.

    """
    # Уровни профессионально важных качеств (Professionally important qualities)
    # PIQ_LEVELS = [
    #     (1, 'ПВК 1'),
    #     (2, 'ПВК 2'),
    #     (3, 'ПВК 3'),
    #     (4, 'ПВК 4'),
    #     (5, 'ПВК 5'),
    #     (6, 'ПВК 6'),
    #     (7, 'ПВК 7'),
    #     (8, 'ПВК 8'),
    # ]

    PIQ_LEVELS = [
        (3, 'ПВК III'),
        (4, 'ПВК IV'),
        (5, 'ПВК V'),
        (6, 'ПВК VI'),
        (7, 'ПВК VII')
    ]

    # Поля
    # Поле связи таблицы со стандартной таблицей пользователей
    user_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='user_id',
        verbose_name='Идентификатор пользователя:',
        help_text='Идентификатор пользователя.'
    )

    # Фамилия пользователя
    last_name = models.CharField(
        db_column='last_name',
        verbose_name='Фамилия:',
        help_text='Фамилия.',
        max_length=20,
        default=""
    )

    # Имя пользователя
    first_name = models.CharField(
        db_column='first_name',
        verbose_name='Имя:',
        help_text='Имя.',
        max_length=20,
        default=""
    )

    # Отчество пользователя
    patronymic = models.CharField(
        db_column='patronymic',
        verbose_name='Отчество:',
        help_text='Отчество.',
        max_length=20,
        default=""
    )

    # Идентификатор пользователя
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name='UUID пользователя:',
        help_text='UUID пользователя.'
    )

    # Признак половой принадлежности вопроса:
    #   1 - мужской;
    #   2 - женский.
    gender = models.IntegerField(
        db_column='gender',
        choices=GENDER,
        verbose_name='Пол пользователя:',
        help_text='Пол пользователя.',
        default=1
    )

    # Признак требуемого уровня ПВК по которому будет осуществляться тестирование:
    #   1 - ПВК 1;
    #   2 - ПВК 2;
    #   3 - ПВК 3;
    #   4 - ПВК 4;
    #   5 - ПВК 5;
    #   6 - ПВК 6;
    #   7 - ПВК 7;
    #   8 - ПВК 8.
    piq = models.IntegerField(
        db_column='piq',
        choices=PIQ_LEVELS,
        verbose_name='Уровень ПВК:',
        help_text='Уровень ПВК.',
        default=0
    )

    # Пример формирования JSON поля - available_tests
    #  
    # [
    # {"name_test": "Тест Кеттелла", "ended": false},
    # {"name_test": "Тест СМИЛ", "ended": true},
    # {"name_test": "Тест УСК", "ended": false},
    # {"name_test": "Тест для подразделений транспортной безопасности", "ended": true},
    # {"name_test": "Тест для сложных аналогий", "ended": false},
    # {"name_test": "Тест для прогрессивных матриц Равена", "ended": true}
    # ]
    # 
    # где:
    #   name_test - имя доступного теста;
    #   ended - отметка о прохождении тестирования (true - пройдено, false - непройдено).
    available_tests = models.JSONField(
        db_column='available_tests',
        verbose_name='Список доступных для пользователя тестов и отметка о их прохождении:',
        help_text='Список доступных для пользователя тестов и отметка о их прохождении:',
        default=dict
    )

    
    def get_user_name(self):
        """Функция получения ФИО пользователя.

        """
        return self.last_name + ' ' + self.first_name + ' ' + self.patronymic


    class Meta: 
        ordering = ["user_id"]
        verbose_name = "информацию о тестируемом пользователе"
        verbose_name_plural = "Информация о тестируемых пользователях"

    # Methods
    def __str__(self):
        """Перегрузка функции __str__.

        """
        return str(self.user_id)


# =================  Тест Кеттелла 16 PF  =================

class KettellQuestion(models.Model):
    """Класс вопроса теста Кеттелла.

    """
    # Поля
    # Номер вопроса
    number = models.IntegerField(
        db_column='number',
        verbose_name='Номер вопроса:',
        help_text='Номер вопроса.'
    )

    # Текст вопроса
    question = models.TextField(
        db_column='text',
        verbose_name='Текст вопроса:',
        help_text='Текст вопроса.'
    )

    # Ответ № 1
    answer_a = models.TextField(
        db_column='answer1',
        verbose_name='Ответ номер - 1:',
        help_text='Ответ номер - 1.'
    )

    # Ответ № 2
    answer_b = models.TextField(
        db_column='answer2',
        verbose_name='Ответ номер - 2:',
        help_text='Ответ номер - 2.'
    )

    # Ответ № 3
    answer_c = models.TextField(
        db_column='answer3',
        verbose_name='Ответ номер - 3:',
        help_text='Ответ номер - 3.'
    )

    # Поля значений правильных ответов по факторам
    #   В факторе "B" совпадение с ключом равно 1-му баллу.
    #   В остальных факторах совпадение с «b» равно 1 баллу,
    #   а совпадение с буквами «а» и «c» по ключу равно 2 баллам.

    # Фактор A
    factor_A = models.CharField(
        db_column='factor_A',
        verbose_name='Значения правильных ответов по фактору - A:',
        help_text='Значения правильных ответов по фактору - A.',
        max_length=2,
        default=0
    )

    # Фактор B
    factor_B = models.CharField(
        db_column='factor_B',
        verbose_name='Значение правильного ответа по фактору - B:',
        help_text='Значение правильного ответа по фактору - B.',
        max_length=1,
        default=0
    )

    # Фактор C
    factor_C = models.CharField(
        db_column='factor_C',
        verbose_name='Значения правильных ответов по фактору - C:',
        help_text='Значения правильных ответов по фактору - C.',
        max_length=2,
        default=0
    )

    # Фактор E
    factor_E = models.CharField(
        db_column='factor_E',
        verbose_name='Значения правильных ответов по фактору - E:',
        help_text='Значения правильных ответов по фактору - E.',
        max_length=2,
        default=0
    )

    # Фактор F
    factor_F = models.CharField(
        db_column='factor_F',
        verbose_name='Значения правильных ответов по фактору - F:',
        help_text='Значения правильных ответов по фактору - F.',
        max_length=2,
        default=0
    )

    # Фактор G
    factor_G = models.CharField(
        db_column='factor_G',
        verbose_name='Значения правильных ответов по фактору - G:',
        help_text='Значения правильных ответов по фактору - G.',
        max_length=2,
        default=0
    )

    # Фактор H
    factor_H = models.CharField(
        db_column='factor_H',
        verbose_name='Значения правильных ответов по фактору - H:',
        help_text='Значения правильных ответов по фактору - H.',
        max_length=2,
        default=0
    )

    # Фактор I
    factor_I = models.CharField(
        db_column='factor_I',
        verbose_name='Значения правильных ответов по фактору - I:',
        help_text='Значения правильных ответов по фактору - I.',
        max_length=2,
        default=0
    )

    # Фактор L
    factor_L = models.CharField(
        db_column='factor_L',
        verbose_name='Значения правильных ответов по фактору - L:',
        help_text='Значения правильных ответов по фактору - L.',
        max_length=2,
        default=0
    )

    # Фактор M
    factor_M = models.CharField(
        db_column='factor_M',
        verbose_name='Значения правильных ответов по фактору - M:',
        help_text='Значения правильных ответов по фактору - M.',
        max_length=2,
        default=0
    )

    # Фактор N
    factor_N = models.CharField(
        db_column='factor_N',
        verbose_name='Значения правильных ответов по фактору - N:',
        help_text='Значения правильных ответов по фактору - N.',
        max_length=2,
        default=0
    )

    # Фактор O
    factor_O = models.CharField(
        db_column='factor_O',
        verbose_name='Значения правильных ответов по фактору - O:',
        help_text='Значения правильных ответов по фактору - O.',
        max_length=2,
        default=0
    )

    # Фактор Q1
    factor_Q1 = models.CharField(
        db_column='factor_Q1',
        verbose_name='Значения правильных ответов по фактору - Q1:',
        help_text='Значения правильных ответов по фактору - Q1.',
        max_length=2,
        default=0
    )

    # Фактор Q2
    factor_Q2 = models.CharField(
        db_column='factor_Q2',
        verbose_name='Значения правильных ответов по фактору - Q2:',
        help_text='Значения правильных ответов по фактору - Q2.',
        max_length=2,
        default=0
    )

    # Фактор Q3
    factor_Q3 = models.CharField(
        db_column='factor_Q3',
        verbose_name='Значения правильных ответов по фактору - Q3:',
        help_text='Значения правильных ответов по фактору - Q3.',
        max_length=2,
        default=0
    )

    # Фактор Q4
    factor_Q4 = models.CharField(
        db_column='factor_Q4',
        verbose_name='Значения правильных ответов по фактору - Q4:',
        help_text='Значения правильных ответов по фактору - Q4.',
        max_length=2,
        default=0
    )

    # Metadata
    class Meta: 
        ordering = ["number"]
        verbose_name = "вопрос теста Кеттелла"
        verbose_name_plural = "Вопросы теста Кеттелла"

    # Methods
    def __str__(self):
        """Перегрузка функции __str__.

        """
        return str(self.number) + ". " + self.question


class KettellAnswer(models.Model):
    """Класс ответа на тест Кеттелла.

    """
    # Поля
    # Поле связи с таблицей информаци о пользователях (InformationTestUser)
    user_id = models.ForeignKey(
        InformationTestUser,
        on_delete=models.CASCADE,
        db_column='user_id',
        verbose_name='Идентификатор пользователя:',
        help_text='Идентификатор пользователя.'
    )

    # Время начала тестирования
    start_testing_dtime = models.DateTimeField(
        db_column='start_testing_dtime',
        verbose_name='Дата и время начала тестирования:',
        help_text='Дата и время начала тестирования.',
        auto_now_add=False,
        default=timezone.now
    )

    # Время окончания тестирования
    end_testing_dtime = models.DateTimeField(
        db_column='end_testing_dtime',
        verbose_name='Дата и время окончания тестирования:',
        help_text='Дата и время окончания тестирования.',
        auto_now_add=False,
        default=timezone.now
    )

    # Данные пользователем ответы в формате - JSON
    answers = models.JSONField(
        db_column='answers',
        verbose_name='Ответы:',
        help_text='Данные пользователем ответы (в формате JSON).',
        default=dict
    )

    # Результаты обработки ответов в формате - JSON
    results = models.JSONField(
        db_column='results',
        verbose_name='Результаты обработки ответов:',
        help_text='Результаты обработки ответов.',
        default=dict
    )

    # Отчет ответа в формате docx
    report = models.FileField(
        db_column='report',
        verbose_name='DOCX результат обработки ответов:',
        help_text='DOCX результат обработки ответов.',
        blank=True,
        upload_to='docx/'
    )


    # Metadata
    class Meta: 
        ordering = ["-id"]
        verbose_name = "ответ теста Кеттелла"
        verbose_name_plural = "Ответы теста Кеттелла"

    # Methods
    def __str__(self):
        """Перегрузка функции __str__.

        """
        return str(self.id) + " | " + str(self.user_id) + " | " + str(self.end_testing_dtime)

# =========================================================


# ===================  Тест СМИЛ (MMPI)  ==================

class MMPIQuestion(models.Model):
    """Класс вопроса теста СМИЛ.

    """
    # Поля
    # Номер вопроса
    number = models.IntegerField(
        db_column='number',
        verbose_name='Номер вопроса:',
        help_text='Номер вопроса.'
    )

    # Текст вопроса
    question = models.TextField(
        db_column='text',
        verbose_name='Текст вопроса:',
        help_text='Текст вопроса.'
    )

    # Признак половой принадлежности вопроса:
    #   1 - мужской;
    #   2 - женский.
    gender = models.IntegerField(
        db_column='gender',
        choices=GENDER,
        verbose_name='Признак половой принадлежности вопроса:',
        help_text='Признак половой принадлежности вопроса.'
    )

    # Шкалы со значениями правильных ответов:
    #   1 - правильный ответ - верно;
    #   2 - правильный ответ - неверно.
    
    # Шкала L (ложь)
    scale_L = models.IntegerField(
        db_column='scale_l',
        verbose_name='Значение правильного ответа по шкале - L:',
        help_text='Значение правильного ответа по шкале - L.',
        default=0        
    )

    # Шкала F (достоверность)
    scale_F = models.IntegerField(
        db_column='scale_f',
        verbose_name='Значение правильного ответа по шкале - F:',
        help_text='Значение правильного ответа по шкале - F.',
        default=0        
    )

    # Шкала K (коррекция)
    scale_K = models.IntegerField(
        db_column='scale_k',
        verbose_name='Значение правильного ответа по шкале - K:',
        help_text='Значение правильного ответа по шкале - K.',
        default=0        
    )

    # Шкала 1 (сверхконтроль)
    scale_1 = models.IntegerField(
        db_column='scale_1',
        verbose_name='Значение правильного ответа по шкале - 1:',
        help_text='Значение правильного ответа по шкале - 1.',
        default=0        
    )

    # Шкала 2 (пессимистичность)
    scale_2 = models.IntegerField(
        db_column='scale_2',
        verbose_name='Значение правильного ответа по шкале - 2:',
        help_text='Значение правильного ответа по шкале - 2.',
        default=0        
    )

    # Шкала 3 (эмоциональная лабильность)
    scale_3 = models.IntegerField(
        db_column='scale_3',
        verbose_name='Значение правильного ответа по шкале - 3:',
        help_text='Значение правильного ответа по шкале - 3.',
        default=0        
    )

    # Шкала 4 (импульсивность)
    scale_4 = models.IntegerField(
        db_column='scale_4',
        verbose_name='Значение правильного ответа по шкале - 4:',
        help_text='Значение правильного ответа по шкале - 4.',
        default=0        
    )

    # Шкала 5 (женственность)
    scale_5 = models.IntegerField(
        db_column='scale_5',
        verbose_name='Значение правильного ответа по шкале - 5:',
        help_text='Значение правильного ответа по шкале - 5.',
        default=0        
    )

    # Шкала 6 (ригидность)
    scale_6 = models.IntegerField(
        db_column='scale_6',
        verbose_name='Значение правильного ответа по шкале - 6:',
        help_text='Значение правильного ответа по шкале - 6.',
        default=0        
    )

    # Шкала 7 (тревожность)
    scale_7 = models.IntegerField(
        db_column='scale_7',
        verbose_name='Значение правильного ответа по шкале - 7:',
        help_text='Значение правильного ответа по шкале - 7.',
        default=0        
    )

    # Шкала 8 (индивидуалистичность)
    scale_8 = models.IntegerField(
        db_column='scale_8',
        verbose_name='Значение правильного ответа по шкале - 8:',
        help_text='Значение правильного ответа по шкале - 8.',
        default=0
    )

    # Шкала 9 (оптимистичность)
    scale_9 = models.IntegerField(
        db_column='scale_9',
        verbose_name='Значение правильного ответа по шкале - 9:',
        help_text='Значение правильного ответа по шкале - 9.',
        default=0
    )

    # Шкала 10 (интроверсия)
    scale_10 = models.IntegerField(
        db_column='scale_10',
        verbose_name='Значение правильного ответа по шкале - 10:',
        help_text='Значение правильного ответа по шкале - 10.',
        default=0
    )

    # Неучитываемые ответы
    noise = models.IntegerField(
        db_column='noise',
        verbose_name='Отметка о неучете ответа на данный вопрос:',
        help_text='Отметка о неучете ответа на данный вопрос.',
        default=0
    )


    # Metadata
    class Meta: 
        ordering = ["number"]
        verbose_name = "вопрос теста СМИЛ"
        verbose_name_plural = "Вопросы теста СМИЛ"

    # Methods
    def __str__(self):
        """Перегрузка функции __str__.

        """
        return str(self.number) + ". " + self.question


class MMPIAnswer(models.Model):
    """Класс ответа теста СМИЛ.

    """
    # Поля
    # Поле связи с таблицей информаци о пользователях (InformationTestUser)
    user_id = models.ForeignKey(
        InformationTestUser,
        on_delete=models.CASCADE,
        db_column='user_id',
        verbose_name='Идентификатор пользователя:',
        help_text='Идентификатор пользователя.'
    )

    # Время начала тестирования
    start_testing_dtime = models.DateTimeField(
        db_column='start_testing_dtime',
        verbose_name='Дата и время начала тестирования:',
        help_text='Дата и время начала тестирования.',
        auto_now_add=False,
        default=timezone.now
    )

    # Время окончания тестирования
    end_testing_dtime = models.DateTimeField(
        db_column='end_testing_dtime',
        verbose_name='Дата и время окончания тестирования:',
        help_text='Дата и время окончания тестирования.',
        auto_now_add=False,
        default=timezone.now
    )

    # Данные пользователем ответы в формате - JSON
    answers = models.JSONField(
        db_column='answers',
        verbose_name='Ответы:',
        help_text='Данные пользователем ответы (в формате JSON).',
        default=dict
    )

    # Результаты обработки ответов в формате - JSON
    #   sum_L  - сырая сумма баллов по шкале L;
    #   sum_F  - сырая сумма баллов по шкале F;
    #   sum_K  - сырая сумма баллов по шкале K;
    #   sum_1  - сырая сумма баллов по шкале 1;
    #   sum_2  - сырая сумма баллов по шкале 2;
    #   sum_3  - сырая сумма баллов по шкале 3;
    #   sum_4  - сырая сумма баллов по шкале 4;
    #   sum_5  - сырая сумма баллов по шкале 5;
    #   sum_6  - сырая сумма баллов по шкале 6;
    #   sum_7  - сырая сумма баллов по шкале 7;
    #   sum_8  - сырая сумма баллов по шкале 8;
    #   sum_9  - сырая сумма баллов по шкале 9;
    #   sum_10 - сырая сумма баллов по шкале 10.
    results = models.JSONField(
        db_column='results',
        verbose_name='Результаты обработки ответов:',
        help_text='Результаты обработки ответов.',
        default=dict
    )

    # Отчет ответа в формате docx
    report = models.FileField(
        db_column='report',
        verbose_name='DOCX результат обработки ответов:',
        help_text='DOCX результат обработки ответов.',
        blank=True,
        upload_to='docx/'
    )


    # Metadata
    class Meta: 
        ordering = ["-id"]
        verbose_name = "ответ теста СМИЛ"
        verbose_name_plural = "Ответы теста СМИЛ"

    # Methods
    def __str__(self):
        """Перегрузка функции __str__.

        """
        return str(self.id) + " | " + str(self.user_id) + " | " + str(self.end_testing_dtime)

# =========================================================


# =========  Тест УСК (Subjective Control Level)  =========

class SCLQuestion(models.Model):
    """Класс вопроса теста УСК.

    """
    # Поля
    # Номер вопроса
    number = models.IntegerField(
        db_column='number',
        verbose_name='Номер вопроса:',
        help_text='Номер вопроса.'
    )

    # Текст вопроса
    question = models.TextField(
        db_column='text',
        verbose_name='Текст вопроса:',
        help_text='Текст вопроса.'
    )

    # Поля значений анализируемых вопросов по шкалам (Io, Id, In, Is, Ip, Im, Iz)
    # Значения:
    #   0 - ответ на данный вопрос не анализируется;
    #   1 - ответ на данный вопрос анализируется со своим знаком "+";
    #   2 - ответ на данный вопрос анализируется с обратным знаком "-".

    # Шкала Io (общая интернальность)
    scale_Io = models.IntegerField(
        db_column='scale_Io',
        verbose_name='Флаг анализа вопроса по шкале - Io:',
        help_text='Флаг анализа вопроса по шкале - Io.',
        default=0
    )

    # Шкала Id (интернальность в области достижений)
    scale_Id = models.IntegerField(
        db_column='scale_Id',
        verbose_name='Флаг анализа вопроса по шкале - Id:',
        help_text='Флаг анализа вопроса по шкале - Id.',
        default=0
    )

    # Шкала In (интернальность в области неудач)
    scale_In = models.IntegerField(
        db_column='scale_In',
        verbose_name='Флаг анализа вопроса по шкале - In:',
        help_text='Флаг анализа вопроса по шкале - In.',
        default=0
    )

    # Шкала Is (интернальность в семейных отношениях)
    scale_Is = models.IntegerField(
        db_column='scale_Is',
        verbose_name='Флаг анализа вопроса по шкале - Is:',
        help_text='Флаг анализа вопроса по шкале - Is.',
        default=0
    )

    # Шкала Ip (интернальность в области производственных отношений)
    scale_Ip = models.IntegerField(
        db_column='scale_Ip',
        verbose_name='Флаг анализа вопроса по шкале - Ip:',
        help_text='Флаг анализа вопроса по шкале - Ip.',
        default=0
    )

    # Шкала Im (интернальность в области межличностных отношений)
    scale_Im = models.IntegerField(
        db_column='scale_Im',
        verbose_name='Флаг анализа вопроса по шкале - Im:',
        help_text='Флаг анализа вопроса по шкале - Im.',
        default=0
    )

    # Шкала Iz (интернильность в отношении здоровья и болезни)
    scale_Iz = models.IntegerField(
        db_column='scale_Iz',
        verbose_name='Флаг анализа вопроса по шкале - Iz:',
        help_text='Флаг анализа вопроса по шкале - Iz.',
        default=0
    )


    # Metadata
    class Meta: 
        ordering = ["number"]
        verbose_name = "вопрос теста УСК"
        verbose_name_plural = "Вопросы теста УСК"

    # Methods
    def __str__(self):
        """Перегрузка функции __str__.

        """
        return str(self.number) + ". " + self.question


class SCLAnswer(models.Model):
    """Класс ответа теста УСК.

    """
    # Поля
    # Поле связи с таблицей информаци о пользователях (InformationTestUser)
    user_id = models.ForeignKey(
        InformationTestUser,
        on_delete=models.CASCADE,
        db_column='user_id',
        verbose_name='Идентификатор пользователя:',
        help_text='Идентификатор пользователя.'
    )

    # Время начала тестирования
    start_testing_dtime = models.DateTimeField(
        db_column='start_testing_dtime',
        verbose_name='Дата и время начала тестирования:',
        help_text='Дата и время начала тестирования.',
        auto_now_add=False,
        default=timezone.now
    )

    # Время окончания тестирования
    end_testing_dtime = models.DateTimeField(
        db_column='end_testing_dtime',
        verbose_name='Дата и время окончания тестирования:',
        help_text='Дата и время окончания тестирования.',
        auto_now_add=False,
        default=timezone.now
    )

    # Данные пользователем ответы в формате - JSON
    answers = models.JSONField(
        db_column='answers',
        verbose_name='Ответы:',
        help_text='Данные пользователем ответы (в формате JSON).',
        default=dict
    )

    # Результаты обработки ответов в формате - JSON
    results = models.JSONField(
        db_column='results',
        verbose_name='Результаты обработки ответов:',
        help_text='Результаты обработки ответов.',
        default=dict
    )

    # Отчет ответа в формате docx
    report = models.FileField(
        db_column='report',
        verbose_name='DOCX результат обработки ответов:',
        help_text='DOCX результат обработки ответов.',
        blank=True,
        upload_to='docx/'
    )


    # Metadata
    class Meta: 
        ordering = ["-id"]
        verbose_name = "ответ теста УСК"
        verbose_name_plural = "Ответы теста УСК"

    # Methods
    def __str__(self):
        """Перегрузка функции __str__.

        """
        return str(self.id) + " | " + str(self.user_id) + " | " + str(self.end_testing_dtime)

# =========================================================


# =========  Прогрессивные матрицы Равена (ПМР)  ==========

class RPMQuestion(models.Model):
    """Класс вопроса прогрессивных матриц Равена.

    """
    # Поля
    # Номер вопроса
    number = models.IntegerField(
        db_column='number',
        verbose_name='Номер вопроса:',
        help_text='Номер вопроса.'
    )

    # Группа вопроса и его номер в группе
    group = models.CharField(
        db_column='group',
        max_length=5,
        blank=True,
        verbose_name='Группа вопроса и его номер в группе:',
        help_text='Группа вопроса и его номер в группе.'
    )

    # Изображение вопроса
    question_img = models.ImageField(
        db_column='question_img',
        verbose_name='Изображение вопроса:',
        help_text='Изображение вопроса.'
    )

    # Изображение ответа-1
    answer_img_1 = models.ImageField(
        db_column='answer_img_1',
        verbose_name='Изображение ответа-1:',
        help_text='Изображение ответа-1.'
    )

    # Изображение ответа-2
    answer_img_2 = models.ImageField(
        db_column='answer_img_2',
        verbose_name='Изображение ответа-2:',
        help_text='Изображение ответа-2.'
    )

    # Изображение ответа-3
    answer_img_3 = models.ImageField(
        db_column='answer_img_3',
        verbose_name='Изображение ответа-3:',
        help_text='Изображение ответа-3.'
    )

    # Изображение ответа-4
    answer_img_4 = models.ImageField(
        db_column='answer_img_4',
        verbose_name='Изображение ответа-4:',
        help_text='Изображение ответа-4.'
    )

    # Изображение ответа-5
    answer_img_5 = models.ImageField(
        db_column='answer_img_5',
        verbose_name='Изображение ответа-5:',
        help_text='Изображение ответа-5.'
    )

    # Изображение ответа-6
    answer_img_6 = models.ImageField(
        db_column='answer_img_6',
        verbose_name='Изображение ответа-6:',
        help_text='Изображение ответа-6.'
    )

    # Изображение ответа-7
    answer_img_7 = models.ImageField(
        db_column='answer_img_7',
        blank=True,
        verbose_name='Изображение ответа-7:',
        help_text='Изображение ответа-7.'
    )

    # Изображение ответа-8
    answer_img_8 = models.ImageField(
        db_column='answer_img_8',
        blank=True,
        verbose_name='Изображение ответа-8:',
        help_text='Изображение ответа-8.'
    )

    # Номер правильного ответа
    correct_answer = models.IntegerField(
        db_column='correct_answer',
        verbose_name='Номер правильного ответа:',
        help_text='Номер правильного ответа.',
        default=1
    )

    # Metadata
    class Meta: 
        ordering = ["number"]
        verbose_name = "вопрос теста прогрессивных матриц Равена"
        verbose_name_plural = "Вопросы теста прогрессивных матриц Равена"

    # Methods
    def __str__(self):
        """Перегрузка функции __str__.

        """
        return str(self.number) + ". " + self.group


class RPMAnswer(models.Model):
    """Класс ответа прогрессивных матриц Равена.

    """
    # Поля
    # Поле связи с таблицей информаци о пользователях (InformationTestUser)
    user_id = models.ForeignKey(
        InformationTestUser,
        on_delete=models.CASCADE,
        db_column='user_id',
        verbose_name='Идентификатор пользователя:',
        help_text='Идентификатор пользователя.'
    )

    # Время начала тестирования
    start_testing_dtime = models.DateTimeField(
        db_column='start_testing_dtime',
        verbose_name='Дата и время начала тестирования:',
        help_text='Дата и время начала тестирования.',
        auto_now_add=False,
        default=timezone.now
    )

    # Время окончания тестирования
    end_testing_dtime = models.DateTimeField(
        db_column='end_testing_dtime',
        verbose_name='Дата и время окончания тестирования:',
        help_text='Дата и время окончания тестирования.',
        auto_now_add=False,
        default=timezone.now
    )

    # Данные пользователем ответы в формате - JSON
    answers = models.JSONField(
        db_column='answers',
        verbose_name='Ответы:',
        help_text='Данные пользователем ответы (в формате JSON).',
        default=dict
    )

    # Результаты обработки ответов в формате - JSON
    #   total_answers          - общее количество данных ответов;
    #   total_correct_answers  - количество данных правильных ответов.
    results = models.JSONField(
        db_column='results',
        verbose_name='Результаты обработки ответов:',
        help_text='Результаты обработки ответов.',
        default=dict
    )

    # Отчет ответа в формате docx
    report = models.FileField(
        db_column='report',
        verbose_name='DOCX результат обработки ответов:',
        help_text='DOCX результат обработки ответов.',
        blank=True,
        upload_to='docx/'
    )


    # Metadata
    class Meta: 
        ordering = ["-id"]
        verbose_name = "ответ теста прогрессивных матриц Равена"
        verbose_name_plural = "Ответы теста прогрессивных матриц Равена"

    # Methods
    def __str__(self):
        """Перегрузка функции __str__.

        """
        return str(self.id) + " | " + str(self.user_id) + " | " + str(self.end_testing_dtime)

# =========================================================


# ==================  Сложные аналогии  ===================

class ComAnalogQuestion(models.Model):
    """Класс вопроса сложных аналогий.

    """
    # Поля
    # Номер вопроса
    number = models.IntegerField(
        db_column='number',
        verbose_name='Номер вопроса:',
        help_text='Номер вопроса.'
    )

   # Текст вопроса
    question = models.TextField(
        db_column='text',
        verbose_name='Текст вопроса:',
        help_text='Текст вопроса.'
    )
    
    # Буква правильного ответа
    correct_answer = models.CharField(
        db_column='correct_answer',
        max_length=5,
        verbose_name='Буква правильного ответа:',
        help_text='Буква правильного ответа.',
        default="A"
    )

    # Metadata
    class Meta: 
        ordering = ["number"]
        verbose_name = "вопрос теста сложных аналогий"
        verbose_name_plural = "Вопросы теста сложных аналогий"

    # Methods
    def __str__(self):
        """Перегрузка функции __str__.

        """
        return str(self.number) + ". " + self.question


class ComAnalogAnswer(models.Model):
    """Класс ответа сложных аналогий.

    """
    # Поля
    # Поле связи с таблицей информаци о пользователях (InformationTestUser)
    user_id = models.ForeignKey(
        InformationTestUser,
        on_delete=models.CASCADE,
        db_column='user_id',
        verbose_name='Идентификатор пользователя:',
        help_text='Идентификатор пользователя.'
    )

    # Время начала тестирования
    start_testing_dtime = models.DateTimeField(
        db_column='start_testing_dtime',
        verbose_name='Дата и время начала тестирования:',
        help_text='Дата и время начала тестирования.',
        auto_now_add=False,
        default=timezone.now
    )

    # Время окончания тестирования
    end_testing_dtime = models.DateTimeField(
        db_column='end_testing_dtime',
        verbose_name='Дата и время окончания тестирования:',
        help_text='Дата и время окончания тестирования.',
        auto_now_add=False,
        default=timezone.now
    )

    # Данные пользователем ответы в формате - JSON
    answers = models.JSONField(
        db_column='answers',
        verbose_name='Ответы:',
        help_text='Данные пользователем ответы (в формате JSON).',
        default=dict
    )

    # Результаты обработки ответов в формате - JSON
    #   total_answers          - общее количество данных ответов;
    #   total_correct_answers  - количество данных правильных ответов.
    results = models.JSONField(
        db_column='results',
        verbose_name='Результаты обработки ответов:',
        help_text='Результаты обработки ответов.',
        default=dict
    )

    # Отчет ответа в формате docx
    report = models.FileField(
        db_column='report',
        verbose_name='DOCX результат обработки ответов:',
        help_text='DOCX результат обработки ответов.',
        blank=True,
        upload_to='docx/'
    )

    # Metadata
    class Meta: 
        ordering = ["-id"]
        verbose_name = "ответ теста сложных аналогий"
        verbose_name_plural = "Ответы теста сложных аналогий"

    # Methods
    def __str__(self):
        """Перегрузка функции __str__.

        """
        return str(self.id) + " | " + str(self.user_id) + " | " + str(self.end_testing_dtime)

# =========================================================











# ===  Тест для подразделений транспортной безопасности ===

class TSafetyQuestion(models.Model):
    """Класс вопроса теста для подразделений транспортной безопасности.

    """
    # Поля
    # Номер вопроса
    number = models.IntegerField(
        db_column='number',
        verbose_name='Номер вопроса:',
        help_text='Номер вопроса.'
    )

    # Текст вопроса
    question = models.TextField(
        db_column='text',
        verbose_name='Текст вопроса:',
        help_text='Текст вопроса.'
    )

    # Ответ № 1
    answer_1 = models.TextField(
        db_column='answer1',
        verbose_name='Ответ номер - 1:',
        help_text='Ответ номер - 1.'
    )

    # Ответ № 2
    answer_2 = models.TextField(
        db_column='answer2',
        verbose_name='Ответ номер - 2:',
        help_text='Ответ номер - 2.'
    )

    # Ответ № 3
    answer_3 = models.TextField(
        db_column='answer3',
        verbose_name='Ответ номер - 3:',
        help_text='Ответ номер - 3.'
    )

    # Ответ № 4
    answer_4 = models.TextField(
        db_column='answer4',
        verbose_name='Ответ номер - 4:',
        help_text='Ответ номер - 4.'
    )

    # Номер правильного ответа
    correct_answer = models.IntegerField(
        db_column='correct_answer',
        verbose_name='Номер правильного ответа:',
        help_text='Номер правильного ответа.'
    )


    # Metadata
    class Meta: 
        ordering = ["number"]
        verbose_name = "вопрос теста для подразделений транспортной безопасности"
        verbose_name_plural = "Вопросы теста для подразделений транспортной безопасности"

    # Methods
    def __str__(self):
        """Перегрузка функции __str__.

        """
        return str(self.number) + ". " + self.question


class TSafetyAnswer(models.Model):
    """Класс ответа теста для подразделений транспортной безопасности.

    """
    # Поля
    # Поле связи с таблицей информаци о пользователях (InformationTestUser)
    user_id = models.ForeignKey(
        InformationTestUser,
        on_delete=models.CASCADE,
        db_column='user_id',
        verbose_name='Идентификатор пользователя:',
        help_text='Идентификатор пользователя.'
    )

    # Время начала тестирования
    start_testing_dtime = models.DateTimeField(
        db_column='start_testing_dtime',
        verbose_name='Дата и время начала тестирования:',
        help_text='Дата и время начала тестирования.',
        auto_now_add=False,
        default=timezone.now
    )

    # Время окончания тестирования
    end_testing_dtime = models.DateTimeField(
        db_column='end_testing_dtime',
        verbose_name='Дата и время окончания тестирования:',
        help_text='Дата и время окончания тестирования.',
        auto_now_add=False,
        default=timezone.now
    )

    # Данные пользователем ответы в формате - JSON
    answers = models.JSONField(
        db_column='answers',
        verbose_name='Ответы:',
        help_text='Данные пользователем ответы (в формате JSON).',
        default=dict
    )

    # Результаты обработки ответов в формате - JSON
    #   total_answers          - общее количество данных ответов;
    #   total_correct_answers  - количество данных правильных ответов.
    results = models.JSONField(
        db_column='results',
        verbose_name='Результаты обработки ответов:',
        help_text='Результаты обработки ответов.',
        default=dict
    )

    # Отчет ответа в формате docx
    report = models.FileField(
        db_column='report',
        verbose_name='DOCX результат обработки ответов:',
        help_text='DOCX результат обработки ответов.',
        blank=True,
        upload_to='docx/'
    )


    # Metadata
    class Meta: 
        ordering = ["-id"]
        verbose_name = "ответ теста для подразделений транспортной безопасности"
        verbose_name_plural = "Ответы теста для подразделений транспортной безопасности"

    # Methods
    def __str__(self):
        """Перегрузка функции __str__.

        """
        return str(self.id) + " | " + str(self.user_id) + " | " + str(self.end_testing_dtime)

# =========================================================