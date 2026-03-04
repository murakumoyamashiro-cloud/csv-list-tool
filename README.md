# CSVリスト整理ツール

CSVデータを読み込み、クレンジング・都道府県別に自動分割するPythonツールです。

## 機能

- CSVの読み込みと項目名の統一（社名・所在地・郵便番号）
- 住所の重複除外
- 除外キーワードに該当する行の自動削除（例：組合・基金・モータープール 等）
- 住所から都道府県名を削除
- 都道府県ごとにCSVファイルを自動分割出力

## 使い方

1. `input.csv` を同じフォルダに置く
2. 必要に応じて `csv_list_tool.py` 内の設定を変更する
3. 以下を実行する

\`\`\`bash
pip install pandas
python csv_list_tool.py
\`\`\`

4. `output/` フォルダに都道府県別のCSVが出力される

## 設定項目

| 設定項目 | 説明 |
|---|---|
| `INPUT_FILE` | 入力CSVのファイル名 |
| `OUTPUT_DIR` | 出力先フォルダ名 |
| `COLUMN_MAP` | 元CSVの列名を統一名にマッピング |
| `EXCLUDE_KEYWORDS` | 除外するキーワードのリスト |

## 動作環境

- Python 3.x
- pandas
