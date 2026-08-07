import os
import sys
import shutil
import webbrowser


def resource_path(relative_path):
    """兼容开发环境和 PyInstaller 打包后的路径"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def stable_app_dir():
    """固定的数据/文件存放目录，不随每次打包解压的临时路径变化，
    保证浏览器本地存储(localStorage)每次都认成同一个"网站"，数据不会丢。"""
    home = os.path.expanduser("~")
    d = os.path.join(home, "CardVaultApp")
    os.makedirs(d, exist_ok=True)
    return d


def main():
    src = resource_path("card-vault.html")
    dst = os.path.join(stable_app_dir(), "card-vault.html")
    # 每次启动都用最新版本覆盖界面文件本身（不影响已保存的卡片数据，
    # 卡片数据存在浏览器本地存储里，跟这个文件内容是分开的）
    shutil.copyfile(src, dst)
    webbrowser.open("file://" + os.path.abspath(dst))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        log_dir = stable_app_dir()
        with open(os.path.join(log_dir, "card-vault-error.log"), "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        raise
