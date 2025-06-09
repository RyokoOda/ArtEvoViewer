from .nodes_and_edges_koala import csv_reader_koala
from .node_and_edges_radialtree import create_elements_radialtree
import os

class NodesAndEdges :
    
    ### コンストラクタ
    # dir_path  : 読み込みたいデータが入ったディレクトリのパス
    # method    : 可視化手法
    # coloring  : カラーリングの種類
    # nodes     : ノードの情報を格納したもの
    # edges     : エッジの情報を格納したもの
    ###
    def __init__(self, directory, network, method, coloring):
        self.dir_path   = os.path.join('./data', directory, network)
        self.method     = method
        self.coloring   = coloring
        self.nodes      = []
        self.edges      = []
    
    ### 異なる仕様のファイルから、nodesとedgesを作成する関数
    def make_nodes_and_edges(self):
        if self.method == 'Koala': # 手法がKoalaのとき
            file_name = 'layout.csv' # ファイル名は 'layout.csv'
            file_path = os.path.join(self.dir_path, file_name)
            self.nodes, self.edges = csv_reader_koala(self.dir_path, file_path, self.coloring) # nodesとedgesを作成
        
        if self.method == 'HierarchyTree': # 手法が階層型木構造のとき
            file_name = 'hierarchy_tree.json' # ファイル名は 'hierarchy_tree.json'
            file_path = os.path.join(self.dir_path, file_name)
            self.nodes, self.edges = create_elements_radialtree(self.dir_path, file_path, self.coloring) # nodesとedgesを作成
        
        if self.method == 'Radial': # 手法が階層型木構造のとき
            file_name = 'radial_tree.json'
            file_path = os.path.join(self.dir_path, file_name)
            self.nodes, self.edges = create_elements_radialtree(self.dir_path, file_path, self.coloring) # nodesとedgesを作成
        
        if self.method == 'ForceLayout': # 手法が階層型木構造のとき
            file_name = 'force_layout_positions.json'
            file_path = os.path.join(self.dir_path, file_name)
            self.nodes, self.edges = create_elements_radialtree(self.dir_path, file_path, self.coloring) # nodesとedgesを作成
        
        if self.method == 'HierarchyTreeYear': # 手法が階層型木構造のとき
            file_name = 'hierarchy_tree_year.json'
            file_path = os.path.join(self.dir_path, file_name)
            self.nodes, self.edges = create_elements_radialtree(self.dir_path, file_path, self.coloring) # nodesとedgesを作成
        
        if self.method == 'RadialTree': # 手法が階層型木構造, radial
            file_name = 'radial_tree_dfs.json'
            file_path = os.path.join(self.dir_path, file_name)
            self.nodes, self.edges = create_elements_radialtree(self.dir_path, file_path, self.coloring) # nodesとedgesを作成