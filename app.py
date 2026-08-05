import sys
import os
import webview


def resource_path(relative_path):
    """兼容开发环境和 PyInstaller 打包后的路径"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def main():
    html_file = resource_path("card-vault.html")
    webview.create_window(
        "卡片保险柜",
        html_file,
        width=1040,
        height=820,
        resizable=True,
        min_size=(560, 500),
    )
    webview.start()


if __name__ == "__main__":
    main()
