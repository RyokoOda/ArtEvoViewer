from dash import html, Input, Output, State
from PIL import Image
from nodes_and_edges.format_controller import NodesAndEdges
import stylesheet
import copy
import time
import os
from nodes_and_edges.coloring import get_coloring_function
from generate_colorbar import generate_colorbar

### データセットの指定
# TODO: データセット変更の仕組みを実装
selected_directory = '20230915'

### スタイルを書いたリストを読み込む
css = stylesheet.CSSSTYLES

### 定数
# 画像ディレクトリのパス
PICTURE_DIRECTORY =  './picture/20230915/ImageSimple'

### キャッシュ用のデフォルトエレメント
n_and_e = NodesAndEdges('20230915', 'color_only', 'HierarchyTree', 'year') # ディレクトリ名と可視化手法を指定
n_and_e.make_nodes_and_edges() # nodesとedgesの作成
nodes, edges = n_and_e.nodes, n_and_e.edges

### ユーティリティ関数

# 親ノードのIDを取得
def find_parents_node(node, default_elements):
    if node:
        node_id = node['id']
        for element in default_elements:
            if 'id' in element['data']:
                if element['data']['id'] == node_id:
                    if 'parents' in element:
                        parents_id = element['parents']['id']
                        return parents_id
    return None

# 子ノードのIDを取得
def find_children_node(node, default_elements):
    if node:
        node_id = node['id']
        for element in default_elements:
            if 'id' in element['data']:
                if element['data']['id'] == node_id:
                    if 'children' in element:
                        children_id = element['children'][0]['id']
                        return children_id
    return None

# IDからdefault_elementsを検索し、中身を返す
def find_node_by_id(target_id, default_elements):
    for element in default_elements:
        if 'label' in element['data']:
            if element['data']['id'] == target_id:
                return element
    return None

# アノテーション表示用にクラスタに所属する画家名を整形する
def format_for_anotation(cluster_artist_names):
    ordered_artists = ""
    for i in range(len(cluster_artist_names)):
        ordered_artists +=  cluster_artist_names[i] + "\n"
    return ordered_artists

# アノテーション表示用にノードの辞書のリストから画家名を整形する
def format_for_anotation_by_nodedict(artist_dict):
    artists_name = []

    # 単一の辞書形式の場合はリスト形式に直す
    if type(artist_dict) == dict:
        artist_dict = [artist_dict]

    for artist in artist_dict:
        artists_name.append(artist['name'])
    
    return artists_name

# 絵画表示用に画像を整形する
def format_images(picture_names):
    children = []
    for i in range(len(picture_names)):
        picture_name = os.path.join(PICTURE_DIRECTORY, picture_names[i])
        try:
            img = Image.open(picture_name)
        except FileNotFoundError:
            picture_name = change_image_name(picture_name)
            img = Image.open(picture_name)
        children.append(html.Img(src=img, style=css['image']))
    return html.Div(style=css['image_insidebox'], children=children)

# ファイル名の％と＿を読み替える
# WindowsとMacの命名規則の違いを考慮するため
def change_image_name(image_name):
    new_image_name = ''
    for c in image_name:
        if c=='%':
            new_image_name += '_'
            continue
        new_image_name += c
    return new_image_name

# クラスタに所属する画家の作品をリスト形式で抽出する
def create_list_of_images(cluster_painters, picture_dict):
    # 表示する画像の枚数
    picture_number = 1
    
    cluster_picture_names = []
    for i in range(len(cluster_painters)):
        painter_name = (cluster_painters[i].split(' ')[0]) # 画家の名前を切り出す
        picture_names = picture_dict[painter_name][0:0+picture_number] # 画像名を取り出す
        cluster_picture_names.extend(picture_names)
    return cluster_picture_names

### 可視化手法更新
def get_cached_elements(directory, network, method, coloring):
    n_and_e = NodesAndEdges(directory, network, method, coloring)
    n_and_e.make_nodes_and_edges()
    return n_and_e.nodes , n_and_e.edges

### エゴネットワーク取得
import copy

def _is_edge(el):
    d = el.get("data", {})
    return ("source" in d) and ("target" in d)

def _edge_is_visible(e):
    d = e.get("data", {})
    # あなたの方式：display='none' は除外
    if d.get("display", "element") == "none":
        return False
    # visible 方式併用ならこれも
    v = d.get("visible", None)
    if v in (False, "False", 0, "0"):
        return False
    return True

def build_single_parent_maps(elements):
    """
    elements（全体、スライダー等反映済み）から
    各ノードの「最強親(重み最大)」を1本だけ選び、
    parent_of と children_of を作る
    """
    nodes = [el for el in elements if not _is_edge(el)]
    edges = [el for el in elements if _is_edge(el) and _edge_is_visible(el)]

    node_by_id = {str(n["data"]["id"]): n for n in nodes}

    # targetごとに最強incoming edge を1本選ぶ
    best_in = {}  # target_id -> edge
    for e in edges:
        s = str(e["data"]["source"])
        t = str(e["data"]["target"])
        if t not in node_by_id or s not in node_by_id:
            continue
        w = float(e["data"].get("weight", 0.0))

        if t not in best_in:
            best_in[t] = e
        else:
            w_prev = float(best_in[t]["data"].get("weight", 0.0))
            # tie-break（同率なら source id が小さい方、など）で安定化
            if (w > w_prev) or (w == w_prev and int(s) < int(best_in[t]["data"]["source"])):
                best_in[t] = e

    parent_of = {}    # child -> parent
    children_of = {}  # parent -> [child,...]
    for t, e in best_in.items():
        s = str(e["data"]["source"])
        parent_of[t] = s
        children_of.setdefault(s, []).append(t)

    # 子リストも安定化（見た目の揺れ防止）
    for p in children_of:
        children_of[p].sort(key=lambda x: int(x))

    return node_by_id, best_in, parent_of, children_of

def build_ego_single_parent(center_id, elements):
    """
    単体親ネットワークと同じ挙動のエゴ：
      - 親：1本チェーン（最強親のみ）
      - 子：単体親ネットワーク上の子（＝children_of）を再帰的に全部
      - 使うエッジも「最強親として選ばれた1本」だけ
      - 参照元は elements-store（全体）なので一本道固定バグが出ない
    """
    center_id = str(center_id)
    node_by_id, best_in, parent_of, children_of = build_single_parent_maps(elements)

    if center_id not in node_by_id:
        return [], []

    ego_ids = set([center_id])

    # 親チェーン（最強親のみ）
    cur = center_id
    while cur in parent_of:
        p = parent_of[cur]
        if p in ego_ids:
            break
        ego_ids.add(p)
        cur = p

    # 子孫（単体親ネットワークの子だけ）
    stack = [center_id]
    while stack:
        nid = stack.pop()
        for c in children_of.get(nid, []):
            if c in ego_ids:
                continue
            ego_ids.add(c)
            stack.append(c)

    # ノード・エッジ（単体親の採用エッジのみ）
    ego_nodes = [copy.deepcopy(node_by_id[_id]) for _id in ego_ids]
    ego_nodes.sort(key=lambda x: int(x["data"]["id"]))

    ego_edges = []
    for child_id in ego_ids:
        if child_id in best_in:
            e = best_in[child_id]
            s = str(e["data"]["source"])
            t = str(e["data"]["target"])
            if s in ego_ids and t in ego_ids:
                ego_edges.append(copy.deepcopy(e))

    return ego_nodes, ego_edges

# ラベルを検索ように正規化する
def normalize_label(label: str) -> str:
    """
    ラベルを検索用に正規化する関数:
    ・小文字化
    ・前後の余分な空白の除去
    ・スペースをハイフンに変換
    """
    return label.strip().lower().replace(" ", "-")

### コールバック関数ここから
def register_callbacks(app, picture_dict, default_elements):

# 各関数内で、インタラクティブ操作から取ってくるelementsの中身は、
# id, label, timestampのみ
    
    # 可視化手法の切り替え
    @app.callback(
        Output('elements-store', 'data', allow_duplicate=True),
        Output('graph', 'elements', allow_duplicate=True),
        [Input('directory-dropdown', 'value'), Input('method-dropdown', 'value'), Input('coloring-dropdown', 'value'), State('weight-slider', 'value')],
        prevent_initial_call=True
        )
    def update_elements_store(selected_network, selected_method, selected_coloring, weight):
        updated_nodes, updated_edges = get_cached_elements(selected_directory, selected_network, selected_method, selected_coloring)
        for e in updated_edges:
            if float(e['data'].get('weight', 0)) >= weight:
                e['data']['display'] = "True"
            else:
                e['data']['display'] = "False"
        return updated_nodes + updated_edges, updated_nodes + updated_edges

    # ネットワークリセット
    # TODO: なぜか場所が保存されたままなので、場所も元の位置に戻せるようにする
    @app.callback(
        Output('graph', 'elements', allow_duplicate=True),
        Input("reset-button", "n_clicks"),
        State('directory-dropdown', 'value'),
        State('method-dropdown', 'value'),
        Input('coloring-dropdown', 'value'),
        State('weight-slider', 'value'),
        prevent_initial_call=True
        )
    def reset_network(n_clicks, selected_network, selected_method, selected_coloring, weight):
        updated_nodes, updated_edges = get_cached_elements(selected_directory, selected_network, selected_method, selected_coloring)
        for e in updated_edges:
            if float(e['data'].get('weight', 0)) >= weight:
                e['data']['display'] = "True"
            else:
                e['data']['display'] = "False"
        return updated_nodes + updated_edges
    
    ### 画家情報のアノテーション
    # ホバーで画家のデータを表示
    @app.callback(
        Output('painter-data', 'children'),
        Input('graph', 'mouseoverNodeData'))
    def display_painter_data(elements):
        if elements:
            return elements['label']

    # ホバーでクラスタに属する画家群を表示
    @app.callback(
        Output('cluster-data', 'children'),
        Input('graph', 'mouseoverNodeData'),
        State('graph', 'elements'))
    def display_cluster_data(element, current_elements):
        if element:
            current_node = find_node_by_id(element['id'], current_elements)
            if 'cluster' in current_node:
                cluster_painters = current_node['cluster']
                return format_for_anotation(cluster_painters)
            
        return "There isn't cluster"
    
    # ホバーで親ノードのデータを表示
    @app.callback(
        Output('parants-data', 'children'),
        Input('graph', 'mouseoverNodeData'),
        State('graph', 'elements'))
    def display_parents_data(element, current_elements):
        if not element:
            return "There is no parent node."
        
        current_node = find_node_by_id(element['id'], current_elements) # 対象のノードの情報を取得
        if current_node:
            if 'parents' in current_node:
                parents_nodes = current_node['parents']
                parents_names = format_for_anotation_by_nodedict(parents_nodes)
                return format_for_anotation(parents_names)

        return "There is no parent node."
    
    # ホバーで子ノードのデータを表示
    @app.callback(
        Output('children-data', 'children'),
        Input('graph', 'mouseoverNodeData'),
        State('graph', 'elements'))
    def display_children_data(element, current_elements):
        if not element:
            return "There is no parent node."

        current_node = find_node_by_id(element['id'], current_elements) # 対象のノードの情報を取得
        if current_node:
            if 'children' in current_node:
                children_nodes = current_node['children']
                children_names = format_for_anotation_by_nodedict(children_nodes)
                return format_for_anotation(children_names)
        return "There is no children node."
    
    # ホバーでWikipediaのリンクを表示
    @app.callback(
        Output('wiki_link', 'children'),
        Input('graph', 'mouseoverNodeData'),
        State('graph', 'elements'))
    def display_wiki_link(element, current_elements):
        if not element:
            return None
        current_node = find_node_by_id(element['id'], current_elements)
        if current_node:
            return current_node['wikipedia']
        
    # ホバーで生まれの情報を表示
    @app.callback(
        Output('born', 'children'),
        Input('graph', 'mouseoverNodeData'),
        State('graph', 'elements'))
    def display_born(element, current_elements):
        if not element:
            return None
        current_node = find_node_by_id(element['id'], current_elements)
        if current_node:
            if current_node['born']['date'] == None:
                when = '- '
            else:
                when = current_node['born']['date']
            
            if current_node['born']['place'] == None:
                where = '-'
            else:
                where = current_node['born']['place']
            return when + '; ' + where
    
    # ホバーで死亡の情報を表示
    @app.callback(
        Output('died', 'children'),
        Input('graph', 'mouseoverNodeData'),
        State('graph', 'elements'))
    def display_died(element, current_elements):
        if not element:
            return None
        current_node = find_node_by_id(element['id'], current_elements)
        if current_node:
            if current_node['died']['date'] == None:
                when = '- '
            else:
                when = current_node['died']['date']
            
            if current_node['died']['place'] == None:
                where = '-'
            else:
                where = current_node['died']['place']
            return when + '; ' + where
    
    # ホバーで国籍を表示
    @app.callback(
        Output('nationality', 'children'),
        Input('graph', 'mouseoverNodeData'),
        State('graph', 'elements'))
    def display_nationality(element, current_elements):
        if not element:
            return None
        current_node = find_node_by_id(element['id'], current_elements)
        if current_node:
            return current_node['nationality']
    
    # ホバーで様式を表示
    @app.callback(
        Output('artstyle', 'children'),
        Input('graph', 'mouseoverNodeData'),
        State('graph', 'elements'))
    def display_artstyle(element, current_elements):
        if not element:
            return None
        current_node = find_node_by_id(element['id'], current_elements)
        if current_node:
            return current_node['artstyle']
    
    ### 画像表示
    # クリックで画家の画像を表示
    @app.callback(
        Output('painter_painting', 'children'),
        Input('graph', 'tapNodeData'))
    def display_painter_painting(elements):
        # 表示する画像の枚数
        picture_number = 12
        
        if elements:
            # id(画家名 年代)から画家名のみを切り出す
            painter_name = elements['label'].split(' ')[0]
            # 辞書を画家名で検索し、作品のファイル名を取得する
            picture_names = picture_dict[painter_name][0:picture_number]
            return format_images(picture_names)

        return None

    # クリックでクラスタに属する画家たちのの画像を表示
    @app.callback(
        Output('cluster_paintings', 'children'),
        Input('graph', 'tapNodeData'),
        State('graph', 'elements'))
    def display_cluster_painting(element, current_elements):

        if element:
            current_node = find_node_by_id(element['id'], current_elements)
            if 'cluster' in current_node:
                cluster_painters = current_node['cluster']
                cluster_picture_names = create_list_of_images(cluster_painters, picture_dict)
                return format_images(cluster_picture_names)
            
        return None
    
    # クリックで親ノードのクラスタの画像を表示
    @app.callback(
        Output('parents_paintings', 'children'),
        Input('graph', 'tapNodeData'),
        State('graph', 'elements'))
    def display_parents_painting(element, current_elements):
        if not element:
            return None
        
        current_node = find_node_by_id(element['id'], current_elements)
        if current_node:
            if 'parents' in current_node:
                parents_nodes = current_node['parents']
                parents_names = format_for_anotation_by_nodedict(parents_nodes)
                parents_picture_names = create_list_of_images(parents_names, picture_dict)
                return format_images(parents_picture_names)
        
        return None
    
    # クリックで子ノードのクラスタの画像を表示
    @app.callback(
        Output('children_paintings', 'children'),
        Input('graph', 'tapNodeData'),
        State('graph', 'elements'))
    def display_parents_painting(element, current_elements):
        
        if not element:
            return None
        
        current_node = find_node_by_id(element['id'], current_elements)
        if current_node:
            if 'children' in current_node:
                children_nodes = current_node['children']
                children_names = format_for_anotation_by_nodedict(children_nodes)
                children_picture_names = create_list_of_images(children_names, picture_dict)
                return format_images(children_picture_names)
        
        return None
    
    ### エゴネットワークの表示
    @app.callback(
        Output('graph', 'elements', allow_duplicate=True),
        [Input('graph', 'tapNodeData'), Input('ego-checkbox', 'value')],
        State('graph', 'elements'),
        State('elements-store', 'data'),
        prevent_initial_call=True
    )
    def render_graph_elements(current_element, checkbox, current_elements, all_elements):
        if not checkbox:
            return current_elements
        if not current_element:
            return current_elements
        ego_nodes, ego_edges = build_ego_single_parent(str(current_element.get('id')), all_elements)
        for n in ego_nodes:
            n['data']['highlight'] = 60
        return ego_nodes + ego_edges

    ### 検索ボックスで該当の画家を強調
    # TODO 元の色に戻すとき、エッジがつながっていないノードも戻す
    @app.callback(
        Output('elements-store', 'data', allow_duplicate=True),
        Input('node-search', 'n_submit'),  # Enterキーが押されたとき
        State('node-search', 'value'),      # 検索ボックスの値
        State('graph', 'elements'),          # 現在のelements
        prevent_initial_call=True,
    )
    def search_node(n_submit, search_value, elements):

        # ユーザー入力を正規化する
        normalized_search = normalize_label(search_value) if search_value else ""
        
        # まずは全てのノードをグレーにする
        new_elements = copy.deepcopy(elements)
        for element in new_elements:
            if 'label' in element['data']:
                if normalized_search and normalized_search in element['data']['label']:
                    element['data']['color'] = 'red'
                    element['data']['highlight'] = 60
                    element['data']['display'] = 1
                else:
                    # 検索値に一致しない場合は 'gray' クラスを付与
                    element['data']['color'] = 'gray'
                    element['data']['highlight'] = 30
                    element['data']['display'] = 1
    
        return new_elements
    
    ### ノードのカラーリングを変更
    @app.callback(
        Output('elements-store', 'data', allow_duplicate=True),
        Input('coloring-dropdown', 'value'),
        State('graph', 'elements'),
        prevent_initial_call=True,
    )
    def update_node_colors(selected_coloring, elements):
        new_elements = copy.deepcopy(elements)
        color_func = get_coloring_function(selected_coloring)
        for element in new_elements:
            if 'label' in element['data']:
                # ここでは、artist の情報が element['data'] に入っていると仮定しています
                element['data']['color'] = color_func(element)
        return new_elements

    ### カラーバーを変更
    @app.callback(
        Output('colorbar-img', 'src'),
        Input('coloring-dropdown', 'value')
    )
    def update_colorbar(selected_coloring):
        # generate_colorbar() はカラーリングに応じた画像を返すと仮定
        return generate_colorbar(selected_coloring)
    
    ### エッジを重みでフィルター
    @app.callback(
        Output('graph', 'elements'),
        Input('weight-slider', 'value'),
        State('graph', 'elements'),
    )
    def filter_edges_by_weight(threshold, elements):

        # nodes と edges を分ける
        nodes = [el for el in elements if 'source' not in el.get('data', {})]
        edges = [el for el in elements if 'source' in el.get('data', {})]

        # weight のある edges のみフィルタ
        for e in edges:
            if float(e['data'].get('weight', 0)) >= threshold:
                e['data']['display'] = "True"
            else:
                e['data']['display'] = "False"

        new_elements = nodes + edges

        return new_elements