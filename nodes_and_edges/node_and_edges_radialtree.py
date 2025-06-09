import json
import matplotlib.pyplot as plt
from .coloring import get_coloring_function

# 平均制作年をベースにして色を決定する
def get_color(year):
    if year is None:
        # year が None の場合、デフォルトの色を返す
        return f'rgb(128, 128, 128)'  # グレー
    
    year = int(year)
    min_year, max_year = 1270, 2022
    norm = (year - min_year) / (max_year - min_year) # 正規化
    cmap = plt.get_cmap('viridis') # カラーマップの指定
    rgba = cmap(norm)
    # フォーマットを直して返す
    return f'rgb({int(rgba[0]*255)}, {int(rgba[1]*255)}, {int(rgba[2]*255)})'


### nodeのデータを作る
# data      : id, label, color, display, highlightからなる
# poaition  : 座標の位置を整数で示したもの。x, yの属性を持つ
# cluster   : 同じクラスタに属する画家のリスト。labelが羅列されている。
# year      : 制作年
# parents   : 親ノード
# children  : 子ノード
###
def create_nodes_for_cyto(nodes, position_radialtree, coloring_method):

    # カラーリング手法を選択
    color_func = get_coloring_function(coloring_method)

    for node in nodes:
        # position
        node_id = node['data']['id']
        for radial_node in position_radialtree:
            if radial_node['data']['id'] == node_id:
                position = radial_node['position']
                node["position"] = {'x': position['x'], 'y': position['y']}
        
        # color
        node['data']['color'] = color_func(node)

        node['data']['type'] = 'node'
        #クラスタ
        node['cluster'] = []

        # display
        node['data']['display'] = 1
        node['data']['highlight'] = 30

        
    return nodes


def create_elements_radialtree(dir_path, json_path, coloring):

    ### ノードとエッジのデータを読み込む
    with open(dir_path + '/node_dict.json') as f1:
        nodes = json.load(f1)

    with open(dir_path + '/edge_dict.json') as f2:
        edges = json.load(f2)

    # jsonファイルを読み込む
    with open(json_path) as f3:
        position_radialtree = json.load(f3)
    
    nodes_for_network = create_nodes_for_cyto(nodes, position_radialtree, coloring)

    return nodes_for_network, edges