"""
日志侦探服务测试

测试覆盖：
1. 正常日志分析
2. MAX_LOG_LINES/MAX_LOG_SIZE 截断
3. max_results 参数生效
4. 恶意/超长日志处理
"""
import pytest
from fastapi.testclient import TestClient
from log_detective_service.app.main import app
from log_detective_service.app.config import settings

client = TestClient(app)


class TestLogDetectiveService:
    """日志侦探服务测试套件"""

    def test_health_check(self):
        """测试健康检查接口"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_analyze_normal_nginx_log(self):
        """测试正常 Nginx 日志分析"""
        log_text = """192.168.1.10 - - [27/Oct/2023:10:00:01 +0000] "GET /api/users HTTP/1.1" 200 1234
192.168.1.10 - - [27/Oct/2023:10:00:02 +0000] "POST /api/login HTTP/1.1" 500 567
192.168.1.20 - - [27/Oct/2023:10:00:03 +0000] "GET /api/orders HTTP/1.1" 200 890
192.168.1.10 - - [27/Oct/2023:10:00:04 +0000] "GET /api/profile HTTP/1.1" 404 123""".strip()

        response = client.post(
            "/internal/log-detective/analyze",
            json={
                "log_text": log_text,
                "profile": "nginx_access",
                "max_results": 100
            }
        )

        assert response.status_code == 200
        data = response.json()

        # 验证基础统计
        assert data["summary"]["total_lines"] == 4
        assert "suspicious_ips" in data
        assert "critical_errors" in data
        assert "meta" in data

    def test_analyze_python_app_log_with_errors(self):
        """测试包含错误的 Python 应用日志"""
        log_text = """2023-10-27 10:00:01 [INFO] Service started
2023-10-27 10:05:23 [WARN] High memory usage from 192.168.1.10
2023-10-27 10:06:01 [ERROR] Database connection failed
2023-10-27 10:07:12 [ERROR] Login failed from 203.0.113.42
2023-10-27 10:08:30 [CRITICAL] System crash imminent
2023-10-27 10:09:00 [INFO] Recovery initiated""".strip()

        response = client.post(
            "/internal/log-detective/analyze",
            json={
                "log_text": log_text,
                "profile": "python_app",
                "max_results": 10
            }
        )

        assert response.status_code == 200
        data = response.json()

        # 验证错误统计
        assert data["summary"]["total_lines"] == 6
        assert data["summary"]["error_lines"] >= 2  # 至少2个ERROR
        assert data["summary"]["warn_lines"] >= 1   # 至少1个WARN

        # 验证可疑 IP 提取
        assert len(data["suspicious_ips"]) > 0
        ip_list = [ip["ip"] for ip in data["suspicious_ips"]]
        assert "192.168.1.10" in ip_list or "203.0.113.42" in ip_list

        # 验证关键错误记录
        assert len(data["critical_errors"]) > 0
        error_levels = [err["level"] for err in data["critical_errors"]]
        assert "ERROR" in error_levels or "CRITICAL" in error_levels

    def test_max_log_lines_truncation(self):
        """测试 MAX_LOG_LINES 截断功能"""
        # 生成超过限制的日志行数
        lines_count = settings.MAX_LOG_LINES + 1000
        log_text = "\n".join([f"2023-10-27 10:00:{i%60:02d} [INFO] Line {i}" for i in range(lines_count)])

        response = client.post(
            "/internal/log-detective/analyze",
            json={
                "log_text": log_text,
                "profile": "generic",
                "max_results": 10
            }
        )

        assert response.status_code == 200
        data = response.json()

        # 验证截断生效
        assert data["summary"]["total_lines"] == settings.MAX_LOG_LINES
        assert data["meta"]["truncated"] is True

    def test_max_log_size_truncation(self):
        """测试 MAX_LOG_SIZE 截断功能"""
        # 生成接近大小限制的日志（确保不超过 Pydantic 验证限制）
        line = "A" * 500  # 500字节每行
        lines_count = (settings.MAX_LOG_SIZE // 500) - 100  # 留出足够余量
        log_text = "\n".join([f"{line} ERROR" for _ in range(lines_count)])

        response = client.post(
            "/internal/log-detective/analyze",
            json={
                "log_text": log_text,
                "profile": "generic",
                "max_results": 10
            }
        )

        assert response.status_code == 200
        data = response.json()

        # 验证大日志被正常处理
        assert data["summary"]["total_lines"] > 1000
        assert data["summary"]["error_lines"] > 0

    def test_max_results_parameter(self):
        """测试 max_results 参数生效"""
        # 生成包含多个错误的日志
        log_text = "\n".join([f"2023-10-27 10:00:{i%60:02d} [ERROR] Error {i}" for i in range(50)])

        response = client.post(
            "/internal/log-detective/analyze",
            json={
                "log_text": log_text,
                "profile": "generic",
                "max_results": 5
            }
        )

        assert response.status_code == 200
        data = response.json()

        # 验证返回的关键错误数量不超过 max_results
        assert len(data["critical_errors"]) <= 5

    def test_empty_log_text(self):
        """测试空日志文本"""
        response = client.post(
            "/internal/log-detective/analyze",
            json={
                "log_text": " ",  # 单个空格（满足 min_length=1）
                "profile": "generic",
                "max_results": 10
            }
        )

        assert response.status_code == 200
        data = response.json()

        # 空日志应该返回零统计
        assert data["summary"]["total_lines"] == 1
        assert data["summary"]["error_lines"] == 0
        assert data["summary"]["warn_lines"] == 0

    def test_malicious_log_with_special_characters(self):
        """测试包含特殊字符的恶意日志"""
        log_text = """2023-10-27 10:00:01 [ERROR] <script>alert('xss')</script>
2023-10-27 10:00:02 [ERROR] '; DROP TABLE users; --
2023-10-27 10:00:03 [ERROR] ../../../etc/passwd
"""
        response = client.post(
            "/internal/log-detective/analyze",
            json={
                "log_text": log_text,
                "profile": "generic",
                "max_results": 10
            }
        )

        assert response.status_code == 200
        data = response.json()

        # 服务应该正常处理，不崩溃
        assert data["summary"]["error_lines"] == 3
        assert len(data["critical_errors"]) > 0

    def test_invalid_profile(self):
        """测试无效的 profile 参数"""
        response = client.post(
            "/internal/log-detective/analyze",
            json={
                "log_text": "test log",
                "profile": "invalid_profile",  # 无效值
                "max_results": 10
            }
        )

        # Pydantic 验证应该拒绝无效的 profile
        assert response.status_code == 422

    def test_max_results_exceeds_limit(self):
        """测试 max_results 超过限制"""
        response = client.post(
            "/internal/log-detective/analyze",
            json={
                "log_text": "test log",
                "profile": "generic",
                "max_results": settings.MAX_RESULTS + 1  # 超过限制
            }
        )

        # Pydantic 验证应该拒绝超限值
        assert response.status_code == 422

    def test_generic_profile_with_mixed_levels(self):
        """测试 generic 模式处理混合日志级别"""
        log_text = """INFO: Application started
DEBUG: Loading configuration
WARN: Deprecated API usage
ERROR: Connection timeout
CRITICAL: System failure""".strip()

        response = client.post(
            "/internal/log-detective/analyze",
            json={
                "log_text": log_text,
                "profile": "generic",
                "max_results": 10
            }
        )

        assert response.status_code == 200
        data = response.json()

        # 验证各级别识别
        assert data["summary"]["total_lines"] == 5
        assert data["summary"]["error_lines"] >= 1
        assert data["summary"]["warn_lines"] >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
