"""LogDetectiveClient HTTP 层测试。"""

import pytest
import respx
from httpx import Response, TimeoutException

from app.log_detective_client import LogDetectiveClient, LogDetectiveServiceError


@pytest.mark.asyncio
@respx.mock
async def test_analyze_logs_success():
    """正常分析日志。"""
    client = LogDetectiveClient(base_url="http://detective")
    respx.post("http://detective/internal/log-detective/analyze").mock(
        return_value=Response(
            200,
            json={
                "summary": "分析完成",
                "suspicious_ips": ["1.2.3.4"],
                "critical_errors": [],
            },
        )
    )

    result = await client.analyze_logs({"log_text": "test log"})
    assert result["summary"] == "分析完成"
    assert "1.2.3.4" in result["suspicious_ips"]


@pytest.mark.asyncio
@respx.mock
async def test_analyze_logs_timeout_raises_error():
    """超时时抛出特定异常。"""
    client = LogDetectiveClient(base_url="http://detective")
    respx.post("http://detective/internal/log-detective/analyze").mock(
        side_effect=TimeoutException("timeout")
    )

    with pytest.raises(LogDetectiveServiceError, match="超时"):
        await client.analyze_logs({"log_text": "test"})


@pytest.mark.asyncio
@respx.mock
async def test_analyze_logs_4xx_raises_error():
    """后端返回 4xx 时抛出异常。"""
    client = LogDetectiveClient(base_url="http://detective")
    respx.post("http://detective/internal/log-detective/analyze").mock(
        return_value=Response(400)
    )

    with pytest.raises(LogDetectiveServiceError, match="状态码：400"):
        await client.analyze_logs({"log_text": "test"})


@pytest.mark.asyncio
@respx.mock
async def test_analyze_logs_5xx_raises_error():
    """后端返回 5xx 时抛出异常。"""
    client = LogDetectiveClient(base_url="http://detective")
    respx.post("http://detective/internal/log-detective/analyze").mock(
        return_value=Response(500)
    )

    with pytest.raises(LogDetectiveServiceError, match="状态码：500"):
        await client.analyze_logs({"log_text": "test"})