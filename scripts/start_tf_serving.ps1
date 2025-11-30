# PowerShell 脚本：启动 TensorFlow Serving 服务

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$DockerDir = Join-Path $ProjectRoot "docker\tf_serving"

Write-Host "🚀 启动 TensorFlow Serving 服务..." -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

# 检查模型文件是否存在
$ModelDir = Join-Path $ProjectRoot "models\wide_deep_ctr_model_tf_serving\1"
if (-not (Test-Path $ModelDir)) {
    Write-Host "❌ 错误: 模型文件不存在: $ModelDir" -ForegroundColor Red
    Write-Host "请先训练 Wide & Deep 模型，模型会自动保存为 TensorFlow Serving 格式" -ForegroundColor Yellow
    exit 1
}

# 检查 Docker 是否运行
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ 错误: Docker 未运行，请先启动 Docker" -ForegroundColor Red
    exit 1
}

# 进入 Docker 目录
Set-Location $DockerDir

# 构建并启动服务
Write-Host "📦 构建 Docker 镜像..." -ForegroundColor Cyan
docker-compose build

Write-Host "🚀 启动 TensorFlow Serving 服务..." -ForegroundColor Cyan
docker-compose up -d

# 等待服务启动
Write-Host "⏳ 等待服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 检查服务健康状态
Write-Host "🔍 检查服务健康状态..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8501/v1/models/wide_and_deep_ctr" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ TensorFlow Serving 服务启动成功！" -ForegroundColor Green
        Write-Host ""
        Write-Host "📋 服务信息:" -ForegroundColor Cyan
        Write-Host "   REST API: http://localhost:8501" -ForegroundColor White
        Write-Host "   gRPC API: http://localhost:8500" -ForegroundColor White
        Write-Host "   模型名称: wide_and_deep_ctr" -ForegroundColor White
        Write-Host ""
        Write-Host "查看日志: docker-compose -f $DockerDir\docker-compose.yml logs -f" -ForegroundColor Yellow
        Write-Host "停止服务: docker-compose -f $DockerDir\docker-compose.yml down" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ 服务可能未完全启动，请检查日志:" -ForegroundColor Yellow
    Write-Host "   docker-compose -f $DockerDir\docker-compose.yml logs" -ForegroundColor Yellow
}

