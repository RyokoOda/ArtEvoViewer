import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import os
import json

# ファイルの読み込み用関数
def load_mapping_file():
    """nodes_and_edges/category_colors.json を読み込む"""
    this_dir = os.path.dirname(__file__)
    json_path = os.path.join(this_dir, 'nodes_and_edges/category_colors.json')
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception:
        return {}

# artstyle 辞書を取り出すための関数
def get_artstyle_mapping():
    """読み込んだ JSON から 'artstyle' の辞書を返す"""
    data = load_mapping_file()
    return data.get('artstyle', {})

# nationality 辞書を取り出すための関数
def get_nationality_mapping():
    """読み込んだ JSON から 'nationality' の辞書を返す"""
    data = load_mapping_file()
    return data.get('nationality', {})

# グローバル変数として一度だけ読み込む
ARTSTYLE_MAPPING = get_artstyle_mapping()
NATIONALITY_MAPPING = get_nationality_mapping()

def generate_colorbar_year():
    # year 用カラーバーの定義
    cmap = plt.get_cmap('viridis')
    norm = plt.Normalize(vmin=1270, vmax=2022)

    # カラーバーを作成
    fig, ax = plt.subplots(figsize=(10, 1))
    fig.subplots_adjust(bottom=0.5)
    cb = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap),
                      cax=ax, orientation='horizontal')
    cb.set_label('Year', fontsize=13)
    cb.ax.tick_params(labelsize=13)

    # 画像として保存
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)

    # 画像を base64 形式に変換して返す
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

def generate_colorbar_from_mapping(mapping, cols=3, fig_width=10, cell_height=1.0, fontsize=13):
    """
    mapping の順番をそのまま利用し、固定列数 (cols) で複数行にわたるカラーバーを生成する。
    各セル内に、色のボックス（左）とラベル（右、fontsize=fontsize）を配置する。
    """
    items = list(mapping.items())
    n = len(items)
    if n == 0:
        return ""
    
    rows = int(np.ceil(n / cols))
    fig, ax = plt.subplots(figsize=(fig_width, rows * cell_height))
    ax.set_axis_off()

    cell_w = 1.0 / cols
    cell_h = 1.0 / rows

    for i, (label, rgb) in enumerate(items):
        col = i % cols
        row = i // cols
        x0 = col * cell_w
        y0 = 1 - (row + 1) * cell_h

        # セル内に色のボックスを配置（セル左側 25%）
        box_w = 0.25 * cell_w
        box_h = 0.6 * cell_h
        # "rgb(r,g,b)" 形式の文字列から正規化されたタプルに変換
        nums = rgb.strip("rgb()").split(',')
        r = int(nums[0].strip()) / 255.
        g = int(nums[1].strip()) / 255.
        b = int(nums[2].strip()) / 255.
        color = (r, g, b)
        rect = plt.Rectangle((x0 + 0.05 * cell_w, y0 + 0.2 * cell_h), box_w, box_h, facecolor=color)
        ax.add_patch(rect)
        # セル内の右側にテキストを配置
        text_x = x0 + 0.05 * cell_w + box_w + 0.05 * cell_w
        text_y = y0 + cell_h / 2
        ax.text(text_x, text_y, label, fontsize=fontsize, va='center', wrap=True)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

def generate_colorbar_artstyle():
    # artstyle 用カラーバーの生成（共通関数を利用）
    return generate_colorbar_from_mapping(ARTSTYLE_MAPPING, cols=3, fig_width=10, cell_height=1.0, fontsize=13)

def generate_colorbar_nationality():
    # nationality 用カラーバーの生成（共通関数を利用）
    return generate_colorbar_from_mapping(NATIONALITY_MAPPING, cols=3, fig_width=10, cell_height=1.0, fontsize=13)

def generate_colorbar(coloring):
    if coloring == 'year':
        return generate_colorbar_year()
    elif coloring == 'artstyle':
        return generate_colorbar_artstyle()
    elif coloring == 'nationality':
        return generate_colorbar_nationality()
    else:
        return ""
