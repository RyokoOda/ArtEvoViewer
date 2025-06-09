# coloring.py
import matplotlib.pyplot as plt
import json
import os

def load_category_mappings():
    """
    category_color.json から 'artstyle' および 'nationality' の辞書を読み込む。
    """
    this_dir = os.path.dirname(__file__)
    json_path = os.path.join(this_dir, 'category_colors.json')
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        artstyle_mapping = data.get('artstyle', {})
        nationality_mapping = data.get('nationality', {})
        return artstyle_mapping, nationality_mapping
    except Exception:
        return {}, {}

# グローバル変数として一度だけ読み込む
ARTSTYLE_MAPPING, NATIONALITY_MAPPING = load_category_mappings()

def color_by_year(artist):
    """ 年ベースのカラーリング（artist['year'] を利用） """
    year = artist.get('year', 1270)
    if year is None:
        return 'rgb(128,128,128)'  # year が None の場合はデフォルトグレー
    min_year, max_year = 1270, 2022
    norm = (year - min_year) / (max_year - min_year)
    cmap = plt.get_cmap('viridis')
    rgba = cmap(norm)
    return f'rgb({int(rgba[0]*255)},{int(rgba[1]*255)},{int(rgba[2]*255)})'

def color_by_palette(artist):
    """ 固定色パレットを用いるカラーリング（artist['cluster_number'] を利用） """
    try:
        index = int(artist.get('cluster_number', 0))
    except Exception:
        index = 0
    palette = ['red', 'green', 'blue', 'orange', 'purple']
    return palette[index % len(palette)]

def color_by_artstyle(artist):
    """
    artstyle によるカラーリング:
      - artist['artstyle'] の値をリスト化し（カンマ区切りまたはリストの場合に対応）小文字に変換
      - ルネサンス系サブカテゴリ（early-renaissance, high-renaissance, northern-renaissance,
        proto-renaissance, mannerism-late-renaissance）は "renaissance" に統一
      - グローバル変数 ARTSTYLE_MAPPING の登録順に探索し、該当する artstyle を採用する
      - 見つからなければデフォルト 'rgb(128,128,128)' を返す
    """
    artstyle_data = artist.get('artstyle', None)
    if not artstyle_data:
        return 'rgb(128,128,128)'

    if isinstance(artstyle_data, str):
        artstyles = [s.strip().lower() for s in artstyle_data.split(',')]
    elif isinstance(artstyle_data, list):
        artstyles = [str(s).strip().lower() for s in artstyle_data]
    else:
        artstyles = [str(artstyle_data).strip().lower()]

    # ルネサンス系サブカテゴリを "renaissance" に統一
    renaissance_subs = {'early-renaissance', 'high-renaissance', 'northern-renaissance', 'proto-renaissance', 'mannerism-late-renaissance'}
    artstyles = ['renaissance' if a in renaissance_subs else a for a in artstyles]

    # ARTSTYLE_MAPPING の登録順に探索
    for style in ARTSTYLE_MAPPING:
        if style in artstyles:
            return ARTSTYLE_MAPPING.get(style, 'rgb(128,128,128)')
    return 'rgb(128,128,128)'

def color_by_nationality(artist):
    """
    nationality によるカラーリング:
      - artist['nationality'] の値をリスト化し（カンマ区切りまたはリストの場合に対応）小文字に変換
      - グローバル変数 NATIONALITY_MAPPING の登録順に探索し、該当する国籍を採用
      - 見つからなければデフォルト 'rgb(128,128,128)' を返す
    """
    nat_data = artist.get('nationality', None)
    if not nat_data:
        return 'rgb(128,128,128)'

    if isinstance(nat_data, str):
        nats = [s.strip().lower() for s in nat_data.split(',')]
    elif isinstance(nat_data, list):
        nats = [str(s).strip().lower() for s in nat_data]
    else:
        nats = [str(nat_data).strip().lower()]

    for nat in NATIONALITY_MAPPING:
        if nat in nats:
            return NATIONALITY_MAPPING[nat]
    return 'rgb(128,128,128)'

def color_default(artist):
    """ その他の場合は固定の色を返す """
    return 'rgb(128,128,128)'

def get_coloring_function(method):
    """
    カラーリング方法名に応じた関数を返すファクトリ関数。
    返される関数は artist オブジェクトを受け取り、色を返す。
    """
    if method == 'year':
        return color_by_year
    elif method == 'palette':
        return color_by_palette
    elif method == 'artstyle':
        return color_by_artstyle
    elif method == 'nationality':
        return color_by_nationality
    else:
        return color_default
