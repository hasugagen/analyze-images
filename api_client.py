import os
import logging
import datetime
from typing import Dict, Any, Optional
import requests
import mysql.connector
from dotenv import load_dotenv
from contextlib import contextmanager

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# .envファイルから環境変数をロード
load_dotenv()

class ImageAnalysisConfig:
    """設定管理クラス"""
    API_URL = "http://localhost:8000/"
    
    @classmethod
    def get_mysql_config(cls) -> Dict[str, Any]:
        """MySQLの設定を安全に取得"""
        required_keys = ['MYSQL_HOST', 'MYSQL_PORT', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE']
        config = {}
        
        for key in required_keys:
            value = os.getenv(key)
            if not value and key != 'MYSQL_PORT':
                raise ValueError(f"環境変数 {key} が設定されていません。")
            
            config[key.lower().replace('mysql_', '')] = (
                int(value) if key == 'MYSQL_PORT' else value
            )
        
        return config

@contextmanager
def get_mysql_connection(config: Dict[str, Any]):
    """データベース接続のコンテキストマネージャー"""
    connection = None
    try:
        connection = mysql.connector.connect(**config)
        yield connection
    except mysql.connector.Error as e:
        logger.error(f"データベース接続エラー: {e}")
        raise
    finally:
        if connection:
            connection.close()

class ImageAnalyzer:
    def __init__(self, api_url: str, mysql_config: Dict[str, Any]):
        self.api_url = api_url
        self.mysql_config = mysql_config

    def insert_analysis_log(
        self, 
        connection, 
        image_path: str, 
        success: bool, 
        message: Optional[str] = None, 
        class_val: Optional[str] = None, 
        confidence: Optional[float] = None,
        request_timestamp: Optional[datetime.datetime] = None,
        response_timestamp: Optional[datetime.datetime] = None
    ) -> None:
        """分析結果をデータベースに安全に挿入"""
        try:
            with connection.cursor() as cursor:
                insert_query = """
                    INSERT INTO ai_analysis_log 
                    (image_path, success, message, class, confidence, request_timestamp, response_timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    image_path, success, message, class_val, 
                    confidence, request_timestamp, response_timestamp
                ))
                connection.commit()
                logger.info(f"ログを保存しました: {image_path}")
        except mysql.connector.Error as e:
            logger.error(f"ログ保存エラー: {e}")

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """画像分析とログ記録を行う"""
        request_timestamp = datetime.datetime.now()

        try:
            response = requests.post(self.api_url, json={"image_path": image_path}, timeout=10)
            response.raise_for_status()
            response_data = response.json()
            response_timestamp = datetime.datetime.now()

            with get_mysql_connection(self.mysql_config) as connection:
                self.insert_analysis_log(
                    connection,
                    image_path,
                    response_data["success"],
                    response_data.get("message", ""),
                    response_data["estimated_data"].get("class"),
                    response_data["estimated_data"].get("confidence"),
                    request_timestamp,
                    response_timestamp
                )

            return response_data

        except requests.exceptions.RequestException as e:
            logger.error(f"APIリクエストエラー: {e}")
            with get_mysql_connection(self.mysql_config) as connection:
                self.insert_analysis_log(
                    connection,
                    image_path,
                    False,
                    f"APIリクエストエラー: {e}",
                )
            return {"success": False, "message": str(e), "estimated_data": {}}

def main():
    try:
        mysql_config = ImageAnalysisConfig.get_mysql_config()
        analyzer = ImageAnalyzer(ImageAnalysisConfig.API_URL, mysql_config)

        test_image_paths = [
            "/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test1.jpg",
            "/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test2.jpg",
            "/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test3.jpg",
            "/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test4.jpg",
            "/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test5.jpg",
        ]

        for image_path in test_image_paths:
            logger.info(f"画像パス: {image_path}")
            response = analyzer.analyze_image(image_path)
            
            if response["success"]:
                logger.info(f"分析成功: {response['estimated_data']}")
            else:
                logger.warning(f"分析失敗: {response['message']}")

    except Exception as e:
        logger.error(f"予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    main()
