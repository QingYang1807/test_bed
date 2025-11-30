# TensorFlow Serving Docker 部署指南

本目录包含用于部署 Wide & Deep CTR 模型的 TensorFlow Serving Docker 配置。

## 目录结构

```
docker/tf_serving/
├── Dockerfile              # TensorFlow Serving 镜像构建文件
├── docker-compose.yml      # Docker Compose 配置文件
└── README.md              # 本文件
```

## 前置要求

1. **Docker** 和 **Docker Compose** 已安装
2. **模型文件已训练并保存**：确保 `models/wide_deep_ctr_model_tf_serving/` 目录存在且包含模型文件

## 快速开始

### 1. 训练并保存模型

首先需要训练 Wide & Deep 模型，模型会自动保存为 TensorFlow Serving 格式：

```bash
# 在项目根目录运行训练脚本或通过 UI 训练模型
# 模型会保存到: models/wide_deep_ctr_model_tf_serving/1/
```

### 2. 构建 Docker 镜像

```bash
cd docker/tf_serving
docker-compose build
```

或者直接使用 docker build：

```bash
docker build -f docker/tf_serving/Dockerfile -t testbed-tf-serving:latest .
```

### 3. 启动 TensorFlow Serving 服务

```bash
docker-compose up -d
```

### 4. 验证服务

检查服务健康状态：

```bash
curl http://localhost:8501/v1/models/wide_and_deep_ctr
```

查看服务日志：

```bash
docker-compose logs -f tensorflow-serving
```

## 配置说明

### 环境变量

- `MODEL_NAME`: 模型名称（默认: `wide_and_deep_ctr`）
- `MODEL_BASE_PATH`: 模型基础路径（默认: `/models`）

### 端口映射

- `8500`: gRPC API 端口
- `8501`: REST API 端口

### 模型目录结构

TensorFlow Serving 要求模型目录结构为：

```
/models/
└── wide_and_deep_ctr/
    └── 1/          # 版本号目录
        ├── saved_model.pb
        └── variables/
            ├── variables.data-00000-of-00001
            └── variables.index
```

## 使用 TensorFlow Serving

### REST API 调用示例

```bash
curl -X POST http://localhost:8501/v1/models/wide_and_deep_ctr:predict \
  -H "Content-Type: application/json" \
  -d '{
    "instances": [{
      "wide": [[1.0, 0.5, 0.8, 0.6, 0.1, 0.1]],
      "deep": [[100, 10, 50, 5, 10, 100, 0.5, 0.3]],
      "query_hash": 123,
      "doc_hash": 456,
      "position_group": 0
    }]
  }'
```

### 在应用中使用

设置环境变量启用 TensorFlow Serving：

```bash
export USE_TF_SERVING=true
export TF_SERVING_URL=http://localhost:8501
export TF_SERVING_MODEL_NAME=wide_and_deep_ctr
```

然后启动应用，Wide & Deep 模型的预测会自动通过 TensorFlow Serving 进行。

## 模型更新

### 方法 1: 重新构建镜像

```bash
# 1. 训练新模型（会自动保存为 TF Serving 格式）
# 2. 重新构建镜像
docker-compose build
# 3. 重启服务
docker-compose restart
```

### 方法 2: 使用 Volume 挂载（推荐）

如果使用 docker-compose.yml 中的 volume 配置，可以直接更新模型文件：

```bash
# 1. 训练新模型
# 2. 模型文件会自动同步到容器中
# 3. TensorFlow Serving 会自动检测并加载新版本
```

TensorFlow Serving 支持版本管理，新版本应放在 `models/wide_and_deep_ctr/2/` 目录中。

## 故障排查

### 检查模型文件是否存在

```bash
ls -la models/wide_deep_ctr_model_tf_serving/1/
```

### 查看容器日志

```bash
docker-compose logs tensorflow-serving
```

### 进入容器检查

```bash
docker-compose exec tensorflow-serving bash
ls -la /models/wide_and_deep_ctr/
```

### 常见问题

1. **模型文件不存在**
   - 确保已训练模型并保存为 TF Serving 格式
   - 检查 `models/wide_deep_ctr_model_tf_serving/1/` 目录

2. **端口被占用**
   - 修改 docker-compose.yml 中的端口映射
   - 或停止占用端口的服务

3. **模型加载失败**
   - 检查模型文件格式是否正确
   - 查看容器日志获取详细错误信息

## 停止服务

```bash
docker-compose down
```

## 参考文档

- [TensorFlow Serving 官方文档](https://www.tensorflow.org/tfx/guide/serving)
- [TensorFlow Serving Docker 镜像](https://hub.docker.com/r/tensorflow/serving)

