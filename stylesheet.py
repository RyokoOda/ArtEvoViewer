# dash cytoscape用のスタイルシート

STYLESHEET = [
    # Group selectors
    #{
    #    'selector': 'node',
    #    'style': {
    #        'content': 'data(label)'
    #    }
    #},

    # Class selectors
    {
        'selector': '.violet',
        'style': {
            'background-color': 'darkviolet',
            'line-color': 'darkviolet'
        }
    },
    {
        'selector': '.blue',
        'style': {
            'background-color': 'blue',
            'line-color': 'blue'
        }
    },
    {
        'selector': '.light_blue',
        'style': {
            'background-color': 'deepskyblue',
            'line-color': 'deepskyblue'
        }
    },
    {
        'selector': '.emerald',
        'style': {
            'background-color': 'darkcyan',
            'line-color': 'darkcyan'
        }
    },
    {
        'selector': '.green',
        'style': {
            'background-color': 'green',
            'line-color': 'green'
        }
    },
    {
        'selector': '.light_green',
        'style': {
            'background-color': 'lawngreen',
            'line-color': 'lawngreen'
        }
    },
    {
        'selector': '.yellow',
        'style': {
            'background-color': 'yellow',
            'line-color': 'yellow'
        }
    },
    {
        'selector': '.orange',
        'style': {
            'background-color': 'orange',
            'line-color': 'orange'
        }
    },
    {
        'selector': '.red',
        'style': {
            'background-color': 'red',
            'line-color': 'red'
        }
    },
    {
        'selector': '.purple',
        'style': {
            'background-color': 'mediumvioletred',
            'line-color': 'mediumvioletred'
        }
    },
    {
        'selector': '.pink',
        'style': {
            'background-color': 'magenta',
            'line-color': 'magenta'
        }
    },
    {
        'selector': '.gray',
        'style': {
            'background-color': 'gray',
            'line-color': 'gray'
        }
    },
    {
    'selector': '.highlighted',
    'style': {
        'background-color': 'red',  # 背景色を赤にする
        'line-color': '#FF4136',    # エッジの色
        'width': '50px',            # ノードの幅を大きくする
        'height': '50px',           # ノードの高さを大きくする
        'border-width': '5px',      # 境界線の太さを増やす
        'border-color': '#FF4136',  # 境界線の色
        'fontSize': '20px',        # ラベルのフォントサイズを大きくする
        'color': '#FFFFFF',         # ラベルの色を白にする
        'text-valign': 'center',    # テキストをノードの中央に配置する
        'text-halign': 'center'     # テキストをノードの中央に配置する
    }
}
]

my_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': 'data(color)',  # 各ノードのスタイルに従う
            'label': 'data(label)',  # ラベルをデータに基づいて表示
            'text-opacity': 0,  # ラベルを見えなくする
            'opacity':'data(display)', # ノードを表示するかどうか
            'width': 'data(highlight)', # ノードの大きさ
            'height': 'data(highlight)',
            'border-width': 2,            # 縁の太さ（px）
            'border-color': 'gray',       # 縁の色
            'border-opacity': 1,          # 不透明度（0〜1）
            'border-style': 'solid',      # 線種（solid, dotted, dashed…）
        }
    }
]

CSSSTYLES = {
    'app': {
        'margin': 0,
        'padding': 0,
    },
    'header': {
        'width': '100%',
        'height': '40px',
        'fontSize': '15px',
        'color': '#A49070',
        'background': '#F0F0F0',
        'display': 'flex',         # Flexboxを使用
        'alignItems': 'center',    # 上下中央に配置
        'justifyContent': 'space-between',  # 左右にスペースを確保
        'padding': '0 10px',          # 両端の余白を追加
    },
    'title': {
        'marginLeft': '2%',
    },
    'search-box': {
        'width': '30%',             # 検索ボックスの幅を調整
        'display': 'flex',         # Flexboxを使用
        'alignItems': 'center',    # 上下中央に配置
        'marginRight': '2%',
    },
    'border': {
        'size':"0.5",
        'align':"center",
        'color':"#B2CDBA",
        'width':'95%',
        'boxShadow': 'none',           # 影を消去
    },
    'viewer': {
        'height': '520px',
        'width': '90%',
        'background': '#F0F0F0',
        #'background': '#FAFAF0',
        #'background': '#FFFFFF',
        'paddingLeft': '5%',
        'marginTop': '10px'
    },
    'article': {
        'height': '100%',
        'width': '80%',
        'color': '#08B0D1',
        #'background': 'blue',
        'fontFamily': 'Courier New',
        'fontSize': '80%',
        'paddingLeft': '10px',
        'marginTop': '10px'
    },
    'container': {
        'display': 'flex'
    },
    'egonet-and-reset' : {
        'paddingTop' : '10px',
        'display': 'flex',
        'flexDirection': 'column',
        'width' : '45.5%'
    },
    'ego-checkbox' : {
        'width' : '100%',
        'marginLeft' : '8%',
    },
    'reset-button' : {
        'width' : '100%',
        'paddingLeft' : '8%',
        'paddingTop' : '5px',
        'fontFamily': 'Courier New',
        'color' : '#08B0D1',
    },
    'aside': {
        'display': 'flex',
        'flexDirection': 'column',
        'width': '100%',
        'paddingTop': '10px',
        'overflowX': 'scroll',
        #'background': 'red',
        'fontFamily': 'Courier New'
    },
    'node-info': {
        'background': '#F0F0F0',
        'height' : '600px',
    },
    'upper' : {
        'display': 'flex',
        'flexDirection': 'row',
    },
    'name-and-wiki' : {
        'paddingLeft' : '3%',
        'width' : '38%',
        'paddingTop':'10px',
    },
    'other-attriburte' : {
        'paddingLeft' : '5%',
        'paddingRight' : '3%',
        'width' : '51%',
        'display': 'flex',
        'flexDirection': 'row',
        #'background' : 'red'
    },
    'labels' : {
        'width' : '40%',
        'display': 'flex',
        'flexDirection': 'column',
    },
    'preboxes' :{
        'width' : '60%',
        'display': 'flex',
        'flexDirection': 'column',
    },
    'tab': {
        'background': '#B2CDBA',
        'color': '#FFFFFF',
        'position': 'right',
        'paddingLeft': '20px',
        'font': 'sans-serif',
        'marginBottom': '10px'
    },
    'label': {
        'width': '100%',
        'fontSize': '13px',
        'color': '#08B0D1',
    },
    'other-attribute-label': {
        'width': '100%',
        'fontSize': '13px',
        'color': '#08B0D1',
        'height' : '25%',
        'verticalAlign': 'middle',
        'paddingTop' : '5%'
    },
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'hidden',
        'width': '100%',
        'height': '80px',
        'color': '#A49070',
        'background': '#F9F9F9',
        'paddingLeft' : '2%',
        #'overflow-x': 'hidden' # 横スクロールバーを非表示
    },
    'painter_name': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
        'width': '100%',
        'height': '30px',
        'background': '#F9F9F9',
        'color': '#A49070',
        'paddingLeft' : '2%',
    },
    'lower' : {
        'display': 'flex',
        'flexDirection': 'row',
    },
    'parents-children-node' : {
        'paddingLeft' : '3%',
        'width' : '30%',
        'paddingTop':'10px',
    },
    'image-field':{
        'paddingLeft' : '3%',
        'width' : '61%',
        'paddingTop':'10px',
        'display': 'flex',
        'flexDirection': 'row',
    },
    'artist-and-cluster-image':{
        'width' : '48%',
        'display': 'flex',
        'flexDirection': 'column',
    },
    'parents-and-children-image':{
        'width' : '48%',
        'display': 'flex',
        'flexDirection': 'column',
        'paddingLeft' : '4%',
    },
    'image-box-small': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
        'position': 'right',
        'width': '100%',
        'height': '80px',
        'background': '#F9F9F9',
    },
    'image-box-large': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
        'position': 'right',
        'width': '100%',
        'height': '160px',
        'background': '#F9F9F9',
    },
    'name_field':{
        'display': 'flex',
        'flexDirection': 'column',
    },
    'image_insidebox':{
        'display': 'grid',
        'gridTemplateColumns': '100px 100px'
    },
    'image': {
        'width': '80px',
        #'marginLeft': '5px'
    },
    'directory-dropdown': {
        'display': 'flex',
        'flexDirection': 'column',
        'width': '45.5%',
        'paddingLeft': '3%',
        'marginTop': '10px',
    },
    'coloring-dropdown': {
        'display': 'flex',
        'flexDirection': 'column',
        'width': '45.5%',
        'paddingLeft': '3%',
        #'marginTop': '10px',
        'marginBottom': '10px',
    },
    'dropdown-menu':{
        'display': 'flex',
        'width': '95%',
        'height': '65px',
        'background':'#F0F0F0',
    },
    'dropdown-top':{
        'display': 'flex',
        'flexDirection': 'row',
    },

}