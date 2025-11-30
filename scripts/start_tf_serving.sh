#!/bin/bash
# 启动 TensorFlow Serving 服务的便捷脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DOCKER_DIR="$PROJECT_ROOT/docker/tf_serving"

echo "🚀 启动 TensorFlow Serving 服务..."
echo "=================================="

# 检查模型文件是否存在
MODEL_DIR="$PROJECT_ROOT/models/wide_deep_ctr_model_tf_serving/1"
if [ ! -d "$MODEL_DIR" ]; then
    echo "❌ 错误: 模型文件不存在: $MODEL_DIR"
    echo "请先训练 Wide & Deep 模型，模型会自动保存为 TensorFlow Serving 格式"
    exit 1
fi

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ 错误: Docker 未运行，请先启动 Docker"
    exit 1
fi

# 进入 Docker 目录
cd "$DOCKER_DIR"

# 构建并启动服务
echo "📦 构建 Docker 镜像..."
docker-compose build

echo "🚀 启动 TensorFlow Serving 服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务健康状态
echo "🔍 检查服务健康状态..."
if curl -f http://localhost:8501/v1/models/wide_and_deep_ctr > /dev/null 2>&1; then
    echo "✅ TensorFlow Serving 服务启动成功！"
    echo ""
    echo "📋 服务信息:"
    echo "   REST API: http://localhost:8501"
    echo "   gRPC API: http://localhost:8500"
    echo "   模型名称: wide_and_deep_ctr"
    echo ""
    echo "查看日志: docker-compose -f $DOCKER_DIR/docker-compose.yml logs -f"
    echo "停止服务: docker-compose -f $DOCKER_DIR/docker-compose.yml down"
else
    echo "⚠️ 服务可能未完全启动，请检查日志:"
    echo "   docker-compose -f $DOCKER_DIR/docker-compose.yml logs"
fi

