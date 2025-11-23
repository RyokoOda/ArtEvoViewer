from dash import Dash, html, dcc
import dash_cytoscape as cyto
import os
import json

import stylesheet
from nodes_and_edges.format_controller import NodesAndEdges
from callbacks import register_callbacks
from generate_colorbar import generate_colorbar

app = Dash(__name__)


### ノードとエッジのデータを成形する
n_and_e = NodesAndEdges('20230915', 'color_only', 'HierarchyTree', 'year') # ディレクトリ名と可視化手法を指定
n_and_e.make_nodes_and_edges() # nodesとedgesの作成
nodes, edges = n_and_e.nodes, n_and_e.edges

# 初期状態
INITIAL_THRESHOLD = 0.2

for e in edges:
    w = float(e['data'].get('weight', 0))
    # しきい値以上だけ visible=True にして、それ以外は False
    e['data']['visible'] = "True" if w >= INITIAL_THRESHOLD else "False"
    
DEFAULT_ELEMENTS = nodes + edges

### 画家の名前と画像のファイル名の対応をとったデータを読み込む
# データセット名を指定
dataset_name = '20230915'  # 必要に応じて変更
# 辞書を取得
picture_dict_path = os.path.join('./data', dataset_name, 'picture_dict.json')
with open(picture_dict_path, "r") as f:
    picture_dict = json.load(f)


### スタイルを書いたリストを読み込む
my_stylesheet = stylesheet.my_stylesheet
css = stylesheet.CSSSTYLES


### ドロップボックスの選択肢の設定
DIRECTORIS = [{'label': 'color', 'value': 'color_only'},
              {'label': 'brushstroke', 'value': 'local_feature_for_top50_1000'},
              {'label': 'theme', 'value': 'clip'},
              {'label': 'color+brushstroke', 'value': 'color_local'},
              {'label': 'color+theme', 'value': 'color_clip'},
              {'label': 'brushstroke+theme', 'value': 'local_clip'},
              {'label': 'color+brushstroke+theme', 'value': 'color_local_clip'},
              ]

VISUALIZATION_METHODS = [{'label': 'HierarchyTree', 'value': 'HierarchyTree'},
                         {'label': 'HierarchyTreeYear', 'value': 'HierarchyTreeYear'},
                         #{'label': 'Koala', 'value': 'Koala'},
                         {'label': 'RadialTree', 'value': 'RadialTree'}
                         ]

COLORING = [{'label': 'year', 'value': 'year'},
            {'label': 'art_style', 'value': 'artstyle'},
            {'label': 'nationality', 'value': 'nationality'},]


### アプリの作り込み
app.layout = html.Div(style=css['app'],children=[
    dcc.Store(id='elements-store', data=DEFAULT_ELEMENTS),  # デフォルトelementsを保存
    dcc.Location(id='url', refresh=True),

    # ダミー
    html.Div(id='dummy-output'),

    html.Header(className='header', style=css['header'], children=[
        html.H1(style=css['title'], children=["ArtEvoViewer"]),
        # 検索ボックス
        dcc.Input(id="node-search", value='', type="text", placeholder="input artist name", style=css['search-box']),
    ]),


    html.Div(style=css['container'], children=[
        html.Article(className='viewer', style=css['article'], children=[
        
        # ドロップダウンメニュー（ディレクトリと手法の選択）
        html.Div([
            # Directory選択
            html.Div([html.Label("Features:"),
                dcc.Dropdown(id='directory-dropdown', options=DIRECTORIS, value='color_only')],
                style=css['directory-dropdown']),
            # Visualization Method選択
            html.Div([html.Label("Visualization Method:"),
                dcc.Dropdown(id='method-dropdown', options=VISUALIZATION_METHODS, value='HierarchyTree')],
                style=css['directory-dropdown']),
        ],style=css['dropdown-menu']),

        html.Div([
            # Coloring選択
            html.Div([html.Label("Colored by:"),
                dcc.Dropdown(id='coloring-dropdown', options=COLORING, value='year')],
                style=css['coloring-dropdown']),
            
            # エゴネットワークとリセットボタン
            html.Div(style=css['egonet-and-reset'], children=[
                html.Div(style=css['ego-checkbox'], children=[
                    dcc.Checklist(id='ego-checkbox', options=[{'label': 'Show Ego Network', 'value': 'show_egonet'}], value=[]),
                ]),
                html.Div(style=css['reset-button'], children=[
                    html.Button("Reset Network", id='reset-button')
                ]),
            ]),
        ],style=css['dropdown-menu']),
        
        # エッジの制御をするスライドバー
        html.Div([
            html.Div([html.Label("Edge:")], style=css['slider-label']),
            html.Div([
                dcc.Slider(
                    id='weight-slider',
                    min=0.0, max=0.3, step=0.01, value=0.2, updatemode='drag',
                    marks={
                        0:  {'label': 'More'},   # 左端 0.0
                        0.3:  {'label': 'Fewer'},  # 右端 max
                    },
                )],
                id='weight-slider-output',
                style=css['slider']),
        ],style=css['slide-bar']),   

        # グラフ本体
        cyto.Cytoscape(
            id='graph',
            layout={'name': 'preset',
                    'animate': True},
            style = css['viewer'],
            stylesheet=my_stylesheet,
            elements=DEFAULT_ELEMENTS
            ),

        # カラーバー
        html.Div([
            html.Img(id='colorbar-img', src=generate_colorbar('year'), 
                     style={'width': '100%', 'position': 'center'})
        ], style={'textAlign': 'center', 'padding': '20px'})
        ]),


        # プロパティ表示
        html.Aside(style=css['aside'], className='painter-data', children=[
            
            # タイトル
            html.Div(style=css['tab'], children=[
                html.P(["Node Information"])
            ]),

            html.Div(style=css['node-info'], children=[
                html.Div(style=css['upper'], children=[
                    # 画家情報左部
                    html.Div(style=css['name-and-wiki'], children=[
                        html.Div(style=css['name_field'], children=[
                            html.Div(children=[
                                # ノードに対応する画家の名前
                                html.Label('Artist Name :', htmlFor='painter-data', style=css['label']),
                                html.Pre(id='painter-data', style=css['painter_name']),
                            ]),
                        ]),
                        html.Div(style=css['name_field'], children=[
                            html.Div(children=[
                                # Wikipediaのリンク
                                html.Label('Wikipedia :', htmlFor='wiki_link', style=css['label']),
                                html.Pre(id='wiki_link', style=css['painter_name']),
                            ]),
                        ]),
                    ]),
                    # 画家情報右部
                    html.Div(style=css['other-attriburte'], children=[
                        # ラベルたち
                        html.Div(style=css['labels'], children=[
                            html.P('Born :', style=css['other-attribute-label']),
                            html.P('Died :', style=css['other-attribute-label']),
                            html.P('Nationality :', style=css['other-attribute-label']),
                            html.P('Art Style :',style=css['other-attribute-label']),
                        ]),
                        # ボックスたち
                        html.Div(style=css['preboxes'], children=[
                            html.Pre(id='born', style=css['painter_name']),
                            html.Pre(id='died', style=css['painter_name']),
                            html.Pre(id='nationality', style=css['painter_name']),
                            html.Pre(id='artstyle', style=css['painter_name']),
                        ]),
                    ]),
                ]),

                html.Hr(style=css['border']),

                html.Div(style=css['lower'], children=[
                    # 親ノード・子ノードの一覧
                    html.Div(style=css['parents-children-node'], children=[
                            # 隣接ノード(親)
                            html.Label('Parants Nodes :', htmlFor='parents-data', style=css['label']),
                            html.Pre(id='parants-data', style=css['painter_name']),
                            # 隣接ノード(子)
                            html.Label("Children Nodes :", htmlFor='children-data', style=css['label']),
                            html.Pre(id='children-data', style=css['pre']),
                            # クラスタ
                            html.Label("Related Nodes :", htmlFor='cluster-data', style=css['label']),
                            html.Pre(id='cluster-data', style=css['pre'])
                    ]),

                     # 画像表示
                    html.Div(style=css['image-field'], children=[
                        # 中央
                        html.Div(style=css['artist-and-cluster-image'], children=[
                            # 画家
                            html.Label('Images of Artist :', htmlFor='painter_paintings', style=css['label']),
                            html.Pre(id='painter_painting', style=css['image-box-small']),

                            # クラスタ
                            html.Label('Images of related nodes :', htmlFor='cluster_paintings', style=css['label']),
                            html.Pre(id='cluster_paintings', style=css['image-box-large']),
                        ]),
                        # 右
                        html.Div(style=css['parents-and-children-image'], children=[
                            # 親ノード
                            html.Label('Images of Parents Nodes :', htmlFor='parents_paintings', style=css['label']),
                            html.Pre(id='parents_paintings', style=css['image-box-small']),
                            # 子ノード
                            html.Label('Images of Children Nodes :', htmlFor='children_paintings', style=css['label']),
                            html.Pre(id='children_paintings', style=css['image-box-large'])
                        ]),
                    ]),
                ]),


            ]),
        ]),
    ])
])


# コールバック関数
register_callbacks(app, picture_dict, DEFAULT_ELEMENTS)

if __name__ == '__main__':
    app.run(debug=True)