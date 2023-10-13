'''
从id.csv中读取身份证号,读取省份、城市、区县,生日,性别等信息,存入csv中
可支持多线程处理任务

'''

import pandas as pd
from mzfuzz import mzfuzz
import re
import datetime
from datetime import date

import csv  

''' 判断偶数奇数 '''
def is_male(num):  
    if num % 2 == 0:  
        return 0  
    else:  
        return 1
    
''' 校验身份证号是否真实'''
def validate_id_card(id_card):  
# 验证身份证号码的格式  
    if not re.match(r'^\d{17}[\d|X]$', id_card):  
        return False  
        
    # 加权因子  
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  
    # 对应校验码  
    codes = '10X98765432'  
    # 计算校验码  
    sum = 0  
    for i in range(17):  
        sum += int(id_card[i]) * weights[i]  
    check_code = codes[sum % 11]  
    # 判断校验码是否匹配  
    return id_card[-1] == check_code

''' 从身份证号中提取信息'''
def extract_id_card_info(id_card):
    # 匹配身份证号码的正则表达式
    pattern = r'^(\d{6})(\d{4})(\d{2})(\d{2})(\d{3})(\d|X|x)$'
    # 提取身份证信息
    match = re.match(pattern, str(id_card))
    if match:
        # 提取区域代码
        area_code = match.group(1)
        # 提取出生年月日
        year = int(match.group(2))
        month = int(match.group(3))
        day = int(match.group(4))
        birthdate = datetime.date(year, month, day)
        # 提取顺序号
        sequence_number = match.group(5)[2]
        # 性别 
        gender = is_male(int(sequence_number))
        # 返回身份证信息
        return area_code, birthdate, gender
    else:
        # 身份证号码格式错误
        return None

''' 将数据输出成dataframe '''
def execute_task(id):
    try:
        # 存储形式（db 或 excel）
        # method = 'excel'  
        # 校验身份证号准确性
        if validate_id_card(str(id)):
            area_code, birthdate, gender = extract_id_card_info(str(id))
            # 解析前六位区县代码
            area_row = code_df.loc[code_df['third_code'] == str(area_code)].iloc[0]
            province = area_row.at['first_name']
            city = area_row.at['second_name']
            country = area_row.at['third_name']
            birthday = birthdate.strftime("%Y-%m-%d")

            # 输出解析结果
            with open(output_file_name,'a+',encoding='utf-8') as f:   
                row = ["'"+str(id),str(province),str(city),str(country),str(birthday),str(gender)] 
                output_string = ",".join(row)
                f.write(output_string+'\n')
           
        else:
            with open('error.log','a+',encoding='utf-8') as f:   
                f.write(str(id)+","+"身份证号格式错误"+"\n") 
        pass
    except Exception as e:
        print(e)
        with open('error.log','a+',encoding='utf-8') as f:   
            f.write(str(id)+","+"\n") 
        pass
    pass

if __name__ == "__main__":
    # 设置 任务文件路径、输出文件路径
    filename = 'id.csv'
    date_today = date.today().strftime("%Y-%m-%d")
    output_file_name = 'result_output_'+str(date_today)+'.csv'

    id = pd.read_csv(filename)['id']
    # 读取区县代码对照关系
    code_df = pd.read_csv('id_code.csv',encoding='utf-8').astype(str)
    # 定义表头
    with open(output_file_name,'a+',encoding='utf-8') as f:
        f.write('身份证号,省份,城市,区县,出生日期,性别'+'\n')
    # 多线程执行任务
    mzfuzz.multi_thread(execute_task,id,15)




