# デッキ評価機能の実装メモ

## 実装日
2026-02-12

## 概要
完成したドラフトデッキとサイドボードのカード評価を表示する機能の実装

---

## ✅ 完了した作業

### 1. バックエンド実装

#### `src/card_logic.py`
- **`parse_arena_export(text)` 関数を追加**
  - Arena の「Export」形式のデッキリストを解析
  - デッキとサイドボードのカード名リストを返す
  - 正規表現でカード枚数と名前を抽出

#### `src/log_scanner.py`
- **`ArenaScanner` クラスに以下を追加:**
  - `self.deck = []` - メインデッキのストレージ
  - `self.sideboard = []` - サイドボードのストレージ（既存を活用）
  - `retrieve_deck_cards()` メソッド - デッキカードデータの取得
  - `retrieve_sideboard_cards()` メソッド - サイドボードカードデータの取得
- **`clear_draft()` メソッドを更新**
  - `self.deck` のクリア処理を追加

#### `src/constants.py`
- **デッキ検出用の定数を追加:**
  - `DRAFT_GET_PACK_STRING_QUICK` - Quick Draft のパック取得文字列
  - `DECK_GET_DETAILS_STRING` - デッキ詳細取得文字列

#### `src/overlay.py`
- **インポートを追加:**
  - `parse_arena_export` を `src.card_logic` からインポート

---

## ❌ 未完了の作業

### 1. UI実装（`src/overlay.py`）

#### 必要な実装:

1. **メニュー項目の追加**
   ```python
   # Cards メニューに以下を追加
   self.cardmenu.add_command(label="Deck Evaluation", command=self.__open_deck_evaluation_window)
   ```

2. **ウィンドウ作成メソッド**
   - `__open_deck_evaluation_window(self)` メソッドの実装
   - 2つのテーブル（Treeview）を作成:
     - メインデッキ用
     - サイドボード用
   - 表示カラム: Name, Count, Color, Cost, Type, GIHWR, Grade など
   - "Paste from Arena" ボタンの実装

3. **テーブル更新メソッド**
   - `__update_deck_evaluation_table(self)` メソッドの実装
   - `self.draft.retrieve_deck_cards()` からデータ取得
   - `self.draft.retrieve_sideboard_cards()` からデータ取得
   - `stack_cards()` でカード枚数を集計
   - `CardResult` で評価データを処理

4. **"Paste from Arena" 機能**
   - クリップボードからデッキリストを取得
   - `parse_arena_export()` で解析
   - `self.draft.deck` と `self.draft.sideboard` に保存
   - テーブルを更新

5. **ウィンドウクローズ処理**
   - `__close_deck_evaluation_window(self, popup)` メソッドの実装
   - テーブル参照のクリア

### 2. 自動デッキ検出（オプション）

現在は手動で "Paste from Arena" を使用する想定。将来的には:
- ログファイルから自動的にデッキを検出
- `DECK_GET_DETAILS_STRING` を使用してデッキ更新を検出
- ドラフト完了時に自動的にデッキを取得

---

## 📝 実装の参考

既存の類似機能:
- **Taken Cards ウィンドウ** (`__open_taken_cards_window`)
  - テーブル作成とフィルタリングの参考
- **Suggest Decks ウィンドウ** (`__open_suggest_deck_window`)
  - デッキ表示とカード評価の参考

---

## 🔧 技術的な問題

### 発生した問題:
- `overlay.py` で `grep_search` と `replace_file_content` ツールが文字列マッチングに失敗
- ファイルのエンコーディング（CRLF改行コード）が原因と推測
- PowerShell スクリプトを使用して回避

### 解決策:
- 一時的な PowerShell スクリプト (`update_log_scanner.ps1`) を作成
- 直接ファイル操作で変更を適用

---

## 次のステップ

1. `overlay.py` の UI 実装を完了
2. 手動テストでデッキ評価機能を検証
3. 必要に応じて自動デッキ検出機能を追加
4. ユニットテストの追加（`tests/test_deck_parsing.py`）
5. プルリクエストを作成してレビュー依頼
