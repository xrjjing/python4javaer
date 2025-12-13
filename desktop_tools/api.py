"""PyWebView API - 暴露给前端的接口"""
import json
from pathlib import Path
from typing import List

from services import ComputerUsageService, NodeConverterService


class Api:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.computer_usage = ComputerUsageService(data_dir / "电脑使用")
        self.node_converter = NodeConverterService(data_dir / "转化节点")

    def __dir__(self):
        """限制暴露成员，避免 pywebview 深度遍历内部 Path 导致噪声日志"""
        return [name for name, val in self.__class__.__dict__.items() if callable(val)]

    # ========== 页签管理 ==========
    def get_tabs(self):
        return self.computer_usage.get_tabs()

    def add_tab(self, name: str):
        return self.computer_usage.add_tab(name)

    def update_tab(self, id: str, name: str):
        return self.computer_usage.update_tab(id, name)

    def delete_tab(self, id: str):
        return self.computer_usage.delete_tab(id)

    def reorder_tabs(self, tab_ids: List[str]):
        return self.computer_usage.reorder_tabs(tab_ids)

    # ========== 命令块管理 ==========
    def get_commands(self):
        return self.computer_usage.get_commands()

    def get_commands_by_tab(self, tab_id: str):
        return self.computer_usage.get_commands_by_tab(tab_id)

    def add_command(self, title: str, description: str, commands: List[str], tab_id: str = "0", tags: List[str] = None):
        return self.computer_usage.add_command(title, description, commands, tab_id, tags)

    def update_command(self, id: str, title: str, description: str, commands: List[str], tab_id: str = None, tags: List[str] = None):
        return self.computer_usage.update_command(id, title, description, commands, tab_id, tags)

    def move_command_to_tab(self, cmd_id: str, target_tab_id: str):
        return self.computer_usage.move_command_to_tab(cmd_id, target_tab_id)

    def delete_command(self, id: str):
        return self.computer_usage.delete_command(id)

    def reorder_commands(self, tab_id: str, command_ids: List[str]):
        return self.computer_usage.reorder_commands(tab_id, command_ids)

    def import_commands(self, text: str):
        return self.computer_usage.import_commands_txt(text)

    # ========== 凭证管理 ==========
    def get_credentials(self):
        return self.computer_usage.get_credentials()

    def add_credential(self, service: str, url: str, account: str, password: str, extra: List[str] = None):
        return self.computer_usage.add_credential(service, url, account, password, extra)

    def update_credential(self, id: str, service: str, url: str, account: str, password: str, extra: List[str] = None):
        return self.computer_usage.update_credential(id, service, url, account, password, extra)

    def delete_credential(self, id: str):
        return self.computer_usage.delete_credential(id)

    def import_credentials(self, text: str):
        return self.computer_usage.import_credentials_txt(text)

    def reorder_credentials(self, credential_ids: List[str]):
        return self.computer_usage.reorder_credentials(credential_ids)

    # ========== 节点转换 ==========
    def convert_links(self, links_text: str):
        return self.node_converter.convert_links(links_text)

    def fetch_subscription(self, url: str):
        return self.node_converter.fetch_subscription(url)

    # ========== 节点管理 ==========
    def get_nodes(self):
        return self.node_converter.get_nodes()

    def save_node(self, name: str, node_type: str, server: str, port: int, raw_link: str, yaml_config: str):
        return self.node_converter.save_node(name, node_type, server, port, raw_link, yaml_config)

    def delete_node(self, id: str):
        return self.node_converter.delete_node(id)

    # ========== 系统配置 ==========
    def get_theme(self):
        """获取保存的主题设置"""
        config_path = self.data_dir / "config.json"
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    return config.get("theme", "dark")
            except Exception:
                pass
        return "dark"

    def save_theme(self, theme: str):
        """保存主题设置"""
        config_path = self.data_dir / "config.json"
        config = {}
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
            except Exception:
                pass
        config["theme"] = theme
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    # ========== 数据备份与恢复 ==========
    def export_data(self):
        """导出所有数据为 JSON 格式"""
        from datetime import datetime

        data = {
            "version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "app": "狗狗百宝箱",
            "data": {
                "tabs": self.computer_usage.get_tabs(),
                "commands": self.computer_usage.get_commands(),
                "credentials": self.computer_usage.get_credentials(),
                "nodes": self.node_converter.get_nodes(),
                "theme": self.get_theme()
            }
        }
        return data

    def import_data(self, json_data: dict):
        """从 JSON 数据导入（覆盖现有数据）"""
        try:
            if not isinstance(json_data, dict) or "data" not in json_data:
                return {"success": False, "error": "无效的备份数据格式"}

            data = json_data["data"]
            imported = {"tabs": 0, "commands": 0, "credentials": 0, "nodes": 0}

            # 导入页签
            if "tabs" in data and isinstance(data["tabs"], list):
                tabs_file = self.computer_usage.tabs_file
                tabs_file.write_text(json.dumps(data["tabs"], ensure_ascii=False, indent=2), encoding="utf-8")
                imported["tabs"] = len(data["tabs"])

            # 导入命令
            if "commands" in data and isinstance(data["commands"], list):
                cmds_file = self.computer_usage.commands_file
                cmds_file.write_text(json.dumps(data["commands"], ensure_ascii=False, indent=2), encoding="utf-8")
                imported["commands"] = len(data["commands"])

            # 导入凭证
            if "credentials" in data and isinstance(data["credentials"], list):
                creds_file = self.computer_usage.credentials_file
                creds_file.write_text(json.dumps(data["credentials"], ensure_ascii=False, indent=2), encoding="utf-8")
                imported["credentials"] = len(data["credentials"])

            # 导入节点
            if "nodes" in data and isinstance(data["nodes"], list):
                nodes = data["nodes"]
                lines = ["# 代理节点", ""]
                for node in nodes:
                    lines.append(f"## {node.get('name', 'Unknown')}")
                    lines.append(f"- **ID**: {node.get('id', '')}")
                    lines.append(f"- **类型**: {node.get('type', '')}")
                    lines.append(f"- **服务器**: {node.get('server', '')}:{node.get('port', '')}")
                    lines.append(f"- **链接**: `{node.get('raw_link', '')}`")
                    config = node.get("config", {})
                    if config.get("yaml"):
                        lines.append(f"```yaml\n{config['yaml']}\n```")
                    lines.append("")
                self.node_converter.nodes_file.write_text("\n".join(lines), encoding="utf-8")
                imported["nodes"] = len(nodes)

            # 导入主题
            if "theme" in data:
                self.save_theme(data["theme"])

            return {"success": True, "imported": imported}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_data_stats(self):
        """获取数据统计信息"""
        return {
            "tabs": len(self.computer_usage.get_tabs()),
            "commands": len(self.computer_usage.get_commands()),
            "credentials": len(self.computer_usage.get_credentials()),
            "nodes": len(self.node_converter.get_nodes())
        }
