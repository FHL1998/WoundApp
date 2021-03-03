import time
import datetime

from db.sqlite3_connect import select_data


def get_days_ago(date, n):
    """获取指定时间的前n天的日期"""
    t = time.strptime(date, "%Y-%m-%d")
    y, m, d = t[0:3]
    date = str(datetime.datetime(y, m, d) - datetime.timedelta(n)).split()
    return date[0]


def get_day_list(n):
    """获取今天与前n天的日期列表"""
    before_n_days = []
    for i in range(0, n + 1)[::-1]:
        before_n_days.append(str(datetime.date.today() - datetime.timedelta(days=i)))
    return before_n_days


def num_of_word_to_known():
    """查询今天已学习单词"""
    today = str(datetime.date.today())
    sql = "SELECT COUNT(id) FROM known WHERE create_date='" + today + "'"
    response = int(select_data(sql)[0][0])
    return response


def num_of_word_to_study():
    """计算待学习的单词"""
    known = num_of_word_to_known()
    sql = "SELECT word_num FROM user WHERE id=1"
    response = int(select_data(sql)[0][0])
    word_to_study = response - known
    if word_to_study > 0:
        return word_to_study
    else:
        return 0


def turn_to_unicode(string):
    """编码转换"""
    res = ''
    for v in string:
        res = res + hex(ord(v)).upper().replace('0X', '\\u')
    print(string, '的Unicode编码为：', res)
    return res


def instance_new_line(str_text, len_text, is_cn=False):
    """例句换行"""
    import math
    if not is_cn:
        str_len = len(str_text)
        # 判断是否需要换行
        lines = math.ceil(str_len/len_text)
        for i in range(1, lines):
            blank_index = str_text.find(' ', len_text * i, -1)
            if not blank_index == -1:
                str_text = str_text[:blank_index] + '\n' + str_text[blank_index+1:]
        return str_text
    else:
        str_len = len(str_text)
        len_text = int(len_text/2)
        lines = math.ceil(str_len / len_text)
        for i in range(1, lines):
            str_text = str_text[:len_text] + '\n' + str_text[len_text:]
        return str_text


def sub_str_len(str_text, len_text):
    """控制字符串长度"""
    ret_text = ''
    new_line_list = str_text.split('\n')
    for line in new_line_list:
        text_list = line.split('；')
        if len(text_list) > len_text:
            for i in range(len_text):
                ret_text += text_list[i] + '；'
        else:
            ret_text += line
        ret_text += '\n'
    return ret_text


if __name__ == '__main__':
    turn_to_unicode('上传文件')
