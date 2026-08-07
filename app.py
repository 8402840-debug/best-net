import sys
import os
import traceback
import webview


def resource_path(relative_path):
    """兼容开发环境和 PyInstaller 打包后的路径"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def app_dir():
    """exe 所在目录（用于写日志），而不是临时解压目录"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


class Api:
    """暴露给前端 JS 调用的原生文件操作接口。
    浏览器里的 <a download> / <input type=file> 在 pywebview 窗口里
    经常不触发真正的系统文件对话框，所以改用 pywebview 自带的
    create_file_dialog，保证"导出备份/导入备份"点了真的有反应。"""

    def __init__(self):
        self.window = None

    def export_backup(self, json_str):
        try:
            default_dir = os.path.expanduser("~/Desktop")
            if not os.path.isdir(default_dir):
                default_dir = os.path.expanduser("~")
            result = self.window.create_file_dialog(
                webview.SAVE_DIALOG,
                directory=default_dir,
                save_filename="card-vault-backup.json",
                file_types=("JSON 文件 (*.json)", "所有文件 (*.*)"),
            )
            if not result:
                return {"ok": False, "canceled": True}
            path = result if isinstance(result, str) else result[0]
            with open(path, "w", encoding="utf-8") as f:
                f.write(json_str)
            return {"ok": True, "path": path}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def import_backup(self):
        try:
            result = self.window.create_file_dialog(
                webview.OPEN_DIALOG,
                file_types=("JSON 文件 (*.json)", "所有文件 (*.*)"),
            )
            if not result:
                return {"ok": False, "canceled": True}
            path = result[0]
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            return {"ok": True, "content": content}
        except Exception as e:
            return {"ok": False, "error": str(e)}


def main():
    html_file = resource_path("card-vault.html")
    api = Api()
    window = webview.create_window(
        "卡片保险柜",
        html_file,
        width=1060,
        height=840,
        resizable=True,
        min_size=(560, 500),
        js_api=api,
    )
    api.window = window
    # 显式指定 Windows 上的 GUI 后端，避免自动探测阶段卡住
    webview.start(gui="edgechromium", debug=False)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # --windowed 模式没有控制台，出错会静默卡住/闪退
        # 把异常写到 exe 同目录的日志文件，方便排查
        log_path = os.path.join(app_dir(), "card-vault-error.log")
        try:
            with open(log_path, "w", encoding="utf-8") as f:
                f.write(traceback.format_exc())
        except Exception:
            pass
        raise
