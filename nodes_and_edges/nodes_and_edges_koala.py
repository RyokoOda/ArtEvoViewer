import csv
import matplotlib.pyplot as plt
import json
from .coloring import get_coloring_function


# クラスタのデータを作る
def create_cluster_data(node_data):
    cluster = {}
    for i in range(len(node_data)):
        cluster_number = node_data[i][3]
        if not cluster_number in cluster:
            cluster[cluster_number] = [node_data[i][4] + ' ' + node_data[i][5]]
        else:
            cluster[cluster_number].append(node_data[i][4] + ' ' + node_data[i][5])
    
    return cluster

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
def create_nodes_for_cyto(node_data, clusters, dir_path, coloring_method):

    # カラーリング手法を選択
    color_func = get_coloring_function(coloring_method)

    # 画家データを読み込む
    with open(dir_path+'/node_dict.json') as f:
        artist_dict = json.load(f)
    
    nodes = []

    for artist in artist_dict:
        position = {}
        find_flag = False

        for i in range(len(node_data)):
            if node_data[i][4] == artist['artist_name']:
                # 座標値
                position['x'] = int(float(node_data[i][1])*1000)
                position['y'] = int(float(node_data[i][2])*1000)
                artist['position'] = position

                # 色
                # カラーリングの切り替え
                artist['data']['color'] = color_func(artist)

                # クラスタ
                artist['cluster'] = clusters[node_data[i][3]]

                # その他、ノードの大きさとネットワークに表示するかの設定
                artist['data']['highlight'] = 30 # ノードの大きさ
                artist['data']['display'] = 1 # ネットワークに表示するかどうか

                nodes.append(artist)
                find_flag = True
                break
        
        if not find_flag:
            artist['position'] = {'x':0, 'y':0}
            artist['data']['color'] = 'gray'
            artist['data']['display'] = 0
            artist['data']['highlight'] = 30
            artist['cluster'] = []

            nodes.append(artist)

    return nodes

### エッジのデータを作る
# data      : source, targetの属性を持つ。各々エッジの始点と終点を表すIDを格納している。
###
def create_edges_for_cyto(dir_path):
    with open(dir_path + '/edge_dict.json') as f2:
        edges = json.load(f2)
    
    gt_set = load_gt_edges()
    
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


### csvファイルを読み込み、ノードとエッジのデータを作る
def csv_reader_koala(dir_path, csv_path, coloring):
    # csvファイルを読み込む
    with open(csv_path) as f:
        reader = csv.reader(f)
        original_data = [row for row in reader]

    # ノードとエッジの数を取得
    node_number = int(original_data[0][1])
    edge_number = int(original_data[node_number+1][1])

    # データを分ける
    node_data = original_data[1:node_number+1]

    edge_data = []
    for i in range(edge_number):
        edge_data.append(original_data[node_number+2+2*i])
    
    # データの成形
    clusters = create_cluster_data(node_data)
    nodes = create_nodes_for_cyto(node_data, clusters, dir_path, coloring)
    edges = create_edges_for_cyto(dir_path)

    return nodes, edges