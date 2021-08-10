from jinja2 import Environment, FileSystemLoader
from pathlib import Path, WindowsPath, PosixPath
import zipfile
from os import fspath

from .models import KettellQuestion
from .models import MMPIQuestion
from .models import SCLQuestion
from .models import RPMQuestion


def check_answers(answers:dict, true_answers:dict):
    """Функция проверки правильности данных ответов из словаря - answers в
    соответствии со словарем правильных ответов - true_answers.
    
    Аргументы:
    answers        -- словарь с данными (проверяемыми) ответами;
    true_answers   -- словарь с правильными ответами.
    """
    # Счетчик правильных ответов
    true_count = 0
    # Выходной словарь
    out_dict = {}
    for key, value in true_answers.items():
        if answers[key] in str(value):
            out_dict.update({
                key: {
                    'answer': answers[key],
                    'is_true': True
                }
            })
            # Увеличиваем счетчик правильных ответов
            true_count += 1
        else:
            out_dict.update({
                key: {
                    'answer': answers[key],
                    'is_true': False
                }
            })

    return out_dict, true_count


def check_kettell_answers(answers:dict, true_answers:dict):
    """Функция проверки правильности данных ответов по тесту Кеттелла
    из словаря - answers в соответствии со словарем правильных
    ответов - true_answers.
    
    Аргументы:
    answers        -- словарь с данными (проверяемыми) ответами;
    true_answers   -- словарь с правильными ответами.
    """
    # Счетчик правильных ответов
    true_count = 0
    # Выходной словарь
    out_dict = {}
    for key, value in true_answers.items():
        if answers[key] in value:
            # Расчитываем значение балла ответа (rating) по следующему принципу:
            # если длинна строки значения правильных ответов равна 2 (это не фактор
            # фактор - "B") и само значение правильного ответа не равно значению - 'b'
            # (то есть это значение 'a' или 'c'), то rating равен 2-м баллам,
            # в остальных случаях 1-му баллу.
            rating = 2 if (len(value) == 2) and (answers[key] != 'b') else 1
            out_dict.update({
                key: {
                    'answer': answers[key],
                    'rating': rating
                }
            })
            # Увеличиваем счетчик правильных ответов на величину - rating
            true_count += rating
        else:
            out_dict.update({
                key: {
                    'answer': answers[key],
                    'rating': 0
                }
            })

    return out_dict, true_count


def get_kettell_sten(rating:int, factor_name:str):
    """Функция возвращающая значение стена по соответствующему фактору
    в зависимости от значения суммы сырых баллов по данному фактору.
    
    Аргументы:
    rating       -- сумма сырых баллов по фактору;
    factor_name  -- имя фактора (A, B, C, E, F, G, H, I, L, M, N, O, Q1, Q2, Q3, Q4).
    """   
    factors_stens = {
        'A': {
            1 : {'from': 3, 'to': 4},
            2 : {'from': 5, 'to': 6},
            3 : {'from': 7, 'to': 7},
            4 : {'from': 8, 'to': 8},
            5 : {'from': 9, 'to': 9},
            6 : {'from': 10, 'to': 11},
            7 : {'from': 12, 'to': 12},
            8 : {'from': 13, 'to': 13},
            9 : {'from': 14, 'to': 15},
            10 : {'from': 16, 'to': 19}
        },
        'B': {
            1 : {'from': 0, 'to': 1},
            2 : {'from': 2, 'to': 3},
            3 : {'from': 4, 'to': 4},
            4 : {'from': 5, 'to': 5},
            5 : {'from': 6, 'to': 6},
            6 : {'from': 7, 'to': 7},
            7 : {'from': 8, 'to': 8},
            8 : {'from': 9, 'to': 9},
            9 : {'from': 10, 'to': 10},
            10 : {'from': 11, 'to': 17}
        },
        'C': {
            1 : {'from': 1, 'to': 6},
            2 : {'from': 7, 'to': 8},
            3 : {'from': 9, 'to': 10},
            4 : {'from': 11, 'to': 12},
            5 : {'from': 13, 'to': 13},
            6 : {'from': 14, 'to': 15},
            7 : {'from': 16, 'to': 17},
            8 : {'from': 18, 'to': 20},
            9 : {'from': 21, 'to': 21},
            10 : {'from': 22, 'to': 26}
        },
        'E': {
            1 : {'from': 2, 'to': 4},
            2 : {'from': 5, 'to': 6},
            3 : {'from': 7, 'to': 7},
            4 : {'from': 8, 'to': 9},
            5 : {'from': 10, 'to': 10},
            6 : {'from': 11, 'to': 12},
            7 : {'from': 13, 'to': 13},
            8 : {'from': 14, 'to': 15},
            9 : {'from': 16, 'to': 17},
            10 : {'from': 18, 'to': 22}
        },
        'F': {
            1 : {'from': 4, 'to': 5},
            2 : {'from': 6, 'to': 7},
            3 : {'from': 8, 'to': 9},
            4 : {'from': 10, 'to': 10},
            5 : {'from': 11, 'to': 12},
            6 : {'from': 13, 'to': 14},
            7 : {'from': 15, 'to': 16},
            8 : {'from': 17, 'to': 18},
            9 : {'from': 19, 'to': 20},
            10 : {'from': 21, 'to': 26}
        },
        'G': {
            1 : {'from': 2, 'to': 4},
            2 : {'from': 5, 'to': 7},
            3 : {'from': 8, 'to': 9},
            4 : {'from': 10, 'to': 11},
            5 : {'from': 12, 'to': 13},
            6 : {'from': 14, 'to': 14},
            7 : {'from': 15, 'to': 16},
            8 : {'from': 17, 'to': 18},
            9 : {'from': 19, 'to': 20},
            10 : {'from': 21, 'to': 25}
        },
        'H': {
            1 : {'from': 1, 'to': 3},
            2 : {'from': 4, 'to': 5},
            3 : {'from': 6, 'to': 7},
            4 : {'from': 8, 'to': 9},
            5 : {'from': 10, 'to': 13},
            6 : {'from': 14, 'to': 14},
            7 : {'from': 15, 'to': 16},
            8 : {'from': 17, 'to': 18},
            9 : {'from': 19, 'to': 20},
            10 : {'from': 21, 'to': 25}
        },
        'I': {
            1 : {'from': 0, 'to': 3},
            2 : {'from': 4, 'to': 4},
            3 : {'from': 5, 'to': 5},
            4 : {'from': 6, 'to': 6},
            5 : {'from': 7, 'to': 8},
            6 : {'from': 9, 'to': 9},
            7 : {'from': 10, 'to': 11},
            8 : {'from': 12, 'to': 13},
            9 : {'from': 14, 'to': 14},
            10 : {'from': 15, 'to': 18}
        },
        'L': {
            1 : {'from': 2, 'to': 3},
            2 : {'from': 4, 'to': 5},
            3 : {'from': 6, 'to': 6},
            4 : {'from': 7, 'to': 7},
            5 : {'from': 8, 'to': 9},
            6 : {'from': 10, 'to': 10},
            7 : {'from': 11, 'to': 11},
            8 : {'from': 12, 'to': 13},
            9 : {'from': 14, 'to': 15},
            10 : {'from': 16, 'to': 18}
        },
        'M': {
            1 : {'from': 2, 'to': 3},
            2 : {'from': 4, 'to': 5},
            3 : {'from': 6, 'to': 7},
            4 : {'from': 8, 'to': 8},
            5 : {'from': 9, 'to': 9},
            6 : {'from': 10, 'to': 11},
            7 : {'from': 12, 'to': 12},
            8 : {'from': 13, 'to': 14},
            9 : {'from': 15, 'to': 16},
            10 : {'from': 17, 'to': 20}
        },
        'N': {
            1 : {'from': 2, 'to': 4},
            2 : {'from': 5, 'to': 5},
            3 : {'from': 6, 'to': 7},
            4 : {'from': 8, 'to': 8},
            5 : {'from': 9, 'to': 10},
            6 : {'from': 11, 'to': 11},
            7 : {'from': 12, 'to': 13},
            8 : {'from': 14, 'to': 15},
            9 : {'from': 16, 'to': 16},
            10 : {'from': 17, 'to': 20}
        },
        'O': {
            1 : {'from': 2, 'to': 4},
            2 : {'from': 5, 'to': 6},
            3 : {'from': 7, 'to': 7},
            4 : {'from': 8, 'to': 9},
            5 : {'from': 10, 'to': 11},
            6 : {'from': 12, 'to': 13},
            7 : {'from': 14, 'to': 15},
            8 : {'from': 16, 'to': 16},
            9 : {'from': 17, 'to': 18},
            10 : {'from': 19, 'to': 22}
        },
        'Q1': {
            1 : {'from': 2, 'to': 3},
            2 : {'from': 4, 'to': 4},
            3 : {'from': 5, 'to': 6},
            4 : {'from': 7, 'to': 7},
            5 : {'from': 8, 'to': 8},
            6 : {'from': 9, 'to': 10},
            7 : {'from': 11, 'to': 11},
            8 : {'from': 12, 'to': 13},
            9 : {'from': 14, 'to': 14},
            10 : {'from': 15, 'to': 18}
        },
        'Q2': {
            1 : {'from': 0, 'to': 2},
            2 : {'from': 3, 'to': 3},
            3 : {'from': 4, 'to': 5},
            4 : {'from': 6, 'to': 6},
            5 : {'from': 7, 'to': 7},
            6 : {'from': 8, 'to': 9},
            7 : {'from': 10, 'to': 11},
            8 : {'from': 12, 'to': 12},
            9 : {'from': 13, 'to': 14},
            10 : {'from': 15, 'to': 17}
        },
        'Q3': {
            1 : {'from': 3, 'to': 5},
            2 : {'from': 6, 'to': 7},
            3 : {'from': 8, 'to': 9},
            4 : {'from': 10, 'to': 10},
            5 : {'from': 11, 'to': 12},
            6 : {'from': 13, 'to': 13},
            7 : {'from': 14, 'to': 15},
            8 : {'from': 16, 'to': 16},
            9 : {'from': 17, 'to': 17},
            10 : {'from': 18, 'to': 20}
        },
        'Q4': {
            1 : {'from': 0, 'to': 1},
            2 : {'from': 2, 'to': 3},
            3 : {'from': 4, 'to': 5},
            4 : {'from': 6, 'to': 8},
            5 : {'from': 9, 'to': 10},
            6 : {'from': 11, 'to': 12},
            7 : {'from': 13, 'to': 15},
            8 : {'from': 16, 'to': 17},
            9 : {'from': 18, 'to': 19},
            10 : {'from': 20, 'to': 22}
        }
    }

    stens = factors_stens[factor_name]
    for key, value in stens.items():
        if rating >= value["from"] and rating <= value["to"]:
            return key
    
    return 0


def get_kettell_results(raw_answers:dict):
    """Функция формирующая словарь хронящий в себе результат
    анализа данных ответов по тесту Кеттелла по различным факторам.
    
    Аргументы:
    raw_answers   -- словарь с данными (анализируемыми) ответами.
    """
    # --------------  Обработка по фактору - A  --------------
    # Формируем словарь правельных ответов и другие метрики по фактору A
    true_answers_A = {}
    questions_A = KettellQuestion.objects.filter(
        factor_A__gt=0
    ).order_by("number")

    for question in questions_A:
        true_answers_A.update({'a_' + str(question.number): question.factor_A})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_A = check_kettell_answers(raw_answers, true_answers_A)
    # --------------------------------------------------------
    # --------------  Обработка по фактору - B  --------------
    # Формируем словарь правельных ответов и другие метрики по фактору B
    true_answers_B = {}
    questions_B = KettellQuestion.objects.filter(
        factor_B__gt=0
    ).order_by("number")

    for question in questions_B:
        true_answers_B.update({'a_' + str(question.number): question.factor_B})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_B = check_kettell_answers(raw_answers, true_answers_B)
    # --------------------------------------------------------
    # --------------  Обработка по фактору - C  --------------
    # Формируем словарь правельных ответов и другие метрики по фактору C
    true_answers_C = {}
    questions_C = KettellQuestion.objects.filter(
        factor_C__gt=0
    ).order_by("number")

    for question in questions_C:
        true_answers_C.update({'a_' + str(question.number): question.factor_C})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_C = check_kettell_answers(raw_answers, true_answers_C)
    # --------------------------------------------------------
    # --------------  Обработка по фактору - E  --------------
    # Формируем словарь правельных ответов и другие метрики по фактору E
    true_answers_E = {}
    questions_E = KettellQuestion.objects.filter(
        factor_E__gt=0
    ).order_by("number")

    for question in questions_E:
        true_answers_E.update({'a_' + str(question.number): question.factor_E})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_E = check_kettell_answers(raw_answers, true_answers_E)
    # --------------------------------------------------------
    # --------------  Обработка по фактору - F  --------------
    # Формируем словарь правельных ответов и другие метрики по фактору F
    true_answers_F = {}
    questions_F = KettellQuestion.objects.filter(
        factor_F__gt=0
    ).order_by("number")

    for question in questions_F:
        true_answers_F.update({'a_' + str(question.number): question.factor_F})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_F = check_kettell_answers(raw_answers, true_answers_F)
    # --------------------------------------------------------
    # --------------  Обработка по фактору - G  --------------
    # Формируем словарь правельных ответов и другие метрики по фактору G
    true_answers_G = {}
    questions_G = KettellQuestion.objects.filter(
        factor_G__gt=0
    ).order_by("number")

    for question in questions_G:
        true_answers_G.update({'a_' + str(question.number): question.factor_G})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_G = check_kettell_answers(raw_answers, true_answers_G)
    # --------------------------------------------------------
    # --------------  Обработка по фактору - H  --------------
    # Формируем словарь правельных ответов и другие метрики по фактору H
    true_answers_H = {}
    questions_H = KettellQuestion.objects.filter(
        factor_H__gt=0
    ).order_by("number")

    for question in questions_H:
        true_answers_H.update({'a_' + str(question.number): question.factor_H})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_H = check_kettell_answers(raw_answers, true_answers_H)
    # --------------------------------------------------------
    # --------------  Обработка по фактору - I  --------------
    # Формируем словарь правельных ответов и другие метрики по фактору I
    true_answers_I = {}
    questions_I = KettellQuestion.objects.filter(
        factor_I__gt=0
    ).order_by("number")

    for question in questions_I:
        true_answers_I.update({'a_' + str(question.number): question.factor_I})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_I = check_kettell_answers(raw_answers, true_answers_I)
    # --------------------------------------------------------
    # --------------  Обработка по фактору - L  --------------
    # Формируем словарь правельных ответов и другие метрики по фактору L
    true_answers_L = {}
    questions_L = KettellQuestion.objects.filter(
        factor_L__gt=0
    ).order_by("number")

    for question in questions_L:
        true_answers_L.update({'a_' + str(question.number): question.factor_L})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_L = check_kettell_answers(raw_answers, true_answers_L)
    # --------------------------------------------------------
    # --------------  Обработка по фактору - M  --------------
    # Формируем словарь правельных ответов и другие метрики по фактору M
    true_answers_M = {}
    questions_M = KettellQuestion.objects.filter(
        factor_M__gt=0
    ).order_by("number")

    for question in questions_M:
        true_answers_M.update({'a_' + str(question.number): question.factor_M})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_M = check_kettell_answers(raw_answers, true_answers_M)
    # --------------------------------------------------------
    # --------------  Обработка по фактору - N  --------------
    # Формируем словарь правельных ответов и другие метрики по фактору N
    true_answers_N = {}
    questions_N = KettellQuestion.objects.filter(
        factor_N__gt=0
    ).order_by("number")

    for question in questions_N:
        true_answers_N.update({'a_' + str(question.number): question.factor_N})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_N = check_kettell_answers(raw_answers, true_answers_N)
    # --------------------------------------------------------
    # --------------  Обработка по фактору - O  --------------
    # Формируем словарь правельных ответов и другие метрики по фактору O
    true_answers_O = {}
    questions_O = KettellQuestion.objects.filter(
        factor_O__gt=0
    ).order_by("number")

    for question in questions_O:
        true_answers_O.update({'a_' + str(question.number): question.factor_O})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_O = check_kettell_answers(raw_answers, true_answers_O)
    # --------------------------------------------------------
    # --------------  Обработка по фактору - Q1  --------------
    # Формируем словарь правельных ответов и другие метрики по фактору Q1
    true_answers_Q1 = {}
    questions_Q1 = KettellQuestion.objects.filter(
        factor_Q1__gt=0
    ).order_by("number")

    for question in questions_Q1:
        true_answers_Q1.update({'a_' + str(question.number): question.factor_Q1})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_Q1 = check_kettell_answers(raw_answers, true_answers_Q1)
    # --------------------------------------------------------
    # --------------  Обработка по фактору - Q2  --------------
    # Формируем словарь правельных ответов и другие метрики по фактору Q2
    true_answers_Q2 = {}
    questions_Q2 = KettellQuestion.objects.filter(
        factor_Q2__gt=0
    ).order_by("number")

    for question in questions_Q2:
        true_answers_Q2.update({'a_' + str(question.number): question.factor_Q2})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_Q2 = check_kettell_answers(raw_answers, true_answers_Q2)
    # --------------------------------------------------------
    # --------------  Обработка по фактору - Q3  --------------
    # Формируем словарь правельных ответов и другие метрики по фактору Q3
    true_answers_Q3 = {}
    questions_Q3 = KettellQuestion.objects.filter(
        factor_Q3__gt=0
    ).order_by("number")

    for question in questions_Q3:
        true_answers_Q3.update({'a_' + str(question.number): question.factor_Q3})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_Q3 = check_kettell_answers(raw_answers, true_answers_Q3)
    # --------------------------------------------------------
    # --------------  Обработка по фактору - Q4  --------------
    # Формируем словарь правельных ответов и другие метрики по фактору Q4
    true_answers_Q4 = {}
    questions_Q4 = KettellQuestion.objects.filter(
        factor_Q4__gt=0
    ).order_by("number")

    for question in questions_Q4:
        true_answers_Q4.update({'a_' + str(question.number): question.factor_Q4})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_Q4 = check_kettell_answers(raw_answers, true_answers_Q4)
    # --------------------------------------------------------

    # =============== РАСЧЕТ ВТОРИЧНЫХ ФАКТОРОВ ==============
    # ------  Расчет стена по фактору - F1 (тревожность) -----
    # F1 = [38 + (2 х L + 3 х О + 4 х Q4) – (2 х С + 2 х Н + 2 х Q3)] : 10, 
    # Где «38» – нормирующая константа, 
    # L, O, Q4, C, H, Q3 – значения соответствующих факторов в стенах. 
    sten_F1 = (38 + (2*get_kettell_sten(checked_answers_L[1], 'L') + \
        3*get_kettell_sten(checked_answers_O[1], 'O') + \
        4*get_kettell_sten(checked_answers_Q4[1], 'Q4')) - \
        (2*get_kettell_sten(checked_answers_C[1], 'C') + \
        2*get_kettell_sten(checked_answers_H[1], 'H') + \
        2*get_kettell_sten(checked_answers_Q3[1], 'Q3')))/10
    # --------------------------------------------------------
    # -----  Расчет стена по фактору - F2 (экстарверсия) -----
    # F2 = [(2 х А + 3 х Е + 4 х F + 5 х Н) – (2 х Q2 + 11)] : 10, 
    # Где «10» – нормирующая константа, 
    # A, E, F, H, Q2 – значения соответствующих факторов в стенах. 
    sten_F2 = ((2*get_kettell_sten(checked_answers_A[1], 'A') + \
        3*get_kettell_sten(checked_answers_E[1], 'E') + \
        4*get_kettell_sten(checked_answers_F[1], 'F') + \
        5*get_kettell_sten(checked_answers_H[1], 'H')) - \
        (2*get_kettell_sten(checked_answers_Q2[1], 'Q2') + 11))/10    
    # --------------------------------------------------------
    # --- Расчет стена по фактору - F3 (эмоциональная лабильность) ---
    # F3 = [77 + 2 х С + 2 х Е + 2 х F + 2 х N – 4 х А – 6 х I – 2 х М] : 10, 
    # Где «77» – нормирующая константа, 
    # C, E, F, N, A, I, M – значения соответствующих факторов в стенах. 
    sten_F3 = ((77 + 2*get_kettell_sten(checked_answers_C[1], 'C') + \
        2*get_kettell_sten(checked_answers_E[1], 'E') + \
        2*get_kettell_sten(checked_answers_F[1], 'F') + \
        2*get_kettell_sten(checked_answers_N[1], 'N')) - \
        (4*get_kettell_sten(checked_answers_A[1], 'A') + \
        6*get_kettell_sten(checked_answers_I[1], 'I') + \
        2*get_kettell_sten(checked_answers_M[1], 'M')))/10    
    # --------------------------------------------------------
    # ----- Расчет стена по фактору - F4 (доминантность) -----
    # F4 = [(4 х Е + 3 х М + 4 х Q1 + 4 х Q2) – (3 х А + 2 х G)] : 10, 
    # Где E, M, Q1, Q2, A, G – значения соответствующих факторов в стенах.
    sten_F4 = ((4*get_kettell_sten(checked_answers_E[1], 'E') + \
        3*get_kettell_sten(checked_answers_M[1], 'M') + \
        4*get_kettell_sten(checked_answers_Q1[1], 'Q1') + \
        4*get_kettell_sten(checked_answers_Q2[1], 'Q2')) - \
        (3*get_kettell_sten(checked_answers_A[1], 'A') + \
        2*get_kettell_sten(checked_answers_G[1], 'G')))/10    
    # --------------------------------------------------------

    # Формируем словарь результатов
    results = {
        'factor_A': {
            'answers': checked_answers_A[0],
            'sum': checked_answers_A[1],
            'sten': get_kettell_sten(checked_answers_A[1], 'A')
        },
        'factor_B': {
            'answers': checked_answers_B[0],
            'sum': checked_answers_B[1],
            'sten': get_kettell_sten(checked_answers_B[1], 'B')
        },
        'factor_C': {
            'answers': checked_answers_C[0],
            'sum': checked_answers_C[1],
            'sten': get_kettell_sten(checked_answers_C[1], 'C')
        },
        'factor_E': {
            'answers': checked_answers_E[0],
            'sum': checked_answers_E[1],
            'sten': get_kettell_sten(checked_answers_E[1], 'E')
        },
        'factor_F': {
            'answers': checked_answers_F[0],
            'sum': checked_answers_F[1],
            'sten': get_kettell_sten(checked_answers_F[1], 'F')
        },
        'factor_G': {
            'answers': checked_answers_G[0],
            'sum': checked_answers_G[1],
            'sten': get_kettell_sten(checked_answers_G[1], 'G')
        },
        'factor_H': {
            'answers': checked_answers_H[0],
            'sum': checked_answers_H[1],
            'sten': get_kettell_sten(checked_answers_H[1], 'H')
        },
        'factor_I': {
            'answers': checked_answers_I[0],
            'sum': checked_answers_I[1],
            'sten': get_kettell_sten(checked_answers_I[1], 'I')
        },
        'factor_L': {
            'answers': checked_answers_L[0],
            'sum': checked_answers_L[1],
            'sten': get_kettell_sten(checked_answers_L[1], 'L')
        },
        'factor_M': {
            'answers': checked_answers_M[0],
            'sum': checked_answers_M[1],
            'sten': get_kettell_sten(checked_answers_M[1], 'M')
        },
        'factor_N': {
            'answers': checked_answers_N[0],
            'sum': checked_answers_N[1],
            'sten': get_kettell_sten(checked_answers_N[1], 'N')
        },
        'factor_O': {
            'answers': checked_answers_O[0],
            'sum': checked_answers_O[1],
            'sten': get_kettell_sten(checked_answers_O[1], 'O')
        },
        'factor_Q1': {
            'answers': checked_answers_Q1[0],
            'sum': checked_answers_Q1[1],
            'sten': get_kettell_sten(checked_answers_Q1[1], 'Q1')
        },
        'factor_Q2': {
            'answers': checked_answers_Q2[0],
            'sum': checked_answers_Q2[1],
            'sten': get_kettell_sten(checked_answers_Q2[1], 'Q2')
        },
        'factor_Q3': {
            'answers': checked_answers_Q3[0],
            'sum': checked_answers_Q3[1],
            'sten': get_kettell_sten(checked_answers_Q3[1], 'Q3')
        },
        'factor_Q4': {
            'answers': checked_answers_Q4[0],
            'sum': checked_answers_Q4[1],
            'sten': get_kettell_sten(checked_answers_Q4[1], 'Q4')
        },
        'factor_F1': {
            'sten': sten_F1
        },
        'factor_F2': {
            'sten': sten_F2
        },
        'factor_F3': {
            'sten': sten_F3
        },
        'factor_F4': {
            'sten': sten_F4
        }
    }

    return results


def get_mmpi_sten(rating:float, factor_name:str, gender:int):
    """Функция возвращающая значение стена по соответствующему фактору
    в зависимости от значения суммы баллов по данной шкале.
    
    Аргументы:
    rating      -- сумма баллов по шкале;
    factor_name  -- имя фактора (L, F, K, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
    gender      -- пол опрашиваемого.
    """   
    average_rate_data = {
        'man': {
            'L' : {'M': 4.20, 'sig': 2.90},
            'F' : {'M': 2.76, 'sig': 4.67},
            'K' : {'M': 12.1, 'sig': 5.40},
            '1' : {'M': 11.1, 'sig': 3.90},
            '2' : {'M': 16.6, 'sig': 4.11},
            '3' : {'M': 16.46, 'sig': 5.4},
            '4' : {'M': 18.68, 'sig': 4.11},
            '5' : {'M': 20.46, 'sig': 5.0},
            '6' : {'M': 7.90, 'sig': 3.40},
            '7' : {'M': 23.06, 'sig': 5.0},
            '8' : {'M': 21.96, 'sig': 5.0},
            '9' : {'M': 17.00, 'sig': 4.06},
            '10' : {'M': 25.0, 'sig': 10.0},

        },
        'woman': {
            'L' : {'M': 4.20, 'sig': 2.90},
            'F' : {'M': 2.76, 'sig': 4.67},
            'K' : {'M': 12.1, 'sig': 5.40},
            '1' : {'M': 12.9, 'sig': 4.83},
            '2' : {'M': 18.9, 'sig': 5.00},
            '3' : {'M': 18.66, 'sig': 5.38},
            '4' : {'M': 18.68, 'sig': 4.11},
            '5' : {'M': 36.7, 'sig': 4.67},
            '6' : {'M': 7.90, 'sig': 3.40},
            '7' : {'M': 25.07, 'sig': 6.1},
            '8' : {'M': 22.73, 'sig': 6.36},
            '9' : {'M': 17.00, 'sig': 4.06},
            '10' : {'M': 25.0, 'sig': 10.0},
        }
    }

    # Определяем соответствующие показатели M и sig
    gender = 'man' if gender==1 else 'woman'
    M = average_rate_data[gender][factor_name]['M']
    sig = average_rate_data[gender][factor_name]['sig']

    sten = 50 + 10*(rating - M)/sig

    return int(sten)


def get_mmpi_results(raw_answers:dict, gender):
    """Функция формирующая словарь хронящий в себе результат
    анализа данных ответов по тесту СМИЛ (MMPI) по различным шкалам.
    
    Аргументы:
    raw_answers   -- словарь с данными (анализируемыми) ответами;
    gender        -- пол пользователя в отношении которого проводится анализ.
    """
    # Запрашиваем все объекты вопросов из БД с фильтрацией по полу
    questions = MMPIQuestion.objects.filter(
        gender__exact=gender
    ).order_by("number")

    # --------------  Обработка по шкале - L  --------------
    # Формируем словарь правельных ответов и другие метрики по шкале L
    true_answers_L = {}
    questions_L = questions.filter(
        scale_L__gt=0
    ).order_by("number")

    for question in questions_L:
        true_answers_L.update({'a_' + str(question.number): question.scale_L})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_L = check_answers(raw_answers, true_answers_L)
    # ------------------------------------------------------
    # --------------  Обработка по шкале - F  --------------
    true_answers_F = {}
    questions_F = questions.filter(
        scale_F__gt=0
    ).order_by("number")

    for question in questions_F:
        true_answers_F.update({'a_' + str(question.number): question.scale_F})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_F = check_answers(raw_answers, true_answers_F)
    # ------------------------------------------------------
    # --------------  Обработка по шкале - K  --------------
    true_answers_K = {}
    questions_K = questions.filter(
        scale_K__gt=0
    ).order_by("number")

    for question in questions_K:
        true_answers_K.update({'a_' + str(question.number): question.scale_K})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_K = check_answers(raw_answers, true_answers_K)
    # ------------------------------------------------------
    # --------------  Обработка по шкале - 1  --------------
    true_answers_1 = {}
    questions_1 = questions.filter(
        scale_1__gt=0
    ).order_by("number")

    for question in questions_1:
        true_answers_1.update({'a_' + str(question.number): question.scale_1})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_1 = check_answers(raw_answers, true_answers_1)
    # ------------------------------------------------------
    # --------------  Обработка по шкале - 2  --------------
    true_answers_2 = {}
    questions_2 = questions.filter(
        scale_2__gt=0
    ).order_by("number")

    for question in questions_2:
        true_answers_2.update({'a_' + str(question.number): question.scale_2})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_2 = check_answers(raw_answers, true_answers_2)
    # ------------------------------------------------------
    # --------------  Обработка по шкале - 3  --------------
    true_answers_3 = {}
    questions_3 = questions.filter(
        scale_3__gt=0
    ).order_by("number")

    for question in questions_3:
        true_answers_3.update({'a_' + str(question.number): question.scale_3})
    # Проверяем данные пользователем ответы на правильность
    checked_answers_3 = check_answers(raw_answers, true_answers_3)
    # ------------------------------------------------------
    # --------------  Обработка по шкале - 4  --------------
    true_answers_4 = {}
    questions_4 = questions.filter(
        scale_4__gt=0
    ).order_by("number")

    for question in questions_4:
        true_answers_4.update({'a_' + str(question.number): question.scale_4})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_4 = check_answers(raw_answers, true_answers_4)
    # ------------------------------------------------------
    # --------------  Обработка по шкале - 5  --------------
    true_answers_5 = {}
    questions_5 = questions.filter(
        scale_5__gt=0
    ).order_by("number")

    for question in questions_5:
        true_answers_5.update({'a_' + str(question.number): question.scale_5})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_5 = check_answers(raw_answers, true_answers_5)
    # ------------------------------------------------------
    # --------------  Обработка по шкале - 6  --------------
    true_answers_6 = {}
    questions_6 = questions.filter(
        scale_6__gt=0
    ).order_by("number")

    for question in questions_6:
        true_answers_6.update({'a_' + str(question.number): question.scale_6})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_6 = check_answers(raw_answers, true_answers_6)
    # ------------------------------------------------------
    # --------------  Обработка по шкале - 7  --------------
    true_answers_7 = {}
    questions_7 = questions.filter(
        scale_7__gt=0
    ).order_by("number")

    for question in questions_7:
        true_answers_7.update({'a_' + str(question.number): question.scale_7})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_7 = check_answers(raw_answers, true_answers_7)
    # ------------------------------------------------------
    # --------------  Обработка по шкале - 8  --------------
    true_answers_8 = {}
    questions_8 = questions.filter(
        scale_8__gt=0
    ).order_by("number")

    for question in questions_8:
        true_answers_8.update({'a_' + str(question.number): question.scale_8})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_8 = check_answers(raw_answers, true_answers_8)
    # ------------------------------------------------------
    # --------------  Обработка по шкале - 9  --------------
    true_answers_9 = {}
    questions_9 = questions.filter(
        scale_9__gt=0
    ).order_by("number")

    for question in questions_9:
        true_answers_9.update({'a_' + str(question.number): question.scale_9})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_9 = check_answers(raw_answers, true_answers_9)
    # ------------------------------------------------------
    # --------------  Обработка по шкале - 10  -------------
    true_answers_10 = {}
    questions_10 = questions.filter(
        scale_10__gt=0
    ).order_by("number")

    for question in questions_10:
        true_answers_10.update({'a_' + str(question.number): question.scale_10})

    # Проверяем данные пользователем ответы на правильность
    checked_answers_10 = check_answers(raw_answers, true_answers_10)
    # ------------------------------------------------------

    # --- Расчитываем откорректированные показатели шкал ---
    scale_1_cor = 0.5*checked_answers_K[1] + checked_answers_1[1]

    scale_4_cor = 0.4*checked_answers_K[1] + checked_answers_4[1]

    scale_7_cor = checked_answers_K[1] + checked_answers_7[1]

    scale_8_cor = checked_answers_K[1] + checked_answers_8[1]

    scale_9_cor = 0.2*checked_answers_K[1] + checked_answers_9[1]

    # ------------------------------------------------------

    # Формируем словарь результатов
    results = {
        'scale_L': {
            'answers': checked_answers_L[0],
            'sum': checked_answers_L[1],
            'sten': get_mmpi_sten(checked_answers_L[1], 'L', gender)
        },
        'scale_F': {
            'answers': checked_answers_F[0],
            'sum': checked_answers_F[1],
            'sten': get_mmpi_sten(checked_answers_F[1], 'F', gender)
        },
        'scale_K': {
            'answers': checked_answers_K[0],
            'sum': checked_answers_K[1],
            'sten': get_mmpi_sten(checked_answers_K[1], 'K', gender)
        },
        'scale_1': {
            'answers': checked_answers_1[0],
            'sum': checked_answers_1[1],
            'cor_sum': scale_1_cor,
            'sten': get_mmpi_sten(scale_1_cor, '1', gender)
        },
        'scale_2': {
            'answers': checked_answers_2[0],
            'sum': checked_answers_2[1],
            'sten': get_mmpi_sten(checked_answers_2[1], '2', gender)
        },
        'scale_3': {
            'answers': checked_answers_3[0],
            'sum': checked_answers_3[1],
            'sten': get_mmpi_sten(checked_answers_3[1], '3', gender)
        },
        'scale_4': {
            'answers': checked_answers_4[0],
            'sum': checked_answers_4[1],
            'cor_sum': scale_4_cor,
            'sten': get_mmpi_sten(scale_4_cor, '4', gender)
        },
        'scale_5': {
            'answers': checked_answers_5[0],
            'sum': checked_answers_5[1],
            'sten': get_mmpi_sten(checked_answers_5[1], '5', gender)
        },
        'scale_6': {
            'answers': checked_answers_6[0],
            'sum': checked_answers_6[1],
            'sten': get_mmpi_sten(checked_answers_6[1], '6', gender)
        },
        'scale_7': {
            'answers': checked_answers_7[0],
            'sum': checked_answers_7[1],
            'cor_sum': scale_7_cor,
            'sten': get_mmpi_sten(scale_7_cor, '7', gender)
        },
        'scale_8': {
            'answers': checked_answers_8[0],
            'sum': checked_answers_8[1],
            'cor_sum': scale_8_cor,
            'sten': get_mmpi_sten(scale_8_cor, '8', gender)
        },
        'scale_9': {
            'answers': checked_answers_9[0],
            'sum': checked_answers_9[1],
            'cor_sum': scale_9_cor,
            'sten': get_mmpi_sten(scale_9_cor, '9', gender)
        },
        'scale_10': {
            'answers': checked_answers_10[0],
            'sum': checked_answers_10[1],
            'sten': get_mmpi_sten(checked_answers_10[1], '10', gender)
        }
    }

    return results


def get_scl_sten(rating:int, scale_name:str):
    """Функция возвращающая значение стена по соответствующему фактору
    в зависимости от значения суммы сырых баллов по данной шкале.
    
    Аргументы:
    rating       -- сумма сырых баллов по шкале;
    scale_name   -- имя шкалы (Io, Id, In, Is, Ip, Im, Iz).
    """   
    scale_stens = {
        'Io': {
            1 : {'from': -132, 'to': -14},
            2 : {'from': -13, 'to': -3},
            3 : {'from': -2, 'to': 9},
            4 : {'from': 10, 'to': 21},
            5 : {'from': 22, 'to': 32},
            6 : {'from': 33, 'to': 44},
            7 : {'from': 45, 'to': 56},
            8 : {'from': 57, 'to': 68},
            9 : {'from': 69, 'to': 79},
            10 : {'from': 80, 'to': 132}
        },
        'Id': {
            1 : {'from': -36, 'to': -11},
            2 : {'from': -10, 'to': -7},
            3 : {'from': -6, 'to': -3},
            4 : {'from': -2, 'to': 1},
            5 : {'from': 2, 'to': 5},
            6 : {'from': 6, 'to': 9},
            7 : {'from': 10, 'to': 14},
            8 : {'from': 15, 'to': 18},
            9 : {'from': 19, 'to': 22},
            10 : {'from': 23, 'to': 36}
        },
        'In': {
            1 : {'from': -36, 'to': -8},
            2 : {'from': -7, 'to': -4},
            3 : {'from': -3, 'to': 0},
            4 : {'from': 1, 'to': 4},
            5 : {'from': 5, 'to': 7},
            6 : {'from': 8, 'to': 11},
            7 : {'from': 12, 'to': 15},
            8 : {'from': 16, 'to': 19},
            9 : {'from': 20, 'to': 23},
            10 : {'from': 24, 'to': 36}
        },
        'Is': {
            1 : {'from': -30, 'to': -5},
            2 : {'from': -4, 'to': -1},
            3 : {'from': 0, 'to': 3},
            4 : {'from': 4, 'to': 7},
            5 : {'from': 8, 'to': 11},
            6 : {'from': 12, 'to': 15},
            7 : {'from': 16, 'to': 19},
            8 : {'from': 20, 'to': 23},
            9 : {'from': 24, 'to': 27},
            10 : {'from': 28, 'to': 30}
        },
        'Ip': {
            1 : {'from': -30, 'to': -12},
            2 : {'from': -11, 'to': -8},
            3 : {'from': -7, 'to': -5},
            4 : {'from': -4, 'to': -1},
            5 : {'from': 0, 'to': 3},
            6 : {'from': 4, 'to': 6},
            7 : {'from': 7, 'to': 10},
            8 : {'from': 11, 'to': 13},
            9 : {'from': 14, 'to': 17},
            10 : {'from': 18, 'to': 30}
        },
        'Im': {
            1 : {'from': -12, 'to': -7},
            2 : {'from': -6, 'to': -5},
            3 : {'from': -4, 'to': -3},
            4 : {'from': -2, 'to': -1},
            5 : {'from': 0, 'to': 1},
            6 : {'from': 2, 'to': 4},
            7 : {'from': 5, 'to': 6},
            8 : {'from': 7, 'to': 8},
            9 : {'from': 9, 'to': 10},
            10 : {'from': 11, 'to': 12}
        },
        'Iz': {
            1 : {'from': -12, 'to': -4},
            2 : {'from': -3, 'to': -2},
            3 : {'from': -1, 'to': 0},
            4 : {'from': 1, 'to': 2},
            5 : {'from': 3, 'to': 3},
            6 : {'from': 4, 'to': 4},
            7 : {'from': 5, 'to': 6},
            8 : {'from': 7, 'to': 8},
            9 : {'from': 9, 'to': 10},
            10 : {'from': 11, 'to': 12}
        }
    }

    stens = scale_stens[scale_name]
    for key, value in stens.items():
        if rating >= value["from"] and rating <= value["to"]:
            return key
    
    return 0


def get_scl_raw_sum(answers:dict, analising_answers:dict):
    """Функция получения сырой суммы баллов по тесту УСК
    из словаря - answers в соответствии со словарем анализируемых
    ответов - analising_answers.
    
    Аргументы:
    answers            -- словарь с данными (проверяемыми) ответами;
    analising_answers  -- словарь с правильными ответами.
    """
    # Счетчик для подсчета общей суммы
    out_sum = 0
    
    # Счетчик для подсчета положительной суммы
    positive_sum = 0
    # Счетчик для подсчета отрицательной суммы
    negative_sum = 0

    # Выходной словарь
    out_dict = {
        "positive":{},
        "negative":{}
    }
    # out_dict = {}

    for key, value in analising_answers.items():
        # Находим значение значимости данного ответа (answer_value),
        # если ответ на данный вопрос анализируется со своим знаком "+"
        # (анализируем value), то просто берем значение данного ответа,
        # иначе меняем знак ответа
        if value == 1:

            out_dict['positive'].update({
                key: {
                    'answer': answers[key],
                }
            })
            positive_sum += int(answers[key])
        else:
            out_dict['negative'].update({
                key: {
                    'answer': answers[key],
                }
            })
            negative_sum += int(answers[key])

        # answer_value = int(answers[key]) if value == 1 else -1*int(answers[key])

        # out_dict.update({
        #     key: {
        #         'answer': answers[key],
        #     }
        # })
        # Увеличиваем счетчик подсчета суммы - out_sum
    
    sum = positive_sum - negative_sum

    # out_dict['positive'].update({
    #     'sum': positive_sum
    # })

    # out_dict['negative'].update({
    #     'sum': negative_sum
    # })

    return out_dict, sum, positive_sum, negative_sum


def get_scl_results(raw_answers:dict):
    """Функция формирующая словарь хронящий в себе результат
    анализа данных ответов по тесту УСК.
    
    Аргументы:
    raw_answers   -- словарь с данными (анализируемыми) ответами.
    """
    # Запрашиваем все объекты вопросов из БД
    questions = SCLQuestion.objects.all()

    # --------------  Обработка по шкале - Io  ---------------
    # Формируем словарь с анализируемыми ответами по шкале Io
    analising_answers_Io = {}
    questions_Io = questions.filter(
        scale_Io__gt=0
    ).order_by("number")

    for question in questions_Io:
        analising_answers_Io.update({'a_' + str(question.number): question.scale_Io})

    # Проверяем данные пользователем ответы на правильность
    raw_sum_Io = get_scl_raw_sum(raw_answers, analising_answers_Io)
    # --------------------------------------------------------
    # --------------  Обработка по шкале - Id  ---------------
    # Формируем словарь с анализируемыми ответами по шкале Id
    analising_answers_Id = {}
    questions_Id = questions.filter(
        scale_Id__gt=0
    ).order_by("number")

    for question in questions_Id:
        analising_answers_Id.update({'a_' + str(question.number): question.scale_Id})

    # Проверяем данные пользователем ответы на правильность
    raw_sum_Id = get_scl_raw_sum(raw_answers, analising_answers_Id)
    # --------------------------------------------------------
    # --------------  Обработка по шкале - In  ---------------
    # Формируем словарь с анализируемыми ответами по шкале In
    analising_answers_In = {}
    questions_In = questions.filter(
        scale_In__gt=0
    ).order_by("number")

    for question in questions_In:
        analising_answers_In.update({'a_' + str(question.number): question.scale_In})

    # Проверяем данные пользователем ответы на правильность
    raw_sum_In = get_scl_raw_sum(raw_answers, analising_answers_In)
    # --------------------------------------------------------
    # --------------  Обработка по шкале - Is  ---------------
    # Формируем словарь с анализируемыми ответами по шкале Is
    analising_answers_Is = {}
    questions_Is = questions.filter(
        scale_Is__gt=0
    ).order_by("number")

    for question in questions_Is:
        analising_answers_Is.update({'a_' + str(question.number): question.scale_Is})

    # Проверяем данные пользователем ответы на правильность
    raw_sum_Is = get_scl_raw_sum(raw_answers, analising_answers_Is)
    # --------------------------------------------------------
    # --------------  Обработка по шкале - Ip  ---------------
    # Формируем словарь с анализируемыми ответами по шкале Ip
    analising_answers_Ip = {}
    questions_Ip = questions.filter(
        scale_Ip__gt=0
    ).order_by("number")

    for question in questions_Ip:
        analising_answers_Ip.update({'a_' + str(question.number): question.scale_Ip})

    # Проверяем данные пользователем ответы на правильность
    raw_sum_Ip = get_scl_raw_sum(raw_answers, analising_answers_Ip)
    # --------------------------------------------------------
    # --------------  Обработка по шкале - Im  ---------------
    # Формируем словарь с анализируемыми ответами по шкале Im
    analising_answers_Im = {}
    questions_Im = questions.filter(
        scale_Im__gt=0
    ).order_by("number")

    for question in questions_Im:
        analising_answers_Im.update({'a_' + str(question.number): question.scale_Im})

    # Проверяем данные пользователем ответы на правильность
    raw_sum_Im = get_scl_raw_sum(raw_answers, analising_answers_Im)
    # --------------------------------------------------------
    # --------------  Обработка по шкале - Iz  ---------------
    # Формируем словарь с анализируемыми ответами по шкале Iz
    analising_answers_Iz = {}
    questions_Iz = questions.filter(
        scale_Iz__gt=0
    ).order_by("number")

    for question in questions_Iz:
        analising_answers_Iz.update({'a_' + str(question.number): question.scale_Iz})

    # Проверяем данные пользователем ответы на правильность
    raw_sum_Iz = get_scl_raw_sum(raw_answers, analising_answers_Iz)
    # --------------------------------------------------------

    # Формируем словарь результатов
    results = {
        'scale_Io': {
            'answers': raw_sum_Io[0],
            'sum': raw_sum_Io[1],
            'positive_sum': raw_sum_Io[2],
            'negative_sum': raw_sum_Io[3],
            'sten': get_scl_sten(raw_sum_Io[1], 'Io')
        },
        'scale_Id': {
            'answers': raw_sum_Id[0],
            'sum': raw_sum_Id[1],
            'positive_sum': raw_sum_Id[2],
            'negative_sum': raw_sum_Id[3],
            'sten': get_scl_sten(raw_sum_Id[1], 'Id')
        },
        'scale_In': {
            'answers': raw_sum_In[0],
            'sum': raw_sum_In[1],
            'positive_sum': raw_sum_In[2],
            'negative_sum': raw_sum_In[3],
            'sten': get_scl_sten(raw_sum_In[1], 'In')
        },
        'scale_Is': {
            'answers': raw_sum_Is[0],
            'sum': raw_sum_Is[1],
            'positive_sum': raw_sum_Is[2],
            'negative_sum': raw_sum_Is[3],
            'sten': get_scl_sten(raw_sum_Is[1], 'Is')
        },
        'scale_Ip': {
            'answers': raw_sum_Ip[0],
            'sum': raw_sum_Ip[1],
            'positive_sum': raw_sum_Ip[2],
            'negative_sum': raw_sum_Ip[3],
            'sten': get_scl_sten(raw_sum_Ip[1], 'Ip')
        },
        'scale_Im': {
            'answers': raw_sum_Im[0],
            'sum': raw_sum_Im[1],
            'positive_sum': raw_sum_Im[2],
            'negative_sum': raw_sum_Im[3],
            'sten': get_scl_sten(raw_sum_Im[1], 'Im')
        },
        'scale_Iz': {
            'answers': raw_sum_Iz[0],
            'sum': raw_sum_Iz[1],
            'positive_sum': raw_sum_Iz[2],
            'negative_sum': raw_sum_Iz[3],
            'sten': get_scl_sten(raw_sum_Iz[1], 'Iz')
        }
    }

    return results


def get_rpm_iq(sum:int):
    """Функция расчета IQ по тесту Прогрессивных матриц Равена.
    
    Аргументы:
    sum  -- сумма правильных ответов.
    """
    intervals = {
        15:	62,
        16:	65,
        17:	65,
        18:	66,
        19:	67,
        20:	69,
        21:	70,
        22:	71,
        23:	72,
        24:	73,
        25:	75,
        26:	76,
        27:	77,
        28:	79,
        29:	80,
        30:	82,
        31:	83,
        32:	84,
        33:	86,
        34:	87,
        35:	88,
        36:	90,
        37:	91,
        38:	92,
        39:	94,
        40:	95,
        41:	96,
        42:	98,
        43:	99,
        44:	100,
        45:	102,
        46:	104,
        47:	106,
        48:	108,
        49:	110,
        50:	112,
        51:	114,
        52:	116,
        53:	118,
        54:	120,
        55:	122,
        56:	124,
        57:	126,
        58:	128,
        59:	130,
        60:	140
    }

    return intervals[sum]


def get_rpm_results(raw_answers:dict):
    """Функция формирующая словарь хронящий в себе результат
    анализа данных ответов по тесту прогрессивных матриц Равена.
    
    Аргументы:
    raw_answers   -- словарь с данными (анализируемыми) ответами.
    """
    # Запрашиваем все объекты вопросов из БД с фильтрацией по полу
    questions = RPMQuestion.objects.all()

    # --------------  Обработка по серии - A  ---------------
    # Формируем словарь с анализируемыми ответами по серии A
    analising_answers_A = {}
    questions_A = questions.filter(
        group='A'
    ).order_by("number")

    for question in questions_A:
        analising_answers_A.update({'a_' + str(question.number): question.correct_answer})

    # Проверяем данные пользователем ответы на правильность
    raw_sum_A = check_answers(raw_answers, analising_answers_A)
    # --------------------------------------------------------
    # --------------  Обработка по серии - B  ---------------
    # Формируем словарь с анализируемыми ответами по серии B
    analising_answers_B = {}
    questions_B = questions.filter(
        group='B'
    ).order_by("number")

    for question in questions_B:
        analising_answers_B.update({'a_' + str(question.number): question.correct_answer})

    # Проверяем данные пользователем ответы на правильность
    raw_sum_B = check_answers(raw_answers, analising_answers_B)
    # --------------------------------------------------------
    # --------------  Обработка по серии - C  ---------------
    # Формируем словарь с анализируемыми ответами по серии C
    analising_answers_C = {}
    questions_C = questions.filter(
        group='C'
    ).order_by("number")

    for question in questions_C:
        analising_answers_C.update({'a_' + str(question.number): question.correct_answer})

    # Проверяем данные пользователем ответы на правильность
    raw_sum_C = check_answers(raw_answers, analising_answers_C)
    # --------------------------------------------------------
    # --------------  Обработка по серии - D  ---------------
    # Формируем словарь с анализируемыми ответами по серии D
    analising_answers_D = {}
    questions_D = questions.filter(
        group='D'
    ).order_by("number")

    for question in questions_D:
        analising_answers_D.update({'a_' + str(question.number): question.correct_answer})

    # Проверяем данные пользователем ответы на правильность
    raw_sum_D = check_answers(raw_answers, analising_answers_D)
    # --------------------------------------------------------
    # --------------  Обработка по серии - E  ---------------
    # Формируем словарь с анализируемыми ответами по серии E
    analising_answers_E = {}
    questions_E = questions.filter(
        group='E'
    ).order_by("number")

    for question in questions_E:
        analising_answers_E.update({'a_' + str(question.number): question.correct_answer})

    # Проверяем данные пользователем ответы на правильность
    raw_sum_E = check_answers(raw_answers, analising_answers_E)
    # --------------------------------------------------------
    sum_cor_answers = raw_sum_A[1] + raw_sum_B[1] + raw_sum_C[1] + raw_sum_D[1] + raw_sum_E[1]

    # Формируем словарь результатов
    results = {
        'group_A': {
            'answers': raw_sum_A[0],
            'sum': raw_sum_A[1]
        },
        'group_B': {
            'answers': raw_sum_B[0],
            'sum': raw_sum_B[1]
        },
        'group_C': {
            'answers': raw_sum_C[0],
            'sum': raw_sum_C[1]
        },
        'group_D': {
            'answers': raw_sum_D[0],
            'sum': raw_sum_D[1]
        },
        'group_E': {
            'answers': raw_sum_E[0],
            'sum': raw_sum_E[1]
        },
        'sum_answers': len(raw_answers),
        'sum_cor_answers': sum_cor_answers,
        'percent_correct_results': int(sum_cor_answers/len(raw_answers)*100),
        'iq': get_rpm_iq(sum_cor_answers)
    }

    return results


def save_to_docx(temlatePath:str, outFileName:str, context):
    """Функция сохранения данных в DOCX файл
            
    Аргументы:
    temlatePath -- путь к папке с шаблоном DOCX
    outfileName -- имя выходного файла
    """
    pathToDocxTemplate = Path(temlatePath)
    pathToOutDocument = Path(outFileName)
    delim = Path('/')

    file_loader = FileSystemLoader(str(pathToDocxTemplate) if pathToDocxTemplate is type(PosixPath) else str(pathToDocxTemplate).replace('\\', '/'))
    env = Environment(loader = file_loader)

    # Заполняем документ шаблона.
    pathToTemlate = Path('word/document.xml')

    # tmpDocument = env.get_template(str(pathToTemlate))
    tmpDocument = env.get_template(str(pathToTemlate) if pathToTemlate is type(PosixPath) else str(pathToTemlate).replace('\\', '/'))

    # Формирование файла по шаблону и сохранение во временный файл
    tmpDocument.stream(context=context).dump(fspath(pathToOutDocument) + '.tmp1')

    # Формируем пакет (архив)
    listFilePathes = pathToDocxTemplate.glob('**/*.*')
    
    with zipfile.ZipFile(fspath(pathToOutDocument), 'w') as zip_file:
        for filePath in listFilePathes:
            if (str(filePath).rfind(str(pathToTemlate))) >= 0:
                # Если переносимый файл расположен в word/document.xml, то 
                # переносим под этим именем первый временный файл.
                zip_file.write(str(pathToOutDocument) + '.tmp1', str(filePath).replace(str(pathToDocxTemplate) + str(delim), ''))
                # Удаляем временный файл
                Path(str(pathToOutDocument) + '.tmp1').unlink()

            else:
                # Во всех остальных случаях просто переносим файлы
                zip_file.write(str(filePath), str(filePath).replace(str(pathToDocxTemplate) + str(delim), ''))


def arr_reshape(array:list, n:int):
    """Функция изменения размерности массива (одномерного массива в двумерный).

    Аргументы:
    array -- одномерный список который будет преобразовываться;
    n     -- колличество элементов в элементе массива.
    """
    return [array[i:i+n] for i in range(0, len(array), n)]