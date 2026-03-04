"""
AIを使ったリスト作成ツール - CSVクレンジング・都道府県別分割
"""

import pandas as pd
import os
import re

# ============================================================
# 設定（必要に応じて変更してください）
# ============================================================

INPUT_FILE = "input.csv"          # 入力CSVファイル名
OUTPUT_DIR = "output"             # 出力先フォルダ
ENCODING = "utf-8-sig"            # 文字コード（Shift-JISの場合は "cp932"）

# 列名マッピング（元CSVの列名 → 統一名）
COLUMN_MAP = {
    # 例: "会社名": "社名", "住所": "所在地", "〒": "郵便番号"
    # 実際のCSVに合わせて変更してください
}

# 除外キーワード（社名・所在地にこれらが含まれる行を削除）
EXCLUDE_KEYWORDS = [
    "サイバー", "組合", "モータープール", "駐", "基金"
]

# 都道府県リスト
PREFECTURES = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
    "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
    "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
    "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
]

# ============================================================
# メイン処理
# ============================================================

def load_csv(filepath):
    """CSVファイルを読み込む"""
    try:
        df = pd.read_csv(filepath, encoding=ENCODING, dtype=str)
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding="cp932", dtype=str)
    df = df.fillna("")
    print(f"読み込み完了: {len(df)}行")
    return df


def rename_columns(df):
    """列名を統一名に変換する"""
    if COLUMN_MAP:
        df = df.rename(columns=COLUMN_MAP)
    # 必須列が存在しない場合は作成
    for col in ["社名", "所在地", "郵便番号"]:
        if col not in df.columns:
            df[col] = ""
    return df[["社名", "所在地", "郵便番号"]]


def remove_duplicates(df):
    """住所の重複を除外する"""
    before = len(df)
    df = df.drop_duplicates(subset=["所在地"])
    print(f"重複除外: {before - len(df)}行削除 → {len(df)}行")
    return df


def remove_excluded_keywords(df):
    """除外キーワードに該当する行を削除する"""
    before = len(df)
    pattern = "|".join(EXCLUDE_KEYWORDS)
    mask = df["社名"].str.contains(pattern, na=False) | \
           df["所在地"].str.contains(pattern, na=False)
    df = df[~mask]
    print(f"除外キーワード除去: {before - len(df)}行削除 → {len(df)}行")
    return df


def extract_prefecture(address):
    """住所から都道府県名を抽出する"""
    for pref in PREFECTURES:
        if pref in address:
            return pref
    return "不明"


def remove_prefecture_from_address(df):
    """所在地から都道府県名を削除する"""
    pattern = "|".join(PREFECTURES)
    df["所在地"] = df["所在地"].str.replace(pattern, "", regex=True)
    return df


def split_by_prefecture(df):
    """都道府県ごとにDataFrameを分割する"""
    df["都道府県"] = df["所在地_original"].apply(extract_prefecture)
    groups = {}
    for pref, group in df.groupby("都道府県"):
        groups[pref] = group.drop(columns=["都道府県", "所在地_original"])
    return groups


def save_outputs(groups):
    """都道府県ごとにCSVファイルを出力する"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for pref, df in groups.items():
        filename = os.path.join(OUTPUT_DIR, f"{pref}.csv")
        df.to_csv(filename, index=False, encoding=ENCODING)
        print(f"  保存: {filename} ({len(df)}行)")
    print(f"\n完了！{OUTPUT_DIR}/ フォルダに{len(groups)}ファイルを出力しました。")


def main():
    print("===== CSVリスト整理ツール 開始 =====\n")

    # 1. 読み込み
    df = load_csv(INPUT_FILE)

    # 2. 列名を統一
    df = rename_columns(df)

    # 3. 都道府県抽出用に元の住所を保持
    df["所在地_original"] = df["所在地"]

    # 4. 重複除外
    df = remove_duplicates(df)

    # 5. 除外キーワード処理
    df = remove_excluded_keywords(df)

    # 6. 住所から都道府県名を削除
    df = remove_prefecture_from_address(df)

    # 7. 都道府県ごとに分割
    groups = split_by_prefecture(df)

    # 8. CSV出力
    print(f"\n都道府県別に出力中...")
    save_outputs(groups)


if __name__ == "__main__":
    main()
