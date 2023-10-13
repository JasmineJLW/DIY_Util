import json
import pandas as pd

if __name__ == "__main__":

    graph = {
        "nodes": [],  
        "edges": []
    }

    # 从nodes.xlsx中读取node的各行，存入字典

    df1 = pd.read_excel('nodes.xlsx',sheet_name=0)  # 读取第一个sheet
    nodes_dict = df1.to_dict('records') 
    for row_dict in nodes_dict:  
        new_dict = {key: str(value) for key, value in row_dict.items()}
        graph["nodes"].append(new_dict)
    

    df2 = pd.read_excel('nodes.xlsx',sheet_name=1)  # 读取第二个sheet
    edges_dict = df2.to_dict('records') 
    for row_dict in edges_dict:  
        new_dict = {key: str(value) for key, value in row_dict.items()}
        graph["edges"].append(new_dict)


    with open('data.json', 'w') as f:  
    # 使用 json.dump() 方法将字典写入文件  
        json.dump(graph, f)