# TensorFlow Serving Dockerfile for Wide & Deep CTR Model
# 基于官方 TensorFlow Serving 镜像

FROM tensorflow/serving:latest

# 设置工作目录
WORKDIR /models

# 复制模型文件到容器中
# TensorFlow Serving 需要模型目录结构为: /models/{model_name}/{version}/
# 例如: /models/wide_and_deep_ctr/1/
COPY models/wide_deep_ctr_model_tf_serving/ /models/wide_and_deep_ctr/

# 设置环境变量
ENV MODEL_NAME=wide_and_deep_ctr
ENV MODEL_BASE_PATH=/models

# 暴露端口
# 8500: gRPC API
# 8501: REST API
EXPOSE 8500 8501

# 使用默认的 TensorFlow Serving 启动命令
# 可以通过环境变量覆盖 MODEL_NAME 和 MODEL_BASE_PATH
CMD ["tensorflow_model_server", \
     "--port=8500", \
     "--rest_api_port=8501", \
     "--model_name=${MODEL_NAME}", \
     "--model_base_path=${MODEL_BASE_PATH}/${MODEL_NAME}"]

