"""日志侦探路由模块"""
from fastapi import APIRouter, HTTPException
from ..schemas import LogDetectiveRequest, LogAnalysisResult
from ..analyzer import analyze_logs

router = APIRouter()


@router.post("/analyze", response_model=LogAnalysisResult)
async def analyze_log_endpoint(request: LogDetectiveRequest):
    """日志分析接口

    教学用：转发到日志侦探服务进行分析
    - 提取可疑 IP
    - 统计错误/警告数量
    - 识别关键错误记录
    """
    try:
        result = analyze_logs(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"请求不合法: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "service": "log_detective"}
