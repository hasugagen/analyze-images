# FastAPI を使用した API サーバーとクライアントのセットアップ

このプロジェクトでは、FastAPI を使用して構築された API サーバーと、それと通信するクライアントを提供します。データベースには MySQL を使用し、Docker Compose を利用して簡単にセットアップできます。

## 概要

*   **API サーバー:** `api_server.py` (FastAPI)
*   **API クライアント:** `api_client.py` (Python)
*   **データベース:** MySQL (Docker Compose 経由)

## 前提条件

*   Docker がインストールされていること
*   Docker Compose がインストールされていること
*   Python 3 がインストールされていること
*   pip がインストールされていること

## セットアップ手順

### 1. MySQL データベースの起動 (Docker Compose)

プロジェクトのルートディレクトリに移動し、以下のコマンドを実行して MySQL データベースを起動します。

```bash
docker-compose up -d
```

### 2. 必要な Python パッケージのインストール
以下のコマンドを実行して、FastAPI とその他の必要なパッケージをインストールします。

```bash
pip install fastapi uvicorn python-dotenv requests mysql-connector-python
```

### 3. API サーバーの起動

以下のコマンドを実行して、API サーバーを起動します。

```bash
uvicorn api_server:app --reload
```

### 4. API クライアントの起動

別のターミナルを開き、以下のコマンドを実行して API クライアントを起動します。

```bash
python api_client.py
```

### 5. API ドキュメントの確認 (OpenAPI)

API サーバーが起動したら、ブラウザで以下の URL にアクセスして、OpenAPI ドキュメントを確認できます。

```
http://127.0.0.1:8000/docs
```

### ６．停止

```bash
docker-compose down
```

## ファイル構成

* `docker-compose.yml`: MySQL データベースの定義
* `api_server.py`: FastAPI を使用した API サーバーのコード
* `api_client.py`: API サーバーと通信するクライアントのコード
* `README.md`: このドキュメント

