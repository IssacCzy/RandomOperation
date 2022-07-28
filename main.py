#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# @Time : 2020/11/25 16:06
# @Author : Issac
# @FileName: main.py
# @Software: PyCharm
# @E-mail : Issac_czy@163.com
"""
宫门
"""
from random import random
import eel
import json
from pyecharts import options as opts
from pyecharts.charts import Line
from UtilLog import MyLogger as logger
import random
from random import randint
from datetime import date

add_subtract_operators = ['+', '-']
multiply_divide_operators = ['*', '/']
all_operators = ['+', '-', '*', '/']
hot_count = 20
train_count = 20

# 除法表达式资源池
divide_pool = []
# 被除数资源池
divided_pool = []
for m in range(1, 10):
    for n in range(1, 10):
        divide_pool.append([m, n, m * n])
        divided_pool.append(m * n)

# 10 以内连除资源池
divide_chain_in_ten = []
for m in range(1, 11):
    for n in range(1, 11):
        for j in range(1, 11):
            if m * n * j <= 10:
                divide_chain_in_ten.append([m, n, j, m * n * j])


@eel.expose
def hot_date():
    """
    获取热身题目数据
    :return:
    """
    try:
        subject_lists = {
            'multiply_table_subjects': multiply_table_subjects(),  # 热身训练：乘法口诀
            'add_subtract_in_20_subjects': add_subtract_in_20_subjects(),  # 20以内加减
            'ten_hundred_thousand_subjects': ten_hundred_thousand_subjects()  # 热身训练：整十、整百、整千加减训练
        }
    except Exception as e:
        printExceptionInfo(e)
    finally:
        return json.dumps(subject_lists)


@eel.expose
def train_date():
    """
    获取训练题目数据
    :return:
    """
    try:
        subject_lists = {
            'add_subtract_subjects': add_subtract_subjects(),  # 正式训练：加减训练题
            'divide_in_ten_subjects': divide_in_ten_subjects(),  # 10以内的连除
            'divide_with_remainder_subjects': divide_with_remainder_subjects(),  # 100以内的有余数的除法
            'multiply_divide_subjects': multiply_divide_subjects(),  # 100以内乘除混合运算
            'multiply_add_subtract_subjects': multiply_add_subtract_subjects(),  # 乘加、乘减混合（加减乘混合）
            'divide_add_subtract_subjects': divide_add_subtract_subjects(),  # 除加、除减混合（加减除混合）
            'add_subtract_multiply_divide_with_brackets_subjects': add_subtract_multiply_divide_with_brackets_subjects()
            # 含小括号的（加减）(乘除)混合：（20+45）*3
        }
    except Exception as e:
        printExceptionInfo(e)
    finally:
        return json.dumps(subject_lists)


def add_subtract_in_20_subjects():
    """
    20 以内的加减法 4 hot
    :return:
    """
    try:
        subjects = []

        logger.info('20 以内的加减法：')
        while True:
            # 运算符随机数：加、减
            operators_nums = randint(0, 100)

            # 两个随机数字
            nums = []
            for j in range(0, 2):
                nums.append(randint(1, 20))

            if operators_nums % 2 == 0:
                item_result = nums[0] + nums[1]
                logger.info('\t\t{}+{}={}'.format(nums[0], nums[1], item_result))
            elif operators_nums % 2 == 1:
                item_result = nums[0] - nums[1]
                logger.info('\t\t{}-{}={}'.format(nums[0], nums[1], item_result))

            if item_result > 0:  # 目前尚未学到负数
                item = {
                    'num_1': nums[0],
                    'num_2': nums[1],
                    'operator_1': all_operators[operators_nums % 2],
                    'result': item_result
                }
                subjects.append(item)

            if len(subjects) == hot_count:
                break
        return subjects
    except Exception as e:
        printExceptionInfo(e)


def add_subtract_multiply_divide_with_brackets_subjects():
    """
    含小括号的（加减）(乘除)混合：（20+45）*3
    :return:
    """
    try:
        subjects = []

        logger.info('含小括号的（加减）(乘除)混合：')
        while True:
            # 运算符加减随机数：加、减
            operators_nums_1 = randint(1, 100)

            # 运算符乘除随机数：乘、除
            operators_nums_2 = randint(1, 100)

            # 加减随机数字
            nums = []
            for j in range(0, 2):
                nums.append(randint(1, 100))

            # 乘除随机数
            num3 = randint(1, 9)

            with_remainder = 0
            if operators_nums_1 % 2 == 0:  # +
                if operators_nums_2 % 2 == 0:  # *
                    item_result = (nums[0] + nums[1]) * num3

                    subject_str = '({} + {}) × {}'.format(nums[0], nums[1], num3)
                    logger.info('\t\t{} = {}'.format(subject_str, item_result))
                elif operators_nums_2 % 2 == 1:  # /
                    # 随机取一个被除数
                    divided_num_temp = random.choice(divide_pool)
                    # 随机取一个小于被除数的数
                    num1 = randint(0, divided_num_temp[2])
                    num2 = divided_num_temp[2] - num1
                    num3 = divided_num_temp[randint(0, 100) % 2]

                    item_result = (num1 + num2) / num3
                    subject_str = '({} + {}) ÷ {}'.format(num1, num2, num3)
                    logger.info('\t\t{} = {}'.format(subject_str, item_result))
            elif operators_nums_1 % 2 == 1:  # -
                if operators_nums_2 % 2 == 0:  # *
                    item_result = (nums[0] - nums[1]) * num3

                    subject_str = '({} - {}) × {}'.format(nums[0], nums[1], num3)
                    logger.info('\t\t{} = {}'.format(subject_str, item_result))
                elif operators_nums_2 % 2 == 1:  # /
                    # 随机取一个被除数
                    divided_num_temp = random.choice(divide_pool)
                    # 随机取一个小于被除数的数
                    num1 = divided_num_temp[2]
                    num2 = randint(0, divided_num_temp[2])
                    num_big = num1 + num2

                    num3 = divided_num_temp[randint(0, 100) % 2]

                    item_result = (num_big - num2) / num3
                    subject_str = '({} - {}) ÷ {}'.format(num_big, num2, num3)
                    logger.info('\t\t{} = {}'.format(subject_str, item_result))

            if item_result > 0 and with_remainder == 0:  # 结果为负数的剔除
                item = {
                    'subject_str': subject_str,
                    'result': int(item_result)
                }
                subjects.append(item)

            if len(subjects) == train_count:
                break
        return subjects
    except Exception as e:
        printExceptionInfo(e)


def divide_add_subtract_subjects():
    """
    除加、除减混合（加减除混合）
    :return:
    """
    try:
        logger.info('除加、除减混合（加减除混合）：')
        subjects = []

        while True:
            # 运算符加减随机数：加、减
            operators_nums_1 = randint(1, 100)

            # 运算符除和加减的相对位置
            option_num = randint(1, 100)

            # 加减随机数字
            num3 = randint(1, 100)

            # 除法 index
            dividend_num = randint(0, len(divide_pool) - 1)
            # 除数随机数
            divisor_num = randint(0, 100)

            subject_str = ''
            if operators_nums_1 % 2 == 0:  # +
                if option_num % 2 == 0:  # 优先 /
                    num1 = divide_pool[dividend_num][2]
                    num2 = divide_pool[dividend_num][divisor_num % 2]
                    item_result = num1 / num2 + num3

                    subject_str = '{} ÷ {} + {}'.format(num1, num2, num3)
                    logger.info('\t\t{} = {}'.format(subject_str, item_result))
                elif option_num % 2 == 1:  # 优先 +
                    num1 = divide_pool[dividend_num][2]
                    num2 = divide_pool[dividend_num][divisor_num % 2]
                    item_result = num3 + num1 / num2

                    subject_str = '{} + {} ÷ {}'.format(num3, num1, num2)
                    logger.info('\t\t{} = {}'.format(subject_str, item_result))

            elif operators_nums_1 % 2 == 1:  # -
                if option_num % 2 == 0:  # 优先 /
                    num1 = divide_pool[dividend_num][2]
                    num2 = divide_pool[dividend_num][divisor_num % 2]
                    item_result = num1 / num2 - num3

                    subject_str = '{} ÷ {} - {}'.format(num1, num2, num3)
                    logger.info('\t\t{} = {}'.format(subject_str, item_result))
                elif option_num % 2 == 1:  # 优先 -
                    num1 = divide_pool[dividend_num][2]
                    num2 = divide_pool[dividend_num][divisor_num % 2]
                    item_result = num3 - num1 / num2

                    subject_str = '{} - {} ÷ {}'.format(num3, num1, num2)
                    logger.info('\t\t{} = {}'.format(subject_str, item_result))

            if item_result > 0:  # 结果为负数的剔除
                item = {
                    'subject_str': subject_str,
                    'result': int(item_result)
                }
                subjects.append(item)

            if len(subjects) == train_count:
                break
        return subjects
    except Exception as e:
        printExceptionInfo(e)


def multiply_add_subtract_subjects():
    """
    乘加、乘减混合（加减乘混合）
    :return:
    """
    try:
        logger.info('除加、除减混合（加减除混合）：')
        subjects = []

        while True:
            # 运算符加减随机数：加、减
            operators_nums = randint(1, 100)

            # 运算符除和加减的相对位置: 加/减 和 乘 的位置
            option_num = randint(1, 100)

            subject_str = ''
            if option_num % 2 == 0:  # * 在前
                num1 = randint(1, 9)
                num2 = randint(1, 9)
                num3 = randint(0, 100)

                if operators_nums % 2 == 0:  # +
                    item_result = num1 * num2 + num3
                    subject_str = '{} × {} + {} '.format(num1, num2, num3)
                    logger.info('\t\t{} = {}'.format(subject_str, item_result))
                elif operators_nums % 2 == 1:  # -
                    while num1 * num2 < num3:
                        num3 = randint(0, 100)

                    item_result = num1 * num2 - num3
                    subject_str = '{} × {} - {}'.format(num1, num2, num3)
                    logger.info('\t\t{} = {}'.format(subject_str, item_result))

            elif option_num % 2 == 1:  # * 在后
                if operators_nums % 2 == 0:  # +
                    num1 = randint(0, 100)
                    num2 = randint(1, 9)
                    num3 = randint(1, 9)
                    item_result = num1 + num2 * num3

                    subject_str = '{} + {} × {}'.format(num1, num2, num3)
                    logger.info('\t\t{} = {}'.format(subject_str, item_result))
                elif operators_nums % 2 == 1:  # -
                    num1 = randint(0, 100)
                    num2 = randint(1, 9)
                    num3 = randint(1, 9)

                    while num1 < num2 * num3:
                        num1 = randint(0, 100)

                    item_result = num1 - num2 * num3
                    subject_str = '{} - {} × {}'.format(num1, num2, num3)
                    logger.info('\t\t{} = {}'.format(subject_str, item_result))

            if item_result > 0:  # 结果为负数的剔除
                item = {
                    'subject_str': subject_str,
                    'result': int(item_result)
                }
                subjects.append(item)

            if len(subjects) == train_count:
                break
        return subjects
    except Exception as e:
        printExceptionInfo(e)


def multiply_divide_subjects():
    """
    100以内乘除混合运算
    :return:
    """
    try:
        logger.info('100以内乘除混合运算：')
        subjects = []

        while True:
            # 运算符加减随机数：乘、除
            subject_str = ''

            # 随机取一个被除数
            divided_num_temp = random.choice(divide_pool)

            num2 = divided_num_temp[randint(0, 100) % 2]
            num1 = divided_num_temp[2]
            num3 = randint(1, 9)

            item_result = num1 / num2 * num3
            subject_str = '{} ÷ {} × {}'.format(num1, num2, num3)
            logger.info('\t\t{} = {}'.format(subject_str, item_result))

            if item_result > 0:  # 结果为负数的剔除
                item = {
                    'subject_str': subject_str,
                    'result': int(item_result)
                }
                subjects.append(item)

            if len(subjects) == train_count:
                break
        return subjects
    except Exception as e:
        printExceptionInfo(e)


def divide_with_remainder_subjects():
    """
    100以内的有余数的除法
    :return:
    """
    try:
        logger.info('100以内的有余数的除法：')
        subjects = []

        while True:
            operators_nums = random.choice(divide_pool)

            # remainder 余数
            remainder = randint(1, 9)

            # 随机除数 index
            divide_num_index = randint(0, 100)

            num1 = operators_nums[2] + remainder
            num2 = operators_nums[divide_num_index % 2]
            num3 = operators_nums[(divide_num_index + 1) % 2]

            if num3 > num2 or remainder > num3 or remainder % num2 == 0 or num2 == 1:
                continue

            logger.info('{} ÷ {} = {} 余 {}'.format(num1, num2, num3, remainder))

            item = {
                'dividend': num1,
                'divisor': num2,
                'result': num3,
                'remainder': remainder
            }
            subjects.append(item)

            if len(subjects) == train_count:
                break
        return subjects
    except Exception as e:
        printExceptionInfo(e)


def divide_in_ten_subjects():
    """
    10以内的连除
    :return:
    """
    try:
        logger.info('10以内的连除：')
        subjects = []

        while True:
            items_index = randint(0, len(divide_chain_in_ten) - 1)
            order_num = randint(0, 100)
            result_num = randint(0, 100)

            items = divide_chain_in_ten[items_index]
            if len(items) < 4:
                continue

            num1 = items[3]
            result = items[result_num % 3]

            items.remove(num1)
            items.remove(result)
            if order_num % 2 == 0:
                num2 = items[0]
                num3 = items[1]
            else:
                num2 = items[1]
                num3 = items[0]

            subject_str = '{} ÷ {} ÷ {}'.format(num1, num2, num3)
            logger.info('\t\t{} = {}'.format(subject_str, result))

            item = {
                'subject_str': subject_str,
                'result': num3
            }
            subjects.append(item)

            if len(subjects) == train_count:
                break
        return subjects
    except Exception as e:
        printExceptionInfo(e)


@eel.expose
def save_result(data):
    """
    获取做题用时
    :return:
    """
    try:
        type = data['type']  # 1：热身   2：训练
        user_time = data['user_time']  # 用时时长(分钟)
        today = date.today()
        today = today.strftime("%Y-%m-%d")

        logger.info('{}\t\t{}\t\t用时 {} 分钟'.format(today, '热身' if type == 1 else '训练', user_time))

        with open('history/history.txt', 'a', encoding='utf-8') as fp:
            fp.write('{}#{}#{}\n'.format(today, type, user_time))
    except Exception as e:
        printExceptionInfo(e)


@eel.expose
def train_history_date():
    """
    获取训练数据
    :return:
    """
    try:
        c_hot = None
        c_train = None

        with open('history/history.txt') as file_obj:
            lines = file_obj.readlines()

        dates_4_hot = []
        dates_4_hot_dict = {}  # {'日期':次数,....}

        dates_4_train = []
        dates_4_train_dict = {}  # {'日期':次数,....}

        hot = []
        train = []

        if len(lines) > 0:
            for line in lines:
                items = line.split('#')
                cur_day_str = items[0]
                train_type = items[1]

                if int(train_type) == 1:  # 热身
                    try:
                        times = dates_4_hot_dict[cur_day_str]
                        dates_4_hot_dict[cur_day_str] = times + 1
                    except:
                        # 当前日期第一次
                        dates_4_hot_dict[cur_day_str] = 1

                    times = dates_4_hot_dict[cur_day_str]
                    dates_4_hot.append('{}(第{}次)'.format(cur_day_str, times))
                    hot.append(items[2])
                elif int(train_type) == 2:  # 正式训练
                    try:
                        times = dates_4_train_dict[cur_day_str]
                        dates_4_train_dict[cur_day_str] = times + 1
                    except:
                        # 当前日期第一次
                        dates_4_train_dict[cur_day_str] = 1

                    times = dates_4_train_dict[cur_day_str]
                    dates_4_train.append('{}(第{}次)'.format(cur_day_str, times))
                    train.append(items[2])

        c_hot = (
            Line(
                ## 初始化配置
                init_opts=opts.InitOpts(
                    # 设置动画
                    animation_opts=opts.AnimationOpts(animation_delay=1000, animation_easing='elasticOut')
                )
            )
            .add_xaxis(dates_4_hot)
            .add_yaxis(series_name='热身练习',
                       y_axis=hot,
                       is_smooth=True,  # 平滑折线
                       color='white'
                       )
            .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
                             color="#00B9FF",
                             # 块 label 样式设置
                             label_opts=opts.LabelOpts(is_show=True, formatter="{@[1]}分钟", color='white',
                                                       font_size='14')
                             )
            .set_global_opts(title_opts=opts.TitleOpts(title=""),
                             tooltip_opts=opts.TooltipOpts(trigger="axis"),  # 显示鼠标线
                             xaxis_opts=opts.AxisOpts(axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                                                      is_scale=True,
                                                      boundary_gap=True,
                                                      axislabel_opts=opts.LabelOpts(color='white')
                                                      ),
                             yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color='white')),
                             legend_opts=opts.LegendOpts(
                                 textstyle_opts=opts.TextStyleOpts(color='white', font_size=16)),
                             datazoom_opts=[opts.DataZoomOpts()]  # 缩略图
                             )
        )

        c_train = (
            Line(
                ## 初始化配置
                init_opts=opts.InitOpts(
                    # 设置动画
                    animation_opts=opts.AnimationOpts(animation_delay=1000, animation_easing='elasticOut')
                )
            )
            .add_xaxis(dates_4_train)
            .add_yaxis(series_name='模拟练习',
                       y_axis=train,
                       is_smooth=True,  # 平滑折线
                       color='white'
                       )
            .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
                             color="#00B9FF",
                             # 块 label 样式设置
                             label_opts=opts.LabelOpts(is_show=True, formatter="{@[1]}分钟", color='white',
                                                       font_size='14')
                             )
            .set_global_opts(title_opts=opts.TitleOpts(title=""),
                             tooltip_opts=opts.TooltipOpts(trigger="axis"),  # 显示鼠标线
                             xaxis_opts=opts.AxisOpts(axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                                                      is_scale=True,
                                                      boundary_gap=True,
                                                      axislabel_opts=opts.LabelOpts(color='white')
                                                      ),
                             yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color='white')),
                             legend_opts=opts.LegendOpts(
                                 textstyle_opts=opts.TextStyleOpts(color='white', font_size=16)),
                             datazoom_opts=[opts.DataZoomOpts()]  # 缩略图
                             )
        )
    except Exception as e:
        printExceptionInfo(e)
    finally:
        history_4_hot = None
        history_4_train = None

        if c_hot:
            history_4_hot = c_hot.dump_options_with_quotes()

        if c_train:
            history_4_train = c_train.dump_options_with_quotes()

        data = {
            'history_4_hot': history_4_hot,
            'history_4_train': history_4_train
        }
        return json.dumps(data)


def ten_hundred_thousand_subjects():
    """
    整十、整百、整千加减训练 20 题
    :return:
    """
    try:
        subjects = []

        logger.info('整十、整百、整千加减训练 20 题：')
        while True:
            # 运算符随机数：加、减
            operators_nums = randint(0, 100)

            # 两个随机数字
            nums = []
            for j in range(0, 2):
                nums.append(randint(1, 9))
            # 随机扩大 10倍、100倍、1000倍
            num1 = nums[0] * random_num()
            num2 = nums[1] * random_num()

            if operators_nums % 2 == 0:
                item_result = num1 + num2
                logger.info('\t\t{}+{}={}'.format(num1, num2, item_result))
            elif operators_nums % 2 == 1:
                item_result = num1 - num2
                logger.info('\t\t{}-{}={}'.format(num1, num2, item_result))

            if item_result > 0:  # 目前尚未学到负数
                item = {
                    'num_1': num1,
                    'num_2': num2,
                    'operator_1': all_operators[operators_nums % 2],
                    'result': item_result
                }
                subjects.append(item)

            if len(subjects) == hot_count:
                break
        return subjects
    except Exception as e:
        printExceptionInfo(e)


def random_num():
    """
    随机整数：10、100、1000
    :return:
    """
    # 倍数随机数：整十、整百、整千
    times_nums = randint(0, 100)
    if times_nums % 3 == 0:
        times_nums = 10
    elif times_nums % 3 == 1:
        times_nums = 100
    elif times_nums % 3 == 2:
        times_nums = 1000
    return times_nums


def multiply_table_subjects():
    """
    乘法口诀训练 20 题
    :return:
    """
    try:
        subjects = []

        logger.info('乘法口诀训练 20 题：')
        while True:
            # 运算符随机数：乘、除
            operators_nums = randint(0, 100)

            if operators_nums % 2 == 0:
                # 两个随机数字
                nums = []
                for j in range(0, 2):
                    nums.append(randint(2, 9))

                num1 = nums[0]
                num2 = nums[1]
                item_result = num1 * num2
                logger.info('\t\t{} * {}={}'.format(num1, num2, item_result))
            elif operators_nums % 2 == 1:

                divide_pool_items = random.choice(divide_pool)
                num1 = divide_pool_items[2]

                if randint(0, 100) % 2 == 0:
                    num2 = divide_pool_items[0]
                    item_result = divide_pool_items[1]
                else:
                    num2 = divide_pool_items[1]
                    item_result = divide_pool_items[0]

                logger.info('\t\t{} / {}={}'.format(num1, num2, item_result))

            item = {
                'num_1': num1,
                'num_2': num2,
                'operator_1': all_operators[(operators_nums % 2) + 2],
                'result': item_result
            }
            subjects.append(item)

            if len(subjects) == hot_count:
                break
        return subjects
    except Exception as e:
        printExceptionInfo(e)


def add_subtract_subjects():
    """
    加减运算混合运算 50 题
    :return:
    """
    try:
        subjects = []

        logger.info('加减运算混合运算 50 题：')
        while True:
            # 三个随机数字
            nums = []
            for j in range(0, 3):
                nums.append(randint(0, 100))

            # 两个运算符随机数
            operators_nums = []
            for j in range(0, 3):
                operators_nums.append(randint(0, 100))

            operator_1 = 0 if operators_nums[0] % 2 == 0 else 1  # 运算符 = : all_operators[operator_1]
            operator_2 = 0 if operators_nums[1] % 2 == 0 else 1  # 运算符 = : all_operators[operator_2]

            if operator_1 == 0 and operator_2 == 0:
                item_result = nums[0] + nums[1] + nums[2]

                subject_str = '{} + {} + {}'.format(nums[0], nums[1], nums[2])
                logger.info('\t\t{} = {}'.format(subject_str, item_result))
            elif operator_1 == 0 and operator_2 == 1:
                item_result = nums[0] + nums[1] - nums[2]

                subject_str = '{} + {} - {}'.format(nums[0], nums[1], nums[2])
                logger.info('\t\t{} = {}'.format(subject_str, item_result))
            elif operator_1 == 1 and operator_2 == 0:
                while nums[0] < nums[1]:
                    # 三个随机数字
                    nums = []
                    for j in range(0, 3):
                        nums.append(randint(0, 100))

                item_result = nums[0] - nums[1] + nums[2]

                subject_str = '{} - {} + {}'.format(nums[0], nums[1], nums[2])
                logger.info('\t\t{} = {}'.format(subject_str, item_result))
            elif operator_1 == 1 and operator_2 == 1:
                while nums[0] < (nums[1] + nums[2]):
                    # 三个随机数字
                    nums = []
                    for j in range(0, 3):
                        nums.append(randint(0, 100))

                item_result = nums[0] - nums[1] - nums[2]

                subject_str = '{} - {} - {}'.format(nums[0], nums[1], nums[2])
                logger.info('\t\t{} = {}'.format(subject_str, item_result))

            if item_result > 0:  # 目前尚未学到负数
                item = {
                    'subject_str': subject_str,
                    'result': item_result
                }
                subjects.append(item)

            if len(subjects) == train_count:
                break
        return subjects
    except Exception as e:
        printExceptionInfo(e)


def printExceptionInfo(e):
    """
    统一异常信息打印方法：
        异常信息
        发生异常的文件名
        发生异常的行号
    :param e:
    :return:
    """
    logger.error(repr(e))
    # 输出异常信息
    logger.error(e)
    # 输出引发异常的文件
    logger.error('文件：{0}'.format(e.__traceback__.tb_frame.f_globals['__file__']))
    # 输出异常信息的行号
    logger.error('行号：{0}'.format(e.__traceback__.tb_lineno))


if __name__ == '__main__':
    try:
        # 明确 web 资源所在的目录
        eel.init('web')
        # 启动的函数调用放在最后,port=0表示使用随机端口,size=(宽,高)
        # eel.start('hot.html', port=0, size=('1200', '800'))
        eel.start('history.html', port=0, size=('1200', '800'))
        # eel.start('train.html', port=0, size=('1200', '800'))
    except Exception as e:
        printExceptionInfo(e)
