import os
import re
from io import BytesIO
import pandas as pd
import numpy as np
import warnings
from requests import request
"""
用于excel校验
"""


def read_excel_from_oss(method="get", url=""):
    """读取oss的excel内容并写入到本地csv"""
    try:
        result = request(method=method, url=url)
        excel_data = BytesIO(result.content)
        print(f"成功读取oss文件内容: {url}")
        return excel_data
    except Exception as e:
        print(f"读取oss报错 {url} 时出错：{e}")


def read_excel_and_write_to_dict(excel_data=None, file_name=None):
    """excel内容并写入到内存dict中
    :param excel_data：excel的io对象, 参数和file_name互斥
    :file_name: excel文件名称，目前读取check_file目录下文件，参数和excel_data互斥
    """
    try:
        if excel_data is not None and file_name is not None:
            pass
        elif file_name is not None:
            excel_data = os.path.join(os.path.dirname(os.getcwd()) + "/check_file/" + file_name)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning, module=re.escape('openpyxl.styles.stylesheet'))
            df = pd.read_excel(excel_data, engine="openpyxl")
        # 将DataFrame转换为字典，以行为单位存储数据
        row_dict = {}  # 创建一个空字典来存储按行转换的数据
        for index, row in df.iterrows():  # 遍历DataFrame中的每一行
            row_dict[index] = row.to_dict()  # 将每一行转换为字典并存储在row_dict中
        return row_dict
    except Exception as e:
        print(f"excel写入dict时出错：{e}")


def read_excel_and_write_to_list(excel_data=None, file_name=None):
    """excel内容并写入到内存list中
    :param excel_data：excel的io对象, 参数和file_name互斥
    :file_name: excel文件名称，目前读取check_file目录下文件，参数和excel_data互斥
    """
    try:
        if excel_data is not None and file_name is not None:
            pass
        elif file_name is not None:
            excel_data = os.path.join(os.path.dirname(os.getcwd()) + "/check_file/" + file_name)

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning, module=re.escape('openpyxl.styles.stylesheet'))
            df = pd.read_excel(excel_data, engine="openpyxl")
        # 将DataFrame转换为字典，以行为单位存储数据
        rows_list = df.values.tolist()
        return rows_list
    except Exception as e:
        print(f"excel写入list时出错：{e}")


def read_excel_and_write_to_csv(excel_data, file_name):
    """excel内容并写入到csv中"""
    try:
        df = pd.read_excel(excel_data, engine="openpyxl")
        local_csv_path = os.path.join(os.path.dirname(os.getcwd()) + "/temp_file/" + file_name)
        df.to_csv(local_csv_path, index=False)
        return local_csv_path
    except Exception as e:
        print(f"excel写入csv时出错：{e}")


def check_excel(actual, expected):
    """对比两份excel内容
    :param: actual: 实际值，list类型
    :param: expected: 预期值，list类型
    """
    try:
        if actual == expected:
            return True, ["完全匹配"]
        else:
            errors = []
            # 断言1：校验行数
            actual_num = len(actual)
            expected_num = len(expected)
            check_row = actual_num - expected_num
            if check_row == 0:
                errors.append("预期和实际行数相等，为" + str(actual_num) + "行")
            else:
                errors.append(
                    "行数和预期对比差" + check_row.__str__() + "行" + ", 实际:" + str(actual_num) + "预期: " + str(
                        expected_num))
            # 断言不匹配行
            if check_row >= 0:
                num = len(expected)
            else:
                num = len(actual)
            for i in range(num):
                if actual[i] == expected[i]:
                    continue
                else:
                    errors.append(
                        "第" + str(i + 1) + "行不匹配，预期为：" + str(expected[i]) + ", 实际为: " + str(actual[i]))
            return False, errors
    except Exception as e:
        print(f"对比excel：{e}")
        return False, [e]


def del_temp_file(file_name=""):
    """删除temp下临时文件"""
    file_path = os.path.join(os.path.dirname(os.getcwd()) + "/temp_file/" + file_name)
    try:
        os.remove(file_path)
        print(f"文件 {file_path} 已成功删除。")
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在。")
    except Exception as e:
        print(f"删除文件 {file_path} 时出错：{e}")
