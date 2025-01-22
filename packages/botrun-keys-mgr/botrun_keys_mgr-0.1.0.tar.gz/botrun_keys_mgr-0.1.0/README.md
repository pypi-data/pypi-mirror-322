# botrun_keys_mgr

波特人 API 金鑰管理套件

## 概述

這是一個專門為波特人（botrun）用戶管理 API 金鑰申請和存取控制的 Python 套件。本套件整合了 Google 表單進行申請，並使用 Google 試算表進行金鑰管理。

## 前置需求

### Google Service Account 設定
1. 本套件需要使用 `create-vms@plant-hero.iam.gserviceaccount.com` service account 來存取 Google 試算表
2. 請確保您有此 service account 的金鑰檔案（JSON 格式）
3. 設定環境變數：
```bash
export GOOGLE_APPLICATION_CREDENTIALS="./keys/google_service_account_key.json"
```
注意：請將金鑰檔案放在專案的 `keys` 目錄下，並命名為 `google_service_account_key.json`

## 安裝方式

### 開發環境安裝

1. 確保您已安裝 Python 3.11+ 和 Poetry
2. Clone 此專案：
```bash
git clone [repository_url]
cd botrun_keys_mgr
```

3. 使用 Poetry 安裝依賴：
```bash
poetry install
```

### 一般安裝
```bash
pip install botrun-keys-mgr
```

## 使用方式

### 基本使用
```python
from botrun_keys_mgr import KeyManager

# 初始化金鑰管理器
key_manager = KeyManager()

# 查詢金鑰資訊
key_data = key_manager.get_key_info("your-api-key")

if key_data:
    print(f"申請單位：{key_data.department}")
    print(f"申請人：{key_data.applicant_name}")
    print(f"Email：{key_data.applicant_email}")
    print(f"申請事由：{key_data.purpose}")
    print(f"處理 RD：{key_data.processor}")
    print(f"發放時間：{key_data.key_time}")
    if key_data.note:
        print(f"備註：{key_data.note}")
else:
    print("找不到此金鑰資訊")
```

### KeyData 類別欄位
```python
from botrun_keys_mgr import KeyData

# KeyData 包含以下欄位：
key_data = KeyData(
    timestamp="2024/1/22 上午 8:55:54",  # 時間戳記
    department="申請單位",
    purpose="申請事由",
    applicant_name="申請人姓名",
    applicant_email="申請人Email",
    processor="處理RD",
    key_time="2024/1/22",  # 發 key 時間
    api_key="sk-xxxxxxxxxxxxxxxx",  # API Key
    note="備註（選填）"
)
```

## 開發與測試

### 執行主程式
1. 確保已正確設置 service account 金鑰：
   - 建立 `keys` 目錄
   - 將金鑰檔案放入 `keys/google_service_account_key.json`

2. 使用 Poetry 執行：
```bash
poetry run python -m botrun_keys_mgr
```

或在 VS Code 中：
1. 開啟命令選擇（F1 或 Cmd+Shift+P）
2. 選擇 "Run and Debug"
3. 選擇 "Python: Run Main Script"

主程式會：
- 連接到 Google Sheets API
- 讀取試算表內容
- 顯示讀取到的資料

### 執行測試
使用 Poetry 執行測試：
```bash
poetry run python -m unittest discover -s tests
```

或者在 VS Code 中：
1. 開啟命令選擇（F1 或 Cmd+Shift+P）
2. 選擇 "Testing: Focus on Python Test Explorer"
3. 點擊測試檔案旁的執行按鈕

## 功能特色

- 透過 Google 表單管理 API 金鑰申請
- 金鑰驗證與確認
- 追蹤使用者電子郵件和金鑰啟用時間
- 整合 Google 試算表作為資料儲存

## 申請流程

使用者可以透過以下流程申請 API 金鑰：

1. 透過[API 金鑰申請表單](https://docs.google.com/forms/d/1M8s6UDzkekVuEKzEATWAOkc-U0229QG0NV89QVMPTDQ/edit)提交申請
2. 填寫必要資訊：
   - 申請單位
   - 申請事由
   - 申請人姓名
   - 申請人電子郵件

## 金鑰管理

系統使用 [Google 試算表資料庫](https://docs.google.com/spreadsheets/d/1P4n8uaLljygnfcn_FUN7RMsfoI-wDFgqygq8dAfejBI/edit)追蹤和管理以下資訊：
- API 金鑰
- 關聯的電子郵件地址
- 金鑰啟用時間戳記

## 授權條款

[授權資訊待補充]