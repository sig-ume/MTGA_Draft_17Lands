## Windows / Python 3.12 / venv セットアップ手順（コマンドのみ）

# 利用可能な Python バージョン確認
py -0p

# Python 3.12 で venv 作成
py -3.12 -m venv venv

# venv 有効化
venv\Scripts\activate

# venv 内の Python バージョン確認
python --version

# pip 更新（必ず python -m 経由）
python -m pip install --upgrade pip

# 依存関係インストール
python -m pip install -r requirements.txt

# アプリ起動
python main.py
