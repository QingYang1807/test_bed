#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TensorFlow Serving 客户端包装器
用于调用 TensorFlow Serving 服务进行模型推理
"""

import os
import numpy as np
import pickle
from typing import Dict, Any, Optional, List
import requests
import json
from datetime import datetime
import jieba

try:
    import tensorflow as tf
    from tensorflow import keras
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("⚠️ TensorFlow未安装，TensorFlow Serving客户端将不可用")


class TensorFlowServingClient:
    """TensorFlow Serving客户端，用于调用远程TF Serving服务"""
    
    def __init__(self, 
                 serving_url: str = "http://localhost:8501",
                 model_name: str = "wide_and_deep_ctr",
                 model_version: Optional[int] = None):
        """
        初始化TensorFlow Serving客户端
        
        Args:
            serving_url: TensorFlow Serving服务地址
            model_name: 模型名称
            model_version: 模型版本号（None表示使用最新版本）
        """
        self.serving_url = serving_url.rstrip('/')
        self.model_name = model_name
        self.model_version = model_version
        
        # 预处理器路径（需要从本地加载）
        self.wide_scaler = None
        self.deep_scaler = None
        self.categorical_encoders = {}
        
        # 预处理器路径
        preprocessor_path = os.path.join(
            os.getcwd(), 
            "models", 
            "wide_deep_ctr_model_preprocessors.pkl"
        )
        self._load_preprocessors(preprocessor_path)
    
    def _load_preprocessors(self, preprocessor_path: str):
        """加载预处理器"""
        try:
            if os.path.exists(preprocessor_path):
                with open(preprocessor_path, 'rb') as f:
                    data = pickle.load(f)
                    self.wide_scaler = data.get('wide_scaler')
                    self.deep_scaler = data.get('deep_scaler')
                    self.categorical_encoders = data.get('categorical_encoders', {})
                print(f"✅ 预处理器加载成功: {preprocessor_path}")
            else:
                print(f"⚠️ 预处理器文件不存在: {preprocessor_path}")
        except Exception as e:
            print(f"❌ 加载预处理器失败: {e}")
    
    def _extract_features(self, query: str, doc_id: str, position: int, 
                         score: float, summary: str, current_timestamp: str = None) -> Dict[str, np.ndarray]:
        """
        提取特征（与WideAndDeepCTRModel中的extract_features保持一致）
        
        Args:
            query: 查询词
            doc_id: 文档ID
            position: 位置
            score: 分数
            summary: 摘要
            current_timestamp: 时间戳
        
        Returns:
            特征字典
        """
        if current_timestamp is None:
            current_timestamp = datetime.now().isoformat()
        
        # 构建单个样本数据
        sample_data = [{
            'query': query,
            'doc_id': doc_id,
            'position': position,
            'score': score,
            'summary': summary,
            'clicked': 0,
            'timestamp': current_timestamp
        }]
        
        # 使用与训练时相同的特征提取逻辑
        import pandas as pd
        
        df = pd.DataFrame(sample_data)
        
        # === Wide特征 ===
        position_features = df['position'].values.reshape(-1, 1)
        position_decay = 1.0 / (position_features.flatten() + 1)
        score_features = df['score'].values.reshape(-1, 1)
        
        # 查询匹配度
        query_words = set(jieba.lcut(df.iloc[0]['query']))
        summary_words = set(jieba.lcut(df.iloc[0]['summary']))
        match_ratio = len(query_words.intersection(summary_words)) / len(query_words) if len(query_words) > 0 else 0
        
        # 历史CTR特征（预测时使用默认值）
        query_ctr = 0.1
        doc_ctr = 0.1
        
        wide_features = np.hstack([
            position_features,
            position_decay.reshape(-1, 1),
            score_features,
            np.array([[match_ratio]]),
            np.array([[query_ctr]]),
            np.array([[doc_ctr]])
        ])
        
        # === Deep特征 ===
        doc_lengths = df['summary'].str.len().values.reshape(-1, 1)
        query_lengths = df['query'].str.len().values.reshape(-1, 1)
        summary_lengths = df['summary'].str.len().values.reshape(-1, 1)
        
        query_word_count = len(jieba.lcut(df.iloc[0]['query']))
        summary_word_count = len(jieba.lcut(df.iloc[0]['summary']))
        
        try:
            timestamp_str = str(current_timestamp)
            time_value = sum(ord(c) for c in timestamp_str) % 1000
        except:
            time_value = 0
        
        position_score_cross = position_features.flatten() * score_features.flatten()
        query_len_match_cross = query_lengths.flatten() * np.array([match_ratio])
        
        deep_features = np.hstack([
            doc_lengths,
            query_lengths,
            summary_lengths,
            np.array([[query_word_count]]),
            np.array([[summary_word_count]]),
            np.array([[time_value]]),
            position_score_cross.reshape(-1, 1),
            query_len_match_cross.reshape(-1, 1)
        ])
        
        # === 分类特征 ===
        query_hash = abs(hash(query)) % 1000
        doc_hash = abs(hash(doc_id)) % 1000
        
        if position <= 3:
            position_group = 0
        elif position <= 10:
            position_group = 1
        else:
            position_group = 2
        
        return {
            'wide': wide_features,
            'deep': deep_features,
            'query_hash': np.array([query_hash]),
            'doc_hash': np.array([doc_hash]),
            'position_group': np.array([position_group])
        }
    
    def _normalize_features(self, features: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """标准化特征"""
        normalized_features = features.copy()
        
        if self.wide_scaler:
            normalized_features['wide'] = self.wide_scaler.transform(features['wide'])
        
        if self.deep_scaler:
            normalized_features['deep'] = self.deep_scaler.transform(features['deep'])
        
        return normalized_features
    
    def _prepare_tf_serving_request(self, features: Dict[str, np.ndarray]) -> Dict[str, Any]:
        """
        准备TensorFlow Serving请求格式
        
        Args:
            features: 特征字典
        
        Returns:
            TF Serving请求格式的字典
        """
        # TensorFlow Serving REST API格式
        # 输入需要转换为列表格式，每个输入是一个数组
        instances = [{
            'wide': features['wide'][0].tolist(),
            'deep': features['deep'][0].tolist(),
            'query_hash': int(features['query_hash'][0]),
            'doc_hash': int(features['doc_hash'][0]),
            'position_group': int(features['position_group'][0])
        }]
        
        return {'instances': instances}
    
    def predict(self, query: str, doc_id: str, position: int, 
                score: float, summary: str, current_timestamp: str = None) -> float:
        """
        调用TensorFlow Serving进行预测
        
        Args:
            query: 查询词
            doc_id: 文档ID
            position: 位置
            score: 分数
            summary: 摘要
            current_timestamp: 时间戳
        
        Returns:
            CTR概率值
        """
        try:
            # 提取特征
            features = self._extract_features(query, doc_id, position, score, summary, current_timestamp)
            
            # 标准化特征
            normalized_features = self._normalize_features(features)
            
            # 准备请求
            request_data = self._prepare_tf_serving_request(normalized_features)
            
            # 构建请求URL
            if self.model_version:
                url = f"{self.serving_url}/v1/models/{self.model_name}/versions/{self.model_version}:predict"
            else:
                url = f"{self.serving_url}/v1/models/{self.model_name}:predict"
            
            # 发送请求
            response = requests.post(
                url,
                json=request_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code != 200:
                raise Exception(f"TensorFlow Serving请求失败: {response.status_code} - {response.text}")
            
            # 解析响应
            result = response.json()
            
            # TF Serving返回格式: {"predictions": [[probability]]}
            if 'predictions' in result and len(result['predictions']) > 0:
                ctr_prob = result['predictions'][0][0]
                return float(ctr_prob)
            else:
                raise Exception(f"TensorFlow Serving响应格式错误: {result}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ TensorFlow Serving请求异常: {e}")
            raise
        except Exception as e:
            print(f"❌ TensorFlow Serving预测失败: {e}")
            raise
    
    def health_check(self) -> bool:
        """检查TensorFlow Serving服务健康状态"""
        try:
            url = f"{self.serving_url}/v1/models/{self.model_name}"
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ TensorFlow Serving健康检查失败: {e}")
            return False
    
    def get_model_status(self) -> Dict[str, Any]:
        """获取模型状态"""
        try:
            url = f"{self.serving_url}/v1/models/{self.model_name}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f'HTTP {response.status_code}'}
        except Exception as e:
            return {'error': str(e)}

