此脚本用于从身份证号中读取信息，识别内容包含：身份证号是否真实、所属省份、城市、区县、出生日期、性别

1、将身份证号信息列，粘贴到id.csv文件中

    注意：第一行为列标题 id,此title必须有，否则无法识别身份证号列

2、全国区县号对照表.csv 存储的是身份证号与户籍所在地对照关系,执行脚本时，该文件与.py脚本再同一级文件夹下。
    
    本文件会根据实际情况持续更新

3、mzfuzz.multi_thread(execute_task,id,15)，其中的15表示线程数，根据任务数量自定义即可

4、执行.py脚本

5、结果输出在 result_output_xx_xx_xx.csv 中，包含身份证号、省份、城市、区县、出生日期、性别，

   其中，身份证号列值前添加了单引号，防止精度缺失，用户导入其他工具进行分析时请注意处理。

6、校验有误的身份证号在 error.log 文件中
