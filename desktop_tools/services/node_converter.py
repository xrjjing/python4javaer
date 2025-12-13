"""节点转换模块 - 订阅链接转换与节点管理"""
from __future__ import annotations

import base64
import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from urllib.parse import parse_qs, unquote, urlparse
import urllib.request
import ssl


@dataclass
class ProxyNode:
    id: str
    name: str
    type: str
    server: str
    port: int
    raw_link: str
    config: Dict


class NodeConverterService:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.nodes_file = data_dir / "nodes.md"
        self._ensure_files()

    def _ensure_files(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.nodes_file.exists():
            self.nodes_file.write_text("# 代理节点\n\n", encoding="utf-8")

    # ========== 链接解析 ==========
    @staticmethod
    def _add_padding(data: str) -> str:
        missing = len(data) % 4
        if missing:
            data += "=" * (4 - missing)
        return data

    def _parse_vless(self, parsed, idx: int) -> Optional[Dict]:
        query = parse_qs(parsed.query or "")
        q = lambda key, default="": query.get(key, [default])[0]

        if not parsed.hostname or not parsed.username or not parsed.port:
            return None

        reality_public_key = q("pbk", "")
        reality_short_id = q("sid", "")
        reality_opts = None
        if reality_public_key or reality_short_id:
            reality_opts = {"public-key": reality_public_key, "short-id": reality_short_id}

        return {
            "name": unquote(parsed.fragment) if parsed.fragment else f"vless-{idx}",
            "type": "vless",
            "server": parsed.hostname,
            "port": parsed.port,
            "uuid": unquote(parsed.username),
            "client-fingerprint": q("fp", "chrome"),
            "servername": q("sni", ""),
            "network": q("type", "tcp"),
            "reality-opts": reality_opts,
            "flow": q("flow", "") or None,
        }

    def _parse_hysteria2(self, parsed, idx: int) -> Optional[Dict]:
        query = parse_qs(parsed.query or "")
        q = lambda key, default="": query.get(key, [default])[0]

        if not parsed.hostname or not parsed.port:
            return None

        password = parsed.username or parsed.password or ""
        if not password:
            return None

        return {
            "name": unquote(parsed.fragment) if parsed.fragment else f"hysteria2-{idx}",
            "type": "hysteria2",
            "server": parsed.hostname,
            "port": parsed.port,
            "password": unquote(password),
            "sni": q("sni", ""),
        }

    def _parse_ss(self, parsed, idx: int) -> Optional[Dict]:
        fragment_name = unquote(parsed.fragment) if parsed.fragment else f"ss-{idx}"

        def build_from_netloc(netloc: str) -> Optional[Dict]:
            inner = urlparse(f"//{netloc}")
            if not inner.hostname or not inner.port:
                return None
            method = inner.username or ""
            password = inner.password
            if password is None:
                if ":" in method:
                    method, password = method.split(":", 1)
                else:
                    return None
            return {
                "name": fragment_name,
                "type": "ss",
                "server": inner.hostname,
                "port": inner.port,
                "cipher": method,
                "password": unquote(password),
            }

        if parsed.netloc:
            node = build_from_netloc(parsed.netloc)
            if node:
                return node

        encoded = (parsed.netloc + parsed.path).strip("/")
        if encoded:
            try:
                decoded = base64.urlsafe_b64decode(self._add_padding(encoded)).decode("utf-8")
                node = build_from_netloc(decoded)
                if node:
                    return node
            except Exception:
                pass
        return None

    def parse_link(self, link: str, idx: int = 0) -> Optional[Dict]:
        parsed = urlparse(link.strip())
        scheme = parsed.scheme.lower()
        if scheme == "vless":
            return self._parse_vless(parsed, idx)
        elif scheme == "hysteria2":
            return self._parse_hysteria2(parsed, idx)
        elif scheme == "ss":
            return self._parse_ss(parsed, idx)
        return None

    # ========== YAML渲染 ==========
    def _render_vless(self, node: Dict) -> List[str]:
        lines = [
            f"  - name: {node['name']}",
            "    type: vless",
            f"    server: {node['server']}",
            f"    port: {node['port']}",
            f"    uuid: {node['uuid']}",
            "    tls: true",
            f"    client-fingerprint: {node['client-fingerprint']}",
        ]
        if node.get("servername"):
            lines.append(f"    servername: {node['servername']}")
        lines.append(f"    network: {node['network']}")
        lines.append("    udp: true")
        if node.get("reality-opts"):
            lines.append("    reality-opts:")
            lines.append(f"      public-key: {node['reality-opts'].get('public-key', '')}")
            lines.append(f"      short-id: {node['reality-opts'].get('short-id', '')}")
        if node.get("flow"):
            lines.append(f"    flow: {node['flow']}")
        lines.append("    skip-cert-verify: false")
        return lines

    def _render_hysteria2(self, node: Dict) -> List[str]:
        lines = [
            f"  - name: {node['name']}",
            "    type: hysteria2",
            f"    server: {node['server']}",
            f"    port: {node['port']}",
            f"    password: {node['password']}",
        ]
        if node.get("sni"):
            lines.append(f"    sni: {node['sni']}")
        lines.append("    alpn: [h3]")
        lines.append("    skip-cert-verify: false")
        return lines

    def _render_ss(self, node: Dict) -> List[str]:
        return [
            f"  - name: {node['name']}",
            "    type: ss",
            f"    server: {node['server']}",
            f"    port: {node['port']}",
            f"    cipher: {node['cipher']}",
            f"    password: {node['password']}",
            "    udp: true",
        ]

    def render_yaml(self, nodes: List[Dict]) -> str:
        if not nodes:
            return "proxies: []\n"
        lines = ["proxies:"]
        for node in nodes:
            if node["type"] == "vless":
                lines.extend(self._render_vless(node))
            elif node["type"] == "hysteria2":
                lines.extend(self._render_hysteria2(node))
            elif node["type"] == "ss":
                lines.extend(self._render_ss(node))
        return "\n".join(lines) + "\n"

    # ========== 转换功能 ==========
    def convert_links(self, links_text: str) -> Dict:
        links = [l.strip() for l in links_text.splitlines() if l.strip()]
        nodes = []
        errors = []
        for idx, link in enumerate(links, 1):
            node = self.parse_link(link, idx)
            if node:
                nodes.append(node)
            else:
                errors.append(f"无法解析: {link[:50]}...")
        yaml_output = self.render_yaml(nodes)
        return {"nodes": nodes, "yaml": yaml_output, "errors": errors}

    def fetch_subscription(self, url: str) -> Dict:
        def maybe_decode_subscription_content(text: str) -> str:
            """尝试将订阅内容进行 base64 解码（兼容 urlsafe），失败则原样返回。"""
            raw = (text or "").strip()
            if not raw:
                return ""

            # 已经是明文节点列表/含协议的内容，不做 base64 解码
            if "://" in raw or "\n" in raw or "\r" in raw:
                return text

            # 仅当看起来像 base64 时才尝试解码，避免误判导致“乱码但能解码”的情况
            if not re.fullmatch(r"[A-Za-z0-9+/=_-]+", raw):
                return text

            for decoder in (base64.urlsafe_b64decode, base64.b64decode):
                try:
                    decoded_bytes = decoder(self._add_padding(raw))
                    decoded = decoded_bytes.decode("utf-8")
                except Exception:
                    continue
                # 简单校验：解码后至少应像“多行”或含协议
                if "://" in decoded or "\n" in decoded or "\r" in decoded:
                    return decoded

            return text

        url = (url or "").strip()
        if not url:
            return {"nodes": [], "yaml": "", "errors": ["订阅链接不能为空"]}

        # 支持直接粘贴节点链接/节点列表到“订阅链接”输入框，避免 urlopen 报错：
        # <urlopen error unknown url type: vless>
        if "\n" in url or "\r" in url:
            return self.convert_links(url)

        parsed = urlparse(url)
        if parsed.scheme and parsed.scheme not in ("http", "https"):
            return self.convert_links(url)

        # 无 scheme：不视为可拉取 URL，尝试按“订阅内容/节点内容”处理（兼容粘贴 base64 内容）
        if not parsed.scheme:
            content = maybe_decode_subscription_content(url)
            return self.convert_links(content)

        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            req = urllib.request.Request(url, headers={"User-Agent": "ClashForAndroid/2.5.12"})
            with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
                content = resp.read().decode("utf-8", errors="replace")
            content = maybe_decode_subscription_content(content)
            return self.convert_links(content)
        except Exception as e:
            return {"nodes": [], "yaml": "", "errors": [str(e)]}

    # ========== 节点管理 ==========
    def _parse_nodes_md(self) -> List[ProxyNode]:
        content = self.nodes_file.read_text(encoding="utf-8")
        nodes = []
        current_node = None
        in_yaml = False
        yaml_lines = []

        for line in content.splitlines():
            if line.startswith("## "):
                if current_node and yaml_lines:
                    current_node.config = {"yaml": "\n".join(yaml_lines)}
                    nodes.append(current_node)
                name = line[3:].strip()
                node_id = str(len(nodes))
                current_node = ProxyNode(id=node_id, name=name, type="", server="", port=0, raw_link="", config={})
                yaml_lines = []
                in_yaml = False
            elif line.startswith("- **链接**:"):
                if current_node:
                    current_node.raw_link = line.split(":", 1)[1].strip().strip("`")
            elif line.startswith("- **类型**:"):
                if current_node:
                    current_node.type = line.split(":", 1)[1].strip()
            elif line.startswith("- **服务器**:"):
                if current_node:
                    current_node.server = line.split(":", 1)[1].strip()
            elif line.startswith("- **端口**:"):
                if current_node:
                    try:
                        current_node.port = int(line.split(":", 1)[1].strip())
                    except ValueError:
                        pass
            elif line.strip() == "```yaml":
                in_yaml = True
            elif line.strip() == "```" and in_yaml:
                in_yaml = False
            elif in_yaml:
                yaml_lines.append(line)

        if current_node:
            if yaml_lines:
                current_node.config = {"yaml": "\n".join(yaml_lines)}
            nodes.append(current_node)

        return nodes

    def _save_nodes_md(self, nodes: List[ProxyNode]):
        lines = ["# 代理节点", ""]
        for node in nodes:
            lines.append(f"## {node.name}")
            lines.append("")
            lines.append(f"- **类型**: {node.type}")
            lines.append(f"- **服务器**: {node.server}")
            lines.append(f"- **端口**: {node.port}")
            if node.raw_link:
                lines.append(f"- **链接**: `{node.raw_link}`")
            if node.config.get("yaml"):
                lines.append("")
                lines.append("```yaml")
                lines.append(node.config["yaml"])
                lines.append("```")
            lines.append("")
        self.nodes_file.write_text("\n".join(lines), encoding="utf-8")

    def get_nodes(self) -> List[Dict]:
        return [asdict(n) for n in self._parse_nodes_md()]

    def save_node(self, name: str, node_type: str, server: str, port: int, raw_link: str, yaml_config: str) -> Dict:
        all_nodes = self._parse_nodes_md()
        new_id = str(max((int(n.id) for n in all_nodes), default=-1) + 1)
        new_node = ProxyNode(
            id=new_id, name=name, type=node_type, server=server,
            port=port, raw_link=raw_link, config={"yaml": yaml_config}
        )
        all_nodes.append(new_node)
        self._save_nodes_md(all_nodes)
        return asdict(new_node)

    def delete_node(self, id: str) -> bool:
        all_nodes = self._parse_nodes_md()
        new_nodes = [n for n in all_nodes if n.id != id]
        if len(new_nodes) < len(all_nodes):
            self._save_nodes_md(new_nodes)
            return True
        return False
