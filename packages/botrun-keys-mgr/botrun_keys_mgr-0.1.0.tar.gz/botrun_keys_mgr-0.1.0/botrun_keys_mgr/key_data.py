"""金鑰資料模組"""

from dataclasses import dataclass
from typing import Optional
import pandas as pd


@dataclass
class KeyData:
    """金鑰資料類別"""

    timestamp: str  # 時間戳記
    department: str  # 申請單位
    purpose: str  # 申請事由
    applicant_name: str  # 申請人姓名
    applicant_email: str  # 申請人 Email
    processor: str  # 處理 RD
    key_time: str  # 發 key 時間
    api_key: str  # Key
    note: Optional[str] = None  # 備註

    @classmethod
    def from_series(cls, series: pd.Series) -> "KeyData":
        """從 Pandas Series 建立 KeyData 物件"""
        return cls(
            timestamp=series.iloc[0],
            department=series.iloc[1],
            purpose=series.iloc[2],
            applicant_name=series.iloc[3],
            applicant_email=series.iloc[4],
            processor=series.iloc[5],
            key_time=series.iloc[6],
            api_key=series.iloc[7],
            note=series.iloc[8] if len(series) > 8 else None,
        )


class KeyDataManager:
    """金鑰資料管理類別"""

    def __init__(self, sheet_data: list[list]):
        """
        初始化金鑰資料管理器

        Args:
            sheet_data: 從試算表讀取的原始資料
        """
        # 將試算表資料轉換為 DataFrame
        self.df = pd.DataFrame(
            sheet_data[1:],
            columns=[
                "timestamp",
                "department",
                "purpose",
                "applicant_name",
                "applicant_email",
                "processor",
                "key_time",
                "api_key",
                "note",
            ],
        )

    def get_key_data(self, api_key: str) -> Optional[KeyData]:
        """
        根據 API Key 取得金鑰資料

        Args:
            api_key: API 金鑰

        Returns:
            KeyData 物件，如果找不到則回傳 None
        """
        # 找出符合的資料
        matches = self.df[self.df["api_key"] == api_key]
        if len(matches) == 0:
            return None

        # 回傳第一筆符合的資料
        return KeyData.from_series(matches.iloc[0])
