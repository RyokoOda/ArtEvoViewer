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

# 正解データを読み込む
def load_gt_edges():
    gt_path = "/Users/r.o/Documents/color_network/Art-Evolution-Viewer/create_data/ReferenceNetworkAnalysis/InfluenceNetowrk_oil.txt"
    id_path = "/Users/r.o/Documents/color_network/Art-Evolution-Viewer/data/artist_and_ids.json"

    with open(id_path) as f:
        name_to_id = json.load(f)

    gt_id_set = set()

    with open(gt_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            child_name, _, parent_name = line.split("\t")

            # ID に変換できるものだけ使う
            if child_name in name_to_id and parent_name in name_to_id:
                child_id = name_to_id[child_name]
                parent_id = name_to_id[parent_name]
                gt_id_set.add((child_id, parent_id))

    return gt_id_set

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


def create_edges_for_cyto(edges, gt_set=None):

    if gt_set is None:
        return edges

    for edge in edges:
        child = edge["data"]["target"]
        parent = edge["data"]["source"]

        # 正解データに含まれるか？
        if (child, parent) in gt_set:
            edge["data"]["color"] = "red"
            edge["data"]["width"] = 10
            edge["data"]["index"] = 9999
            edge["data"]["weight"] += 1
        else :
            edge["data"]["color"] = weight_to_gray_color(edge["data"]["weight"])
            edge["data"]["width"] = 1 + 2*edge["data"]["weight"]
            edge["data"]["index"] = 0

    return edges

### グレーの色をエッジの重みで作成する
def weight_to_gray_color(weight, gamma=1.2):
    """
    weight: 0〜1
    背景 #F0F0F0 (240) より必ず濃く表示されるグレーを返す
    """

    # クリップ
    w = max(0.0, min(weight, 1.0))

    # 非線形（低重みをさらに薄く）
    w_gamma = w ** gamma

    # グレー範囲
    gray_min = 0    # 濃い側（はっきり）
    gray_max = 200   # ← 背景(240)より確実に濃い

    gray = int(gray_max - w_gamma * (gray_max - gray_min))

    return f"rgb({gray}, {gray}, {gray})"


def create_elements_radialtree(dir_path, json_path, coloring):

    ### ノードとエッジのデータを読み込む
    with open(dir_path + '/node_dict.json') as f1:
        nodes = json.load(f1)

    with open(dir_path + '/edge_dict.json') as f2:
        edges = json.load(f2)

    # jsonファイルを読み込む
    with open(json_path) as f3:
        position_radialtree = json.load(f3)
    
    # 正解データを読み込む
    gt_set = load_gt_edges()

    # ノードとエッジを作り替える
    nodes_for_network = create_nodes_for_cyto(nodes, position_radialtree, coloring)
    edges_for_network = create_edges_for_cyto(edges, gt_set)

    return nodes_for_network, edges_for_network