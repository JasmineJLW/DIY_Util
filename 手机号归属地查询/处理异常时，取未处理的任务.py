import pandas as pd
 # 打开phoneNum，将15938565886这行之后的数据读取一遍

df = pd.read_csv('phoneNum.txt',encoding='utf-8')
df_new = df.iloc[524288:].astype('str')
df_new['phone'] = df_new['phone'].apply(lambda x: x[:11])
df_new.to_csv('phoneNum2.txt',index=False, sep='\t')
