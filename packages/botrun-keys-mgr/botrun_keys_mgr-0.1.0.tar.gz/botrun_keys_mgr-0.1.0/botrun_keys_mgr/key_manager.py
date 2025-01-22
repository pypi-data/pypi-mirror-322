"""金鑰管理模組"""

from typing import Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from .key_data import KeyData, KeyDataManager


class KeyManager:
    """金鑰管理類別"""

    def __init__(self):
        """初始化金鑰管理器"""
        self.sheet_id = "1P4n8uaLljygnfcn_FUN7RMsfoI-wDFgqygq8dAfejBI"
        self._data_manager = None

    def _init_sheets_service(self):
        """初始化 Google Sheets 服務"""
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
        credentials = service_account.Credentials.from_service_account_file(
            "keys/google_service_account_key.json", scopes=SCOPES
        )
        service = build("sheets", "v4", credentials=credentials)
        return service.spreadsheets()

    def _load_data(self):
        """載入試算表資料"""
        if self._data_manager is None:
            sheet = self._init_sheets_service()
            result = (
                sheet.values()
                .get(spreadsheetId=self.sheet_id, range="A1:I1000")  # 讀取足夠多的行數
                .execute()
            )
            self._data_manager = KeyDataManager(result.get("values", []))

    def get_key_info(self, api_key: str) -> Optional[KeyData]:
        """
        根據 API Key 取得金鑰資訊

        Args:
            api_key: API 金鑰

        Returns:
            KeyData 物件，如果找不到則回傳 None
        """
        self._load_data()
        return self._data_manager.get_key_data(api_key)
