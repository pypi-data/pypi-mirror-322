"""主程式模組"""

from .key_manager import KeyManager


def main():
    """主程式入口點"""
    try:
        # 初始化金鑰管理器
        key_manager = KeyManager()

        # 測試讀取金鑰資訊
        test_keys = [
            "sk-abcd1678djklfojwj3iow",
            "invalid-key",
        ]

        print("測試金鑰查詢功能：")
        print("-" * 50)

        for key in test_keys:
            print(f"\n查詢金鑰：{key}")
            key_data = key_manager.get_key_info(key)

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

            print("-" * 50)

    except Exception as e:
        print(f"發生錯誤：{str(e)}")


if __name__ == "__main__":
    main()
