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

### Koalaのnode_idの一覧. KoalaのIDから、ノードデータのIDを検索する。
def make_node_id_in_Koala(node_data, dir_path):
    # 画家データを読み込む
    with open(dir_path+'/node_dict.json') as f:
        artist_dict = json.load(f)
    
    # Koala内のノードidと対応させる
    node_id_Koala = {}
    for node in node_data:
        for artist in artist_dict:
            if artist['artist_name'] == node[4]:
                node_id_Koala[node[0]] = {'name': node[4], 'id': artist['data']['id']}
    
    return node_id_Koala



### エッジのデータを作る
# data      : source, targetの属性を持つ。各々エッジの始点と終点を表すIDを格納している。
###
def create_edges_for_cyto(edge_data, node_id):
    edges = []
    for i in range(len(edge_data)):
        edge = {}
        data = {}

        source_id = edge_data[i][1]
        target_id = edge_data[i][2]

        # 始点ノードと終点ノードのidを追加
        data['source'] = node_id[source_id]['id']
        data['target'] = node_id[target_id]['id']
        edge['data'] = data
        edges.append(edge)
    
    return edges


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
    node_id = make_node_id_in_Koala(node_data, dir_path)
    edges = create_edges_for_cyto(edge_data, node_id)

    # エッジデータを読み込む
    #with open(dir_path+'/edge_dict.json') as f:
    #    edges = json.load(f)


    return nodes, edges


if __name__ == '__main__':
    csv_reader_koala()