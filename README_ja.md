# MTGA_Draft_17Lands

17Landsのデータを利用したMagic: The Gathering Arenaドラフトツール。

**このアプリケーションは、新しいセットがArenaでリリースされ、[17Landsのカード評価データ](https://www.17lands.com/card_ratings)が利用可能になり次第、自動的にサポートします。**

**サポート対象イベント:** プレミア・ドラフト、マッチ・ドラフト、クイック・ドラフト、シールド、マッチ・シールド
  
![Premier_Draft](https://github.com/unrealities/MTGA_Draft_17Lands/blob/main/assets/96687942/9d7283ff-cb8b-46f9-8d72-7bf531d707b1.png)

## 目次

- [MTGA\_Draft\_17Lands](#mtga_draft_17lands)
  - [目次](#目次)
  - [実行手順: Windows実行ファイル (Windowsのみ)](#実行手順-windows実行ファイル-windowsのみ)
  - [実行手順: Python (Windows/Mac/Linux)](#実行手順-python-windowsmaclinux)
  - [開発環境のセットアップ](#開発環境のセットアップ)
  - [Windows実行ファイルのビルド手順](#windows実行ファイルのビルド手順)
  - [UI機能](#ui機能)
  - [メニュー機能](#メニュー機能)
  - [追加機能](#追加機能)
  - [設定](#設定)
  - [ファイルの場所](#ファイルの場所)
    - [設定ファイル (`config.json`)](#設定ファイル-configjson)
    - [データセット](#データセット)
    - [ログ](#ログ)
  - [カードロジック](#カードロジック)
  - [P1P1の解決策](#p1p1の解決策)
    - [問題点](#問題点)
    - [解決策](#解決策)
    - [今後の展望](#今後の展望)
  - [ティアリスト (API提供型)](#ティアリスト-api提供型)
    - [仕組み](#仕組み)
    - [使い方](#使い方)
  - [シグナル検出 (ベータ)](#シグナル検出-ベータ)
  - [データセット通知](#データセット通知)
    - [データセットが見つからない場合](#データセットが見つからない場合)
    - [不足しているデータセット](#不足しているデータセット)
    - [データセットの更新が利用可能な場合](#データセットの更新が利用可能な場合)
  - [トラブルシューティング](#トラブルシューティング)
    - [既知の問題](#既知の問題)
    - [Arenaログの問題](#arenaログの問題)
      - [プレミアおよびマッチ・ドラフト](#プレミアおよびマッチ・ドラフト)
      - [クイック・ドラフト](#クイック・ドラフト)
      - [シールドおよびマッチ・シールド](#シールドおよびマッチ-シールド)

## 実行手順: Windows実行ファイル (Windowsのみ)

- **ステップ 1:** [リリースページ](https://github.com/unrealities/MTGA_Draft_17Lands/releases)から最新のzipファイルをダウンロードします。
- **ステップ 2:** 解凍し、exeファイルをダブルクリックしてインストールを開始します。
- **ステップ 3:** (任意) インストール先のフォルダに移動し、実行ファイル（`MTGA_Draft_Tool.exe`）を右クリックして「プロパティ」を選択。「互換性」タブから「管理者としてこのプログラムを実行する」にチェックを入れます。
  - この手順は、アプリケーションが書き込み制限のあるディレクトリ（`Program Files`や`Program Files (x86)`など）にインストールされている場合にのみ必要です。
  - ドライブのメインディレクトリ（`C:/`や`D:/`など）や`Users/<ユーザー名>/`ディレクトリにインストールされている場合は不要です。
- **ステップ 4:** Arena内で「オプション設定」→「アカウント」へ進み、「詳細ログ (プラグインサポート)」のチェックボックスをオンにします。
- **ステップ 5:** `MTGA_Draft_Tool.exe`をダブルクリックしてプログラムを開始します。
- **ステップ 6:** 利用予定のセットをダウンロードします (`Data->Download Dataset`)。
  - イベントデータセットは異なるイベント間で使用可能です（例：プレミア・ドラフトのデータセットをシールドイベントで使用できます）。
  - クイック・ドラフトをプレイする場合、開始直後などはプレミア・ドラフトのデータセットを使用することを検討してください。
- **ステップ 7:** [設定ウィンドウ](#設定)でツールを設定します。
  - 17Landsに馴染みのない方は、勝率パーセンテージよりも[勝率評価（グレード）](#カードロジック)（`Win Rate Format: Grade`）の方が価値を感じられるかもしれません。
  - [UI Size](#設定)設定で画像やテキストのサイズを調整できます。
- **ステップ 8:** Arenaでドラフトを開始します。
  - Arenaのログには、プレミア・ドラフトとマッチ・ドラフトの P1P1 (1パック目1手目) はP1P2が記録されるまで表示されません。
  - `Refresh`ボタンを押すと、OCRが最初のパックのカードを特定するのに役立ちます。詳細については、[P1P1の解決策](#p1p1の解決策)をご覧ください。
    - [カード比較](#メニュー機能)機能もP1P1の代替として使用できます。
  - シールドのカードプールは、[ピック済みカードウィンドウ](#メニュー機能)で確認できます。

## 実行手順: Python (Windows/Mac/Linux)

- **ステップ 1:** `MTGA_Draft_17Lands-main.zip`ファイルを[ダウンロード](https://github.com/unrealities/MTGA_Draft_17Lands/archive/refs/heads/main.zip)して解凍するか、リポジトリをクローンします。
  - 3.10 リリース以降、いくつかの Python 関連のバグ修正が行われています。3.10 リリースではなく、[メインブランチ](https://github.com/unrealities/MTGA_Draft_17Lands/archive/refs/heads/main.zip)からコードをダウンロードしてください。
- **ステップ 2:** Python 3.12 をダウンロードしてインストールします。
  - [Windows](https://www.python.org/downloads/windows/)
  - [Mac](https://www.python.org/downloads/macos/)
  - [Linux](https://wiki.python.org/moin/BeginnersGuide/Download#Linux)
- **ステップ 3:** ターミナルを開き、```python --version``` を入力して、```Python 3.12.*``` と表示されることを確認します。
- **ステップ 4:** ```python -m ensurepip --upgrade``` を入力して、Pythonパッケージインストーラー Pip をインストール/アップグレードします。
- **ステップ 5:** ターミナルで ```pip install -r requirements.txt``` を入力して、依存関係をインストールします。
- **ステップ 6:**
  - (Macのみ) `/Applications/Python 3.##/` に移動し、`Install Certificates.command` ファイルをダブルクリックしてWeb証明書をインストールします。
  - (Linuxのみ) [Tkをインストール](https://tkdocs.com/tutorial/install.html#installlinux)します。
- **ステップ 7:** Arena内で「オプション設定」→「アカウント」へ進み、「詳細ログ (プラグインサポート)」のチェックボックスをオンにします。
- **ステップ 8:** ターミナルで ```python main.py``` を入力してアプリケーションを起動します。
- **ステップ 9:** アプリケーションが Arena の `Player.log` の場所を尋ねてきたら、`File->Read Player.log` をクリックし、以下のいずれかの場所からログファイルを選択します：
  - **Windows:** {ドライブ}/Users/{ユーザー名}/AppData/LocalLow/Wizards Of The Coast/MTGA/Player.log
  - **Mac:** {ユーザー名}/Library/Logs/Wizards Of The Coast/MTGA/Player.log
  - **Bottles (Linux):** /home/{ユーザー名}/.var/app/com.usebottles.bottles/data/bottles/bottles/MTG-Arena/drive_c/users/{ユーザー名}/AppData/LocalLow/Wizards Of The Coast/MTGA/Player.log
  - **Lutris (Linux):** /home/{ユーザー名}/Games/magic-the-gathering-arena/drive_c/users/{ユーザー名}/AppData/LocalLow/Wizards Of The Coast/MTGA/Player.log
- **ステップ 10:** (Macのみ) Arena をウィンドウモードに設定します。
- **ステップ 11:** 利用予定のセットをダウンロードします (`Data->Download Dataset`)。
  - イベントデータセットは異なるイベント間で使用可能です。
  - `Arena Cube` を選択し、開始日を調整することで、最新の Arena Cube イベントのデータをダウンロードできます。
  - クイック・ドラフトをプレイする場合、開始直後などはプレミア・ドラフトのデータセットを使用することを検討してください。
- **ステップ 12:** [設定ウィンドウ](#設定)でツールを設定します。
- **ステップ 13:** Arenaでドラフトを開始します。

## 開発環境のセットアップ

コード品質ツールを含む開発環境を構築したいコントリビューターの方は、以下のコマンドを実行してください。

```bash
python setup_dev.py
```

このコマンド一つで以下のことが行われます：
- `requirements.txt` からすべての依存関係をインストール
- 開発ツール（pre-commit, black, ruff）のインストール
- pre-commit hooks のセットアップ

pre-commit hooks は、コミット時にコードを自動的にフォーマットし、不備をチェック（Linter）することで、一貫したコード品質を保ちます。

## Windows実行ファイルのビルド手順

**注意:** このプロジェクトでは、以下の手順を実行するために [GitHub Actions](https://github.com/unrealities/MTGA_Draft_17Lands/actions/workflows/build-windows-exe.yml) を使用しています。

- **ステップ 1:** Python 3.12 をダウンロードしてインストールします。
- **ステップ 2:** ```python -m ensurepip --upgrade``` を入力して Pip をインストールします。
- **ステップ 3:** ターミナルで以下のコマンドを入力します。
  - ```pip install -r requirements.txt```
  - ```pip install pywin32==306```
  - ```pip install pyinstaller==6.7.0```
- **ステップ 4:** [Inno Setupをダウンロード](https://jrsoftware.org/isdl.php#stable) します。
- **ステップ 5:** ```python -m PyInstaller  main.py --onefile --noconsole -n MTGA_Draft_Tool --clean``` を入力してビルドします。
  - ビルドに失敗する場合は、Windowsの「ウイルスと脅威の防止」で除外設定を追加する必要があります。
- **ステップ 6:** Inno Setup で `Installer.iss` を開き、Build->Compile をクリックします。
  - `{app}` フォルダにある `mysetup.exe` を `setup.exe` にリネームし、`MTGA_Draft_17Lands` のメインフォルダに移動させます。

## UI機能

- **Current Draft:** アプリケーションが識別した現在のドラフトタイプ（プレミア、クイック、マッチなど）を表示します。
  - プレミアおよびマッチ・ドラフトでは、P1P2 が記録されるまで P1P1 は Arena のログに表示されません。
  - [設定ウィンドウ](#設定)で `Enable Current Draft Display` をオフにすることで非表示にできます。
- **Data Source:** アプリケーションがカードデータを取得している現在のドラフトタイプを表示します。
  - アプリケーションは、現在のドラフトタイプとセットに対応するデータを取得しようとします（例：プレミア・ドラフトなら `NEO_PremierDraft_Data.json`）。対応するデータが見つからない場合は、同じセットの別のデータファイルを使用しようとします。
  - 有効なデータファイルが見つからない場合は "None" と表示されます。
  - [設定ウィンドウ](#設定)で `Enable Data Source Options` をオフにすることで非表示にできます。
  - 特定のユーザーグループ（"Top", "Middle", "Bottom"）を選択できます。デフォルトは "All" です。[ユーザーグループの定義](https://www.17lands.com/metrics_definitions)
- **Deck Filter:** デッキの色によるフィルタリングを行うドロップダウンです。
  - 数値の隣のパーセンテージは、その色の組み合わせの勝率を表します（17Landsの [color rating ページ](https://www.17lands.com/color_ratings) から取得）。
  - `All Decks` はすべての色の組み合わせの総合評価を表示します。
  - `Auto` オプションは、最初の15ピックまでは `All Decks` を維持し、その後、取得したカードに最適なフィルタに自動的に切り替えます。
- **Refresh Button:** ログの読み込みをトリガーします。
  - [P1P1の解決策](#p1p1の解決策) を使用して、P1P1 のカードを見つけることができます。
  - アプリケーションは自動的に新しいログを読み込むため、通常このボタンは Windows 7 や 8 などの古い OS でのみ必要です。
- **Pack / Pick Table:** 現在のパックに含まれるカードを表示するテーブルです。
  - データが見つからない場合（`Data Source: None`）や未認識のカードがある場合、名前の列に番号が表示されます。
- **Missing Cards Table:** 既に見たことのあるパックから消えた（他のプレイヤーにピックされた）カードを表示します。
  - 自分が選んだカードの名前の横にはアスタリスク（*）が表示されます。
- **Draft Stats Table:** クリーチャー、非クリーチャー、およびドラフト中に取得したすべてのカードの分布と合計を表示します。
  - 数字の列はマナコスト (CMC) を表します。
- **Signals Table:** 5色の各色について計算された「シグナルスコア」を表示します。詳細は [シグナル検出](#シグナル検出-ベータ) を参照してください。

## メニュー機能

![Settings_Dark](https://github.com/unrealities/MTGA_Draft_17Lands/blob/main/assets/96687942/642a0795-e407-410e-b8d6-6332f3083ac7.png)
![Settings_Colors](https://github.com/unrealities/MTGA_Draft_17Lands/blob/main/assets/96687942/90c6b3df-0ade-4f32-a1be-b2ef40cedc32.png)

- **Read Draft Logs:** `File->Read Draft Log` からドラフトのログファイルを読み込みます。`DraftLog_<セット>_<ドラフトタイプ>_<ID>.log` という形式のファイルを選択してください。
- **Export Draft Data:** `File->Export Draft Data` から、現在のドラフトの全履歴（見たすべてのパックとピック内容）を CSV または JSON でエクスポートします。
- **Download Set Data:** `Data->Download Dataset` からセットデータをダウンロードします。セット情報を入力して ADD SET ボタンを押してください。
  - ダウンロードには数分かかる場合があります。
- **List Taken Cards:** `Cards->Taken Cards` から、ドラフト中に取得したカードの一覧を表示します。
- **List Suggested Decks:** `Cards->Suggest Decks` から、取得したカードを使ってアプリケーションが作成した40枚のデッキ提案を表示します。
- **Card Compare:** `Cards->Compare Cards` からカードを比較できます。P1P1 の比較に便利です。

## 追加機能

- **ホットキー:** `CTRL+G` でメインウィンドウの最小化/最大化を切り替えられます（Windowsのみ）。管理者権限が必要です。
- **ティアリスト:** 17Lands API からティアリストを直接追加できます。`Data > Download Tier List` を使用してください。
- **カードツールチップ:** カードの行をクリックすると、カード画像と 17Lands データを表示するツールチップが現れます。

## 設定

- **Columns 2-7:** パックテーブルなどの 2〜7 列目に表示する項目を設定します。
- **Deck Filter Format:** デッキフィルタの表示形式を、色の組み合わせ（UB, BG など）か、ギルド/ラヴニカ名（Dimir, Golgari など）に切り替えます。
- **Win Rate Format:** 勝率の表示形式を、パーセンテージ、5段階評価、またはグレード（A+〜F）に切り替えます。
- **Enable Bayesian Average:** すべての勝率フィールドにベイズ平均を適用します。
  - **2023年9月現在、17Landsが500サンプル未満のカードの勝率データを提供しなくなったため、この機能は動作しません。**
- **UI Size:** テキストと画像のサイズを変更します。
- **Enable P1P1 OCR:** [P1P1の解決策](#p1p1の解決策) を有効にします。

## ファイルの場所

### 設定ファイル (`config.json`)

以下の順序で検索されます：
1. **実行フォルダ:** アプリケーションと同じフォルダにある場合、それが優先されます（ポータブルモード）。
2. **システムユーザーフォルダ:**
    - **Windows:** `%APPDATA%\MTGA_Draft_Tool\config.json`
    - **Mac:** `~/Library/Application Support/MTGA_Draft_Tool/config.json`
    - **Linux:** `~/.config/MTGA_Draft_Tool/config.json`

### データセット
ダウンロードされたデータは、実行ファイルと同じディレクトリにある `Sets` フォルダに保存されます。

### ログ
デバッグログは `Debug` フォルダ、ドラフトログは `Logs` フォルダに保存されます。

## カードロジック

- **勝率グレード:** 全カードの勝率の平均と標準偏差を算出し、平均からどれだけ離れているかに基づいて A+ から F までのグレードを割り当てます。
- **勝率レーティング:** -1.67 から 2.00 標準偏差の範囲を 0.0 から 5.0 のスケールにマッピングして算出します。
- **ベイズ平均 (Bayesian Average):** サンプルサイズが小さい場合に、事前の仮定（40-60% の範囲、平均 50% など）と観測データを組み合わせてより信頼性の高い推定値を出します。サンプル数が200に近づくにつれて観測データの影響が強くなります。
- **自動最高評価 (Auto Highest Rating):** `Auto` フィルタが設定されており、16枚以上ピックしている場合、取得カードから有力な色の組み合わせを判定します。

## P1P1の解決策

### 問題点
MTG Arena のログには、ドラフトの最初のパック (P1P1) のデータが含まれていないため、通常は表示できません。

### 解決策
**`Enable P1P1 OCR` 設定で有効化されます（デフォルトで有効）。**
1. `Refresh` ボタンを押すとスクリーンショットが撮られます。
2. 画像は Google Cloud Function (GCF) に送られます。
3. Google Vision API を使用して OCR (文字認識) を行います。
4. 認識されたテキストとカード名のリストを比較し、一致するカードを表示します。

## ティアリスト (API提供型)
17Lands のティアリストをダウンロードして、ドラフト中に表示できます。ブラウザ拡張機能は不要です。

## シグナル検出 (ベータ)
渡されてきたカードを分析して、「空いている色」を特定しようとします。
- **仕組み:** パック1とパック3で、各カードの質 (GIHWR) と、それが通常取られる順手 (ATA) よりどれだけ遅く流れてきているかに基づいて「シグナルスコア」を計算します。
- **スコアの意味:** スコアが高いほど、その色が流れてきていることを示します（20点以上なら非常に空いています）。

## データセット通知
データセットが不足している場合や更新がある場合に通知されます。

---

## トラブルシューティング

- **ピック済みカードウィンドウにカードが足りない:** Arenaを再起動するとログが新しくなるため、再起動前のデータは追跡できません。
- **テーブルの勝率が 0% や NA になる:** 17Landsの仕様により、サンプル数が 500 未満のカードのデータは表示されません。
- **CTRL+G が効かない:** Windows では管理者権限で実行してください。Mac では利用できません。
- **SSLエラー (MacOS):** `/Applications/Python 3.12/Install Certificates.command` を実行してください。

## Arenaログの問題
Arenaのアップデートによりログ形式が変わることがあります。問題が発生した場合は、`File > Open Player.log` からログを確認し、報告をお願いします。
