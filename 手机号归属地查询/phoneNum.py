from phone import Phone
import os
import pandas as pd

def getPhoneNum(file):      #读取源文件，获取待查询的手机号
    try:
        with open(file,"r") as f:
            df = pd.read_csv(file)    
            phonList = df.iloc[:, 0].tolist()  #读取源手机号文档中的手机号
            return phonList   #返回手机号列表。phonList
    
    except:     #兼容读取文档失败
        pass

def getPhoneInfo(phoneNum):     #查询函数
    info = Phone().find(phoneNum[:11])   #通过phone库查询
    try:    #返回所有查询的信息
        phone = info['phone']   #手机号
        province = info['province'] #归属地：省份
        city = info['city'] #归属地，城市
        zip_code = info['zip_code']     #邮政编码
        area_code = info['area_code']   #区域编码
        phone_type = info['phone_type'] #手机号运营商
        print(phone+"\t"+province+city+"\t"+phone_type)
        return ("\n"+phone+" \t"+province+city+" \t"+phone_type)    #因为我只需要手机号、区域、运营商，所以只返回这三个字段，其他字段，可以自己按需添加；
    except:     #兼容查询失败的情况
        print("\n"+str(phoneNum.strip("\n"))+" \t"+"Error!")
        return ("\n"+str(phoneNum.strip("\n"))+" \t"+"Error!")  

if __name__ == "__main__":

    cwd = os.getcwd()

    listPhoneNum = getPhoneNum('phoneNum2.txt')  #通过getPhoneNum函数，读取源文件。
    listResult = []

    for i in listPhoneNum:
        try:
            num = str(i)[:11]
            res = getPhoneInfo(num)
            listResult.append(res)
            with open('result.txt',"a",encoding='utf-8') as f:   #写入结果文档
                f.write(res)
                f.close()
        except:     #兼容出错
            res = "\n"+str(i).strip("\n") + "\t" + "Error!"     
            with open('result.txt',"a",encoding='utf-8') as f: 
                f.write(res)
                f.close()