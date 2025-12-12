"""电脑使用模块 - 服务器命令与密码管理（重新设计）"""
from __future__ import annotations

import re
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field


@dataclass
class CommandTab:
    """命令页签"""
    id: str
    name: str
    order: int = 0


@dataclass
class CommandBlock:
    """命令块：一组相关的命令"""
    id: str
    title: str
    description: str
    commands: List[str]
    tab_id: str = ""  # 所属页签ID，空表示未分类
    order: int = 0    # 排序
    tags: List[str] = field(default_factory=list)


@dataclass
class Credential:
    """凭证记录"""
    id: str
    service: str
    url: str
    account: str
    password: str
    extra: List[str] = field(default_factory=list)
    order: int = 0


class ComputerUsageService:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.commands_file = data_dir / "commands.json"
        self.credentials_file = data_dir / "credentials.json"
        self.tabs_file = data_dir / "command_tabs.json"
        self._ensure_files()

    def _ensure_files(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.commands_file.exists():
            self.commands_file.write_text("[]", encoding="utf-8")
        if not self.credentials_file.exists():
            self.credentials_file.write_text("[]", encoding="utf-8")
        if not self.tabs_file.exists():
            # 默认创建一个"未分类"页签
            default_tab = [{"id": "0", "name": "未分类", "order": 0}]
            self.tabs_file.write_text(json.dumps(default_tab, ensure_ascii=False, indent=2), encoding="utf-8")

    # ========== 页签管理 ==========
    def _load_tabs(self) -> List[CommandTab]:
        data = json.loads(self.tabs_file.read_text(encoding="utf-8"))
        return [CommandTab(**item) for item in data]

    def _save_tabs(self, tabs: List[CommandTab]):
        data = [asdict(t) for t in tabs]
        self.tabs_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def get_tabs(self) -> List[Dict]:
        tabs = self._load_tabs()
        return sorted([asdict(t) for t in tabs], key=lambda x: x['order'])

    def add_tab(self, name: str) -> Dict:
        tabs = self._load_tabs()
        new_id = str(max((int(t.id) for t in tabs), default=0) + 1)
        max_order = max((t.order for t in tabs), default=-1) + 1
        new_tab = CommandTab(id=new_id, name=name, order=max_order)
        tabs.append(new_tab)
        self._save_tabs(tabs)
        return asdict(new_tab)

    def update_tab(self, id: str, name: str) -> Optional[Dict]:
        tabs = self._load_tabs()
        for i, tab in enumerate(tabs):
            if tab.id == id:
                tabs[i] = CommandTab(id=id, name=name, order=tab.order)
                self._save_tabs(tabs)
                return asdict(tabs[i])
        return None

    def delete_tab(self, id: str) -> bool:
        if id == "0":  # 不能删除"未分类"
            return False
        tabs = self._load_tabs()
        new_tabs = [t for t in tabs if t.id != id]
        if len(new_tabs) < len(tabs):
            self._save_tabs(new_tabs)
            # 将该页签下的命令移到"未分类"
            cmds = self._load_commands()
            for cmd in cmds:
                if cmd.tab_id == id:
                    cmd.tab_id = "0"
            self._save_commands(cmds)
            return True
        return False

    def reorder_tabs(self, tab_ids: List[str]) -> bool:
        """重新排序页签"""
        tabs = self._load_tabs()
        tab_map = {t.id: t for t in tabs}
        for i, tid in enumerate(tab_ids):
            if tid in tab_map:
                tab_map[tid].order = i
        self._save_tabs(list(tab_map.values()))
        return True

    # ========== 命令块管理 ==========
    def _load_commands(self) -> List[CommandBlock]:
        data = json.loads(self.commands_file.read_text(encoding="utf-8"))
        # 兼容旧数据：添加缺失的字段
        for item in data:
            if 'tab_id' not in item:
                item['tab_id'] = "0"
            if 'order' not in item:
                item['order'] = 0
        return [CommandBlock(**item) for item in data]

    def _save_commands(self, commands: List[CommandBlock]):
        data = [asdict(c) for c in commands]
        self.commands_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def get_commands(self) -> List[Dict]:
        cmds = self._load_commands()
        return sorted([asdict(c) for c in cmds], key=lambda x: (x['tab_id'], x['order']))

    def get_commands_by_tab(self, tab_id: str) -> List[Dict]:
        cmds = self._load_commands()
        filtered = [asdict(c) for c in cmds if c.tab_id == tab_id]
        return sorted(filtered, key=lambda x: x['order'])

    def add_command(self, title: str, description: str, commands: List[str], tab_id: str = "0", tags: List[str] = None) -> Dict:
        all_cmds = self._load_commands()
        new_id = str(max((int(c.id) for c in all_cmds), default=0) + 1)
        # 计算该页签下的最大order
        tab_cmds = [c for c in all_cmds if c.tab_id == tab_id]
        max_order = max((c.order for c in tab_cmds), default=-1) + 1
        new_cmd = CommandBlock(id=new_id, title=title, description=description, commands=commands, tab_id=tab_id, order=max_order, tags=tags or [])
        all_cmds.append(new_cmd)
        self._save_commands(all_cmds)
        return asdict(new_cmd)

    def update_command(self, id: str, title: str, description: str, commands: List[str], tab_id: str = None, tags: List[str] = None) -> Optional[Dict]:
        all_cmds = self._load_commands()
        for i, cmd in enumerate(all_cmds):
            if cmd.id == id:
                new_tab_id = tab_id if tab_id is not None else cmd.tab_id
                all_cmds[i] = CommandBlock(id=id, title=title, description=description, commands=commands, tab_id=new_tab_id, order=cmd.order, tags=tags or [])
                self._save_commands(all_cmds)
                return asdict(all_cmds[i])
        return None

    def move_command_to_tab(self, cmd_id: str, target_tab_id: str) -> Optional[Dict]:
        """移动命令到指定页签"""
        all_cmds = self._load_commands()
        for cmd in all_cmds:
            if cmd.id == cmd_id:
                cmd.tab_id = target_tab_id
                # 放到目标页签的最后
                tab_cmds = [c for c in all_cmds if c.tab_id == target_tab_id and c.id != cmd_id]
                cmd.order = max((c.order for c in tab_cmds), default=-1) + 1
                self._save_commands(all_cmds)
                return asdict(cmd)
        return None

    def delete_command(self, id: str) -> bool:
        all_cmds = self._load_commands()
        new_cmds = [c for c in all_cmds if c.id != id]
        if len(new_cmds) < len(all_cmds):
            self._save_commands(new_cmds)
            return True
        return False

    def reorder_commands(self, tab_id: str, command_ids: List[str]) -> bool:
        """根据前端传入的ID顺序重排指定页签下的命令块"""
        all_cmds = self._load_commands()
        tab_cmds = [c for c in all_cmds if c.tab_id == tab_id]
        cmd_map = {c.id: c for c in tab_cmds}

        for order, cid in enumerate(command_ids):
            if cid in cmd_map:
                cmd_map[cid].order = order

        current_order = len(command_ids)
        for cmd in sorted(tab_cmds, key=lambda c: c.order):
            if cmd.id not in command_ids:
                cmd.order = current_order
                current_order += 1

        self._save_commands(all_cmds)
        return True

    def import_commands_txt(self, text: str) -> Dict:
        """从原始txt格式批量导入命令块"""
        blocks = []
        current_title = ""
        current_desc = ""
        current_cmds = []

        lines = text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # 跳过空行
            if not line:
                if current_title and current_cmds:
                    blocks.append({"title": current_title, "description": current_desc, "commands": current_cmds})
                    current_title = ""
                    current_desc = ""
                    current_cmds = []
                i += 1
                continue

            # 识别标题行（以冒号结尾或以#开头的注释）
            if line.endswith((':', '：')) and not line.startswith('#'):
                if current_title and current_cmds:
                    blocks.append({"title": current_title, "description": current_desc, "commands": current_cmds})
                current_title = line.rstrip(':：').strip()
                current_desc = ""
                current_cmds = []
            elif line.startswith('#'):
                comment = line.lstrip('# ').strip()
                if not current_title:
                    current_title = comment
                else:
                    current_desc = (current_desc + " " + comment).strip() if current_desc else comment
            else:
                current_cmds.append(line)

            i += 1

        # 最后一个块
        if current_title and current_cmds:
            blocks.append({"title": current_title, "description": current_desc, "commands": current_cmds})

        # 保存
        imported = 0
        for block in blocks:
            self.add_command(block["title"], block["description"], block["commands"])
            imported += 1

        return {"imported": imported, "blocks": blocks}

    # ========== 凭证管理 ==========
    def _load_credentials(self) -> List[Credential]:
        data = json.loads(self.credentials_file.read_text(encoding="utf-8"))
        for idx, item in enumerate(data):
            # 兼容旧数据：补齐排序字段
            if "order" not in item:
                item["order"] = idx
        return [Credential(**item) for item in data]

    def _save_credentials(self, credentials: List[Credential]):
        data = [asdict(c) for c in credentials]
        self.credentials_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def get_credentials(self) -> List[Dict]:
        creds = self._load_credentials()
        return sorted([asdict(c) for c in creds], key=lambda x: x["order"])

    def add_credential(self, service: str, url: str, account: str, password: str, extra: List[str] = None) -> Dict:
        all_creds = self._load_credentials()
        new_id = str(max((int(c.id) for c in all_creds), default=0) + 1)
        max_order = max((c.order for c in all_creds), default=-1) + 1
        new_cred = Credential(
            id=new_id,
            service=service,
            url=url,
            account=account,
            password=password,
            extra=extra or [],
            order=max_order,
        )
        all_creds.append(new_cred)
        self._save_credentials(all_creds)
        return asdict(new_cred)

    def update_credential(self, id: str, service: str, url: str, account: str, password: str, extra: List[str] = None) -> Optional[Dict]:
        all_creds = self._load_credentials()
        for i, cred in enumerate(all_creds):
            if cred.id == id:
                all_creds[i] = Credential(
                    id=id,
                    service=service,
                    url=url,
                    account=account,
                    password=password,
                    extra=extra or [],
                    order=cred.order,
                )
                self._save_credentials(all_creds)
                return asdict(all_creds[i])
        return None

    def delete_credential(self, id: str) -> bool:
        all_creds = self._load_credentials()
        new_creds = [c for c in all_creds if c.id != id]
        if len(new_creds) < len(all_creds):
            self._save_credentials(new_creds)
            return True
        return False

    def import_credentials_txt(self, text: str) -> Dict:
        """从原始txt格式批量导入凭证

        支持格式：
        1. 服务名 URL || 账号 || 密码
        2. 多行格式：
           服务名
           账号：xxx
           密码：xxx
        """
        credentials = []
        blocks = self._split_blocks(text)

        for block in blocks:
            cred = self._parse_credential_block(block)
            if cred:
                credentials.append(cred)

        # 保存
        imported = 0
        for cred in credentials:
            self.add_credential(cred["service"], cred["url"], cred["account"], cred["password"], cred.get("extra", []))
            imported += 1

        return {"imported": imported, "credentials": credentials}

    def reorder_credentials(self, credential_ids: List[str]) -> bool:
        """根据前端传入的ID顺序重排"""
        creds = self._load_credentials()
        cred_map = {c.id: c for c in creds}

        # 先按传入顺序设置排序值
        for order, cid in enumerate(credential_ids):
            if cid in cred_map:
                cred_map[cid].order = order

        # 未出现在列表中的旧数据继续排在后面，保持原相对顺序
        current_order = len(credential_ids)
        for cred in sorted(cred_map.values(), key=lambda c: c.order):
            if cred.id not in credential_ids:
                cred.order = current_order
                current_order += 1

        self._save_credentials(list(cred_map.values()))
        return True

    def _split_blocks(self, text: str) -> List[List[str]]:
        """按空行切分文本块"""
        blocks = []
        buf = []
        for line in text.splitlines():
            if line.strip():
                buf.append(line.rstrip())
            else:
                if buf:
                    blocks.append(buf)
                    buf = []
        if buf:
            blocks.append(buf)
        return blocks

    def _parse_credential_block(self, lines: List[str]) -> Optional[Dict]:
        """解析单个凭证块"""
        if not lines:
            return None

        merged = " ".join(lines)

        # 格式1: 服务名 URL || 账号 || 密码 || 备注
        if "||" in merged:
            parts = [p.strip() for p in merged.split("||")]
            service_url = parts[0] if parts else ""

            # 分离服务名和URL
            url_match = re.search(r'(https?://\S+)', service_url)
            if url_match:
                url = url_match.group(1)
                service = service_url.replace(url, "").strip()
            else:
                url = ""
                service = service_url

            return {
                "service": service.strip(". "),
                "url": url,
                "account": parts[1].strip() if len(parts) > 1 else "",
                "password": parts[2].strip() if len(parts) > 2 else "",
                "extra": [p.strip() for p in parts[3:] if p.strip()] if len(parts) > 3 else []
            }

        # 格式2: 多行格式
        service = re.sub(r'[：:]\s*$', '', lines[0]).strip()
        url = ""
        account = ""
        password = ""
        extra = []

        # 提取URL
        url_match = re.search(r'(https?://\S+)', service)
        if url_match:
            url = url_match.group(1)
            service = service.replace(url, "").strip()

        for line in lines[1:]:
            line_lower = line.lower()

            # 识别账号
            m = re.match(r'(账号|loginname|username|用户名?)[:：]\s*(.+)', line, re.I)
            if m:
                account = m.group(2).strip()
                continue

            # 识别密码
            m = re.match(r'(密码|password|pwd)[:：]\s*(.+)', line, re.I)
            if m:
                password = m.group(2).strip()
                continue

            # 识别URL
            url_match = re.search(r'(https?://\S+)', line)
            if url_match and not url:
                url = url_match.group(1)
                continue

            # 其他作为附加信息
            if line.strip():
                # 如果还没有账号密码，按顺序填充
                if not account:
                    account = line.strip()
                elif not password:
                    password = line.strip()
                else:
                    extra.append(line.strip())

        if not service:
            return None

        return {
            "service": service,
            "url": url,
            "account": account,
            "password": password,
            "extra": extra
        }
