import pandas as pd
import networkx as nx
from datetime import datetime

def process_csv(file_path):
    # 读取CSV文件
    print("开始输入时间:", datetime.now())
    df = pd.read_csv(file_path, usecols=['id', 'parent_id', 'is_valid_user'], dtype=str)

    # 创建有向图
    G = nx.DiGraph()
    
    # 加入节点和边
    for _, row in df.iterrows():
        G.add_node(row['id'], is_valid_user=row['is_valid_user'])
        if not pd.isna(row['parent_id']):
            G.add_edge(row['parent_id'], row['id'])

    print("写入完成时间:", datetime.now())

    # 缓存每个节点的层级和下线人数
    levels = {}
    descendants_cache = {}
    
    def calculate_level(node, current_level):
        """递归计算节点的层级"""
        if node in levels:
            return levels[node]
        levels[node] = current_level
        for child in G.successors(node):
            calculate_level(child, current_level + 1)
        return levels[node]

    def calculate_descendants(node):
        """递归计算节点的下线人数和有效下线人数"""
        if node in descendants_cache:
            return descendants_cache[node]
        
        descendants = set()
        valid_descendants = 0
        
        for child in G.successors(node):
            child_descendants, child_valid_descendants = calculate_descendants(child)
            descendants.add(child)
            descendants.update(child_descendants)
            valid_descendants += child_valid_descendants
        
        # 如果节点本身是有效用户，则增加计数
        if G.nodes[node]['is_valid_user'] == '1':
            valid_descendants += 1

        descendants_cache[node] = (descendants, valid_descendants)
        return descendants_cache[node]

    def calculate_descendant_levels(node):
        """计算当前节点的下级层级数（最大下级层级数）"""
        max_level = 0  # 最深层级数初始化为0
        for child in G.successors(node):
            child_level = calculate_descendant_levels(child) + 1  # 递归加1计算层级
            max_level = max(max_level, child_level)
        return max_level  # 返回最大下级层级数，不减去当前节点的层级数

    def get_upline_path(node):
        """获取上级链路（从节点到根节点的路径）"""
        path = []
        current_node = node
        while True:
            predecessors = list(G.predecessors(current_node))
            if not predecessors:
                break  # 根节点没有父节点
            current_node = predecessors[0]
            path.append(current_node)
        return path

    # 计算每个节点的层级、下线人数、有效下线人数、直推人数、上级链路、下级层级数
    print("开始计算时间:", datetime.now())
    results = []
    for node in G.nodes:
        level = calculate_level(node, 1)  # 将初始层级设为 1
        descendants, valid_descendants = calculate_descendants(node)
        num_direct_referrals = len(list(G.successors(node)))  # 直推人数
        upline_path = get_upline_path(node)  # 获取上级链路
        descendant_levels = calculate_descendant_levels(node)  # 计算下级层级数
        results.append({
            'id': node,
            'level': level,
            'descendant_levels': descendant_levels,  # 下级层级数
            'num_descendants': len(descendants),
            'num_valid_descendants': max(valid_descendants - 1, 0),  # 确保不小于0
            'num_direct_referrals': num_direct_referrals,  # 直推人数
            'upline_path': '|'.join(reversed(upline_path))  # 上级链路
            
        })

    print("计算完成时间:", datetime.now())

    # 转换为DataFrame并保存为CSV
    result_df = pd.DataFrame(results)
    result_df.to_csv('output.csv', index=False)

    print("输出完成时间:", datetime.now())

# 使用示例
process_csv('input.csv')
