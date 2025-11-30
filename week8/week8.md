# 人工智能
## 1 模板选择

[](1.png)

```
## 🎯 阶段1: 模板选择

**选择状态**: ✅ 成功  
**选择方法**: LLM智能选择  
**选择模板**: `simple_chat`  
**置信度**: 0.90  
**耗时**: 9.89秒

**🤖 选择理由**:
用户意图关于'人工智能'较为宽泛，没有具体指向如代码审查、财务分析等特定任务。simple_chat模板适合进行一般性的对话交流，可以用来讨论人工智能相关的话题。

**📝 可用模板**:
- simple_chat: 简单对话提示词 - 使用占位符模式

固定分区（模板内定义）：人设、输出格式
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}
- rag_answer: RAG检索增强提示词 - 使用占位符模式

固定分区（模板内定义）：人设、RAG流程、输出格式
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}
- react_reasoning: ReAct推理提示词 - 使用占位符模式

固定分区（模板内定义）：人设、Few-shot示例
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}
- code_review: 代码审查提示词 - 使用占位符模式

固定分区（模板内定义）：人设、审查标准、输出格式
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}
- financial_analysis: 财务分析提示词 - 使用占位符模式

固定分区（模板内定义）：人设、分析框架、输出格式
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}
- context_engineering: 上下文工程专用提示词 - 使用占位符模式

固定分区（模板内定义）：人设、Few-shot示例
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}

**🔍 选择过程**:
- **用户意图**: 人工智能
- **模板数量**: 6 个
- **选择算法**: LLM驱动的智能选择
- **数据源**: 直接MCP服务器获取
- **选择结果**: simple_chat
```

## 2 上下文装配

[](2.png)

```
🔧 **阶段2完成** (10.59秒) | 模板: simple_chat | 长度: 1002 字符

### 📝 原始模板（包含占位符）

```
[人设] 你是一个友好、专业的AI助手，善于回答各种问题。
你的特点：
1. 回答简洁明了，重点突出
2. 语言流畅自然，易于理解
3. 必要时提供例子或解释
4. 态度友好，乐于助人

[当前状态] 
处理时间: ${local:current_time}
用户意图: ${local:user_intent}

[对话历史] 
${mcp:resource:conversation://current/history}

[用户信息] 
${local:user_profile}

[系统概览] 
${local:system_overview}

[可用工具] 
${mcp:tool:dynamic_tool_selection}

[用户问题] 
人工智能

[输出格式] 
${local:tao_example}

现在请回答用户问题。
```


### ✅ 装配后的完整上下文

```
[人设] 你是一个友好、专业的AI助手，善于回答各种问题。
你的特点：
1. 回答简洁明了，重点突出
2. 语言流畅自然，易于理解
3. 必要时提供例子或解释
4. 态度友好，乐于助人

[当前状态] 
处理时间: 2025-11-30 20:19:44
用户意图: 人工智能

[对话历史] 
[]

[用户信息] 
用户信息：普通用户

[系统概览] 
系统概览：基于MCP协议的上下文工程系统

[可用工具] 
- retrieve: 智能文档检索工具，支持动态决策和思考-行动-观察模式
  输入参数: ['reasoning', 'action', 'query', 'top_k', 'include_metadata']

[用户问题] 
人工智能

[输出格式] 
【输出格式要求】
你必须严格按照以下格式之一输出：

格式1 - 需要调用工具：
Thought: [详细的思考过程，说明为什么需要这个工具]
Action: tool_name(param1="value1", param2="value2")

格式2 - 直接给出答案：
Thought: [详细的思考过程，说明为什么可以直接回答]
Final Answer: [完整的回答内容]

【重要规则】
1. 每行必须以 "Thought:", "Action:", 或 "Final Answer:" 开头
2. Action 只能使用可用工具列表中的工具
3. 参数格式：param="value"，多个参数用逗号分隔
4. 不要输出 "Observation:"，观察结果由系统自动添加

【可用工具】
- retrieve: 从知识库检索相关文档
  参数：query（检索关键词）, top_k（返回文档数量，默认3）
  示例：retrieve(query="量子力学", top_k=3)

【输出示例】
示例1（需要检索）：
Thought: 用户询问量子力学的定义，这是专业知识，我需要从知识库检索准确信息
Action: retrieve(query="量子力学定义", top_k=3)

示例2（直接回答）：
Thought: 这是一个简单的问候，无需检索知识库，我可以直接友好地回答
Final Answer: 你好！我是AI助手，很高兴为您服务。请问有什么可以帮助您的？

现在请回答用户问题。
```

---

**占位符替换说明**:
- `${local:xxx}` → CE Server本地生成（时间、用户意图等）
- `${mcp:resource:xxx}` → 调用MCP Resource获取（对话历史等）
- `${mcp:tool:xxx}` → 调用MCP Tools获取（工具列表等）
```


## 3 LLM推理

[](3.png)

```
🤖 **阶段3完成** (16.58秒) | 模型: qwen-max

### TAO推理结果（已解析）

```json
{
  "thought": "用户的问题非常宽泛，只提到了“人工智能”这个词，没有具体的询问方向。为了能够提供更准确的帮助，我需要更多关于用户对人工智能方面感兴趣的具体信息。",
  "action": "retrieve(query=\"人工智能简介\", top_k=3)",
  "final_answer": null
}
```

---

**说明**:
- **Thought**: 用户的问题非常宽泛，只提到了“人工智能”这个词，没有具体的询问方向。为了能够提供更准确的帮助，我需要更多关于用户对人工智能方面感兴趣的具体信息。...
- **Action**: retrieve(query="人工智能简介", top_k=3)
- **Final Answer**: N/A...

**下一步**: 阶段4将执行工具调用并更新对话历史
```

## 4 上下文更新

[](4.png)

```
🔄 **阶段4完成** (19.25秒)

### ✅ 上下文更新完成

**状态**:
- 历史已更新: True
- 任务完成: True


**完整TAO记录**:
- **Thought**: 用户输入了“人工智能”但没有提出具体问题。我需要先了解用户对于人工智能方面想要了解的具体内容是什么，比如定义、应用领域、未来发展等，因此需要进一步询问以明确用户意图。
- **Action**: （无）
- **Observation**: 已得出最终答案，任务完成


---

**流程说明**:
1. ✅ 解析LLM输出（Thought + Action）
2. ✅ 执行工具调用（获取Observation）
3. ✅ 更新对话历史（保存完整TAO）

**下一步**: 
- 对话历史已包含本轮交互
- 可以继续下一轮对话（基于历史上下文）
```

## 5 系统状态

[](5.png)

```
## 📊 系统状态报告

**🕐 报告时间**: 2025-11-30 20:22:53

**🔗 MCP服务器状态**:
- **连接状态**: ✅ 已连接
- **可用工具**: 1 个
- **可用资源**: 1 个  
- **可用提示词**: 6 个

**🛠️ 可用工具**:

**📚 可用资源**:

**📝 可用提示词**:

**🎯 核心功能**:
- **动态工具选择**: ✅ 已实现
- **模板匹配**: ✅ 已实现
- **上下文工程**: ✅ 已实现
- **智能体循环**: ✅ 已实现
```

## 6 对话历史

[](6.png)

```
[
  {
    "user": "人工智能",
    "assistant": "您好！您提到的人工智能是一个非常广泛的话题，它包括了很多不同的方面，比如AI的基本概念、当前的应用情况以及未来的发展趋势等。请问您可以具体说明一下想了解哪方面的信息吗？这样我可以更好地为您提供帮助。",
    "thought": "用户输入了“人工智能”但没有提出具体问题。我需要先了解用户对于人工智能方面想要了解的具体内容是什么，比如定义、应用领域、未来发展等，因此需要进一步询问以明确用户意图。",
    "action": null,
    "observation": "已得出最终答案，任务完成",
    "final_answer": "您好！您提到的人工智能是一个非常广泛的话题，它包括了很多不同的方面，比如AI的基本概念、当前的应用情况以及未来的发展趋势等。请问您可以具体说明一下想了解哪方面的信息吗？这样我可以更好地为您提供帮助。",
    "timestamp": "2025-11-30T20:20:57.427763"
  }
]
```


# 查询今天北京的天气

## 1 模板选择

[](7.png)

```
## 🎯 阶段1: 模板选择

**选择状态**: ✅ 成功  
**选择方法**: LLM智能选择  
**选择模板**: `rag_answer`  
**置信度**: 0.90  
**耗时**: 11.74秒

**🤖 选择理由**:
用户需要查询具体的天气信息，这涉及到从外部数据源检索实时信息。rag_answer模板通过其RAG流程能够有效地支持这种类型的信息检索需求。

**📝 可用模板**:
- simple_chat: 简单对话提示词 - 使用占位符模式

固定分区（模板内定义）：人设、输出格式
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}
- rag_answer: RAG检索增强提示词 - 使用占位符模式

固定分区（模板内定义）：人设、RAG流程、输出格式
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}
- react_reasoning: ReAct推理提示词 - 使用占位符模式

固定分区（模板内定义）：人设、Few-shot示例
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}
- code_review: 代码审查提示词 - 使用占位符模式

固定分区（模板内定义）：人设、审查标准、输出格式
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}
- financial_analysis: 财务分析提示词 - 使用占位符模式

固定分区（模板内定义）：人设、分析框架、输出格式
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}
- context_engineering: 上下文工程专用提示词 - 使用占位符模式

固定分区（模板内定义）：人设、Few-shot示例
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}

**🔍 选择过程**:
- **用户意图**: 查询今天北京的天气
- **模板数量**: 6 个
- **选择算法**: LLM驱动的智能选择
- **数据源**: 直接MCP服务器获取
- **选择结果**: rag_answer
```

## 2 上下文装配

[](8.png)

```
🔧 **阶段2完成** (6.40秒) | 模板: rag_answer | 长度: 1342 字符

### 📝 原始模板（包含占位符）

```
[人设] 你是一个专业的信息检索与分析专家，擅长使用RAG（检索增强生成）技术回答问题。
你的核心能力：
1. 精准检索：从知识库中检索最相关的信息
2. 深度理解：分析检索结果，提取关键信息
3. 综合回答：结合检索内容和背景知识，给出完整答案
4. 来源标注：明确标注信息来源，增强可信度

[当前状态] 
处理时间: ${local:current_time}
用户意图: ${local:user_intent}

[对话历史] 
${mcp:resource:conversation://current/history}

[用户信息] 
${local:user_profile}

[系统概览] 
${local:system_overview}

[可用工具] 
${mcp:tool:dynamic_tool_selection}

[用户问题] 
查询今天北京的天气

[RAG工作流程]
1. **理解问题**：分析用户问题的核心意图和关键信息需求
2. **检索信息**：使用retrieve工具从知识库检索相关文档
3. **分析整合**：评估检索结果的相关性和可信度
4...
```


### ✅ 装配后的完整上下文

```
[人设] 你是一个专业的信息检索与分析专家，擅长使用RAG（检索增强生成）技术回答问题。
你的核心能力：
1. 精准检索：从知识库中检索最相关的信息
2. 深度理解：分析检索结果，提取关键信息
3. 综合回答：结合检索内容和背景知识，给出完整答案
4. 来源标注：明确标注信息来源，增强可信度

[当前状态] 
处理时间: 2025-11-30 20:26:15
用户意图: 查询今天北京的天气

[对话历史] 
用户: 人工智能
助手: 您好！您提到的人工智能是一个非常广泛的话题，它包括了很多不同的方面，比如AI的基本概念、当前的应用情况以及未来的发展趋势等。请问您可以具体说明一下想了解哪方面的信息吗？这样我可以更好地为您提供帮助。

[用户信息] 
用户信息：普通用户

[系统概览] 
系统概览：基于MCP协议的上下文工程系统

[可用工具] 
- retrieve: 智能文档检索工具，支持动态决策和思考-行动-观察模式
  输入参数: ['reasoning', 'action', 'query', 'top_k', 'include_metadata']

[用户问题] 
查询今天北京的天气

[RAG工作流程]
1. **理解问题**：分析用户问题的核心意图和关键信息需求
2. **检索信息**：使用retrieve工具从知识库检索相关文档
3. **分析整合**：评估检索结果的相关性和可信度
4. **生成答案**：基于检索内容生成准确、完整的回答
5. **标注来源**：注明信息来源，便于用户验证

[输出格式] 
【输出格式要求】
你必须严格按照以下格式之一输出：

格式1 - 需要调用工具：
Thought: [详细的思考过程，说明为什么需要这个工具]
Action: tool_name(param1="value1", param2="value2")

格式2 - 直接给出答案：
Thought: [详细的思考过程，说明为什么可以直接回答]
Final Answer: [完整的回答内容]

【重要规则】
1. 每行必须以 "Thought:", "Action:", 或 "Final Answer:" 开头
2. Action 只能使用可用工具列表中的工具
3. 参数格式：param="value"，多个参数用逗号分隔
4. 不要输出 "Observation:"，观察结果由系统自动添加

【可用工具】
- retrieve: 从知识库检索相关文档
  参数：query（检索关键词）, top_k（返回文档数量，默认3）
  示例：retrieve(query="量子力学", top_k=3)

【输出示例】
示例1（需要检索）：
Thought: 用户询问量子力学的定义，这是专业知识，我需要从知识库检索准确信息
Action: retrieve(query="量子力学定义", top_k=3)

示例2（直接回答）：
Thought: 这是一个简单的问候，无需检索知识库，我可以直接友好地回答
Final Answer: 你好！我是AI助手，很高兴为您服务。请问有什么可以帮助您的？

现在请使用RAG流程回答用户问题。
```

---

**占位符替换说明**:
- `${local:xxx}` → CE Server本地生成（时间、用户意图等）
- `${mcp:resource:xxx}` → 调用MCP Resource获取（对话历史等）
- `${mcp:tool:xxx}` → 调用MCP Tools获取（工具列表等）
```

## 3 LLM推理

[](9.png)

```
🤖 **阶段3完成** (15.99秒) | 模型: qwen-max

### TAO推理结果（已解析）

```json
{
  "thought": "用户想要知道今天北京的天气情况，这类实时信息需要通过网络获取最新的气象数据来提供准确答案。",
  "action": "retrieve(query=\"今天北京天气\", top_k=1)",
  "final_answer": null
}
```

---

**说明**:
- **Thought**: 用户想要知道今天北京的天气情况，这类实时信息需要通过网络获取最新的气象数据来提供准确答案。...
- **Action**: retrieve(query="今天北京天气", top_k=1)
- **Final Answer**: N/A...

**下一步**: 阶段4将执行工具调用并更新对话历史
```


## 4 上下文更新

[](10.png)

```
🔄 **阶段4完成** (20.70秒)

### ✅ 上下文更新完成

**状态**:
- 历史已更新: True
- 任务完成: False


**完整TAO记录**:
- **Thought**: 用户想要知道今天北京的天气情况，这类实时信息我需要通过特定工具来获取最新数据。
- **Action**: retrieve(query="今天北京天气", top_k=1)
- **Observation**: [TextContent(type='text', text='{"status":"success","observation":{"reasoning":"","action":"search","query":"今天北京天气","timestamp":"now","tool":"retrieve","result":"检索完成","documents":[],"total_found":0},"query":"今天北京天气","documents":[],"total_found":0,"source":"dynamic_mcp_server","search_metadata":{"query_time":"real_time","index_size":0}}', annotations=None, meta=None)]


---

**流程说明**:
1. ✅ 解析LLM输出（Thought + Action）
2. ✅ 执行工具调用（获取Observation）
3. ✅ 更新对话历史（保存完整TAO）

**下一步**: 
- 对话历史已包含本轮交互
- 可以继续下一轮对话（基于历史上下文）
```



# SEARCH["人工智能"]
## 1 模板选择

```
## 🎯 阶段1: 模板选择

**选择状态**: ✅ 成功  
**选择方法**: LLM智能选择  
**选择模板**: `rag_answer`  
**置信度**: 0.95  
**耗时**: 10.31秒

**🤖 选择理由**:
用户需要搜索关于人工智能的信息，rag_answer模板专门用于检索增强生成，能够更好地满足用户的搜索需求

**📝 可用模板**:
- simple_chat: 简单对话提示词 - 使用占位符模式

固定分区（模板内定义）：人设、输出格式
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}
- rag_answer: RAG检索增强提示词 - 使用占位符模式

固定分区（模板内定义）：人设、RAG流程、输出格式
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}
- react_reasoning: ReAct推理提示词 - 使用占位符模式

固定分区（模板内定义）：人设、Few-shot示例
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}
- code_review: 代码审查提示词 - 使用占位符模式

固定分区（模板内定义）：人设、审查标准、输出格式
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}
- financial_analysis: 财务分析提示词 - 使用占位符模式

固定分区（模板内定义）：人设、分析框架、输出格式
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}
- context_engineering: 上下文工程专用提示词 - 使用占位符模式

固定分区（模板内定义）：人设、Few-shot示例
动态分区（占位符）：通过CE Server替换

占位符格式：${local:xxx} 或 ${mcp:resource:xxx} 或 ${mcp:tool:xxx}

**🔍 选择过程**:
- **用户意图**: SEARCH["人工智能"]
- **模板数量**: 6 个
- **选择算法**: LLM驱动的智能选择
- **数据源**: 直接MCP服务器获取
- **选择结果**: rag_answer
```

## 2 上下文装配

```
🔧 **阶段2完成** (7.18秒) | 模板: rag_answer | 长度: 1593 字符

### 📝 原始模板（包含占位符）

```
[人设] 你是一个专业的信息检索与分析专家，擅长使用RAG（检索增强生成）技术回答问题。
你的核心能力：
1. 精准检索：从知识库中检索最相关的信息
2. 深度理解：分析检索结果，提取关键信息
3. 综合回答：结合检索内容和背景知识，给出完整答案
4. 来源标注：明确标注信息来源，增强可信度

[当前状态] 
处理时间: ${local:current_time}
用户意图: ${local:user_intent}

[对话历史] 
${mcp:resource:conversation://current/history}

[用户信息] 
${local:user_profile}

[系统概览] 
${local:system_overview}

[可用工具] 
${mcp:tool:dynamic_tool_selection}

[用户问题] 
SEARCH["人工智能"]

[RAG工作流程]
1. **理解问题**：分析用户问题的核心意图和关键信息需求
2. **检索信息**：使用retrieve工具从知识库检索相关文档
3. **分析整合**：评估检索结果的相关性和...
```


### ✅ 装配后的完整上下文

```
🔧 **阶段2完成** (6.74秒) | 模板: rag_answer | 长度: 1593 字符

### 📝 原始模板（包含占位符）

```
[人设] 你是一个专业的信息检索与分析专家，擅长使用RAG（检索增强生成）技术回答问题。
你的核心能力：
1. 精准检索：从知识库中检索最相关的信息
2. 深度理解：分析检索结果，提取关键信息
3. 综合回答：结合检索内容和背景知识，给出完整答案
4. 来源标注：明确标注信息来源，增强可信度

[当前状态] 
处理时间: ${local:current_time}
用户意图: ${local:user_intent}

[对话历史] 
${mcp:resource:conversation://current/history}

[用户信息] 
${local:user_profile}

[系统概览] 
${local:system_overview}

[可用工具] 
${mcp:tool:dynamic_tool_selection}

[用户问题] 
SEARCH["人工智能"]

[RAG工作流程]
1. **理解问题**：分析用户问题的核心意图和关键信息需求
2. **检索信息**：使用retrieve工具从知识库检索相关文档
3. **分析整合**：评估检索结果的相关性和...
```


### ✅ 装配后的完整上下文

```
[人设] 你是一个专业的信息检索与分析专家，擅长使用RAG（检索增强生成）技术回答问题。
你的核心能力：
1. 精准检索：从知识库中检索最相关的信息
2. 深度理解：分析检索结果，提取关键信息
3. 综合回答：结合检索内容和背景知识，给出完整答案
4. 来源标注：明确标注信息来源，增强可信度

[当前状态] 
处理时间: 2025-11-30 20:33:45
用户意图: SEARCH["人工智能"]

[对话历史] 
用户: 人工智能
助手: 您好！您提到的人工智能是一个非常广泛的话题，它包括了很多不同的方面，比如AI的基本概念、当前的应用情况以及未来的发展趋势等。请问您可以具体说明一下想了解哪方面的信息吗？这样我可以更好地为您提供帮助。

用户: 查询今天北京的天气
助手: Thought: 用户想要知道今天北京的天气情况，这类实时信息我需要通过特定工具来获取最新数据。
Action: retrieve(query="今天北京天气", top_k=1)

用户: SEARCH["人工智能"]
助手: 人工智能（AI）是指由人制造出来的具有一定智能的系统或软件，能够完成通常需要人类智慧才能完成的任务。它被广泛应用于语音识别、图像处理、自然语言处理等领域。如果您对某个特定领域感兴趣或者想要了解更多细节，请告诉我！

[用户信息] 
用户信息：普通用户

[系统概览] 
系统概览：基于MCP协议的上下文工程系统

[可用工具] 
- retrieve: 智能文档检索工具，支持动态决策和思考-行动-观察模式
  输入参数: ['reasoning', 'action', 'query', 'top_k', 'include_metadata']

[用户问题] 
SEARCH["人工智能"]

[RAG工作流程]
1. **理解问题**：分析用户问题的核心意图和关键信息需求
2. **检索信息**：使用retrieve工具从知识库检索相关文档
3. **分析整合**：评估检索结果的相关性和可信度
4. **生成答案**：基于检索内容生成准确、完整的回答
5. **标注来源**：注明信息来源，便于用户验证

[输出格式] 
【输出格式要求】
你必须严格按照以下格式之一输出：

格式1 - 需要调用工具：
Thought: [详细的思考过程，说明为什么需要这个工具]
Action: tool_name(param1="value1", param2="value2")

格式2 - 直接给出答案：
Thought: [详细的思考过程，说明为什么可以直接回答]
Final Answer: [完整的回答内容]

【重要规则】
1. 每行必须以 "Thought:", "Action:", 或 "Final Answer:" 开头
2. Action 只能使用可用工具列表中的工具
3. 参数格式：param="value"，多个参数用逗号分隔
4. 不要输出 "Observation:"，观察结果由系统自动添加

【可用工具】
- retrieve: 从知识库检索相关文档
  参数：query（检索关键词）, top_k（返回文档数量，默认3）
  示例：retrieve(query="量子力学", top_k=3)

【输出示例】
示例1（需要检索）：
Thought: 用户询问量子力学的定义，这是专业知识，我需要从知识库检索准确信息
Action: retrieve(query="量子力学定义", top_k=3)

示例2（直接回答）：
Thought: 这是一个简单的问候，无需检索知识库，我可以直接友好地回答
Final Answer: 你好！我是AI助手，很高兴为您服务。请问有什么可以帮助您的？

现在请使用RAG流程回答用户问题。
```

---

**占位符替换说明**:
- `${local:xxx}` → CE Server本地生成（时间、用户意图等）
- `${mcp:resource:xxx}` → 调用MCP Resource获取（对话历史等）
- `${mcp:tool:xxx}` → 调用MCP Tools获取（工具列表等）
```

## 3 LLM推理
```
🤖 **阶段3完成** (20.31秒) | 模型: qwen-max

### TAO推理结果（已解析）

```json
{
  "thought": "用户再次提到了“SEARCH[人工智能]”，这可能意味着用户希望获取更多关于人工智能的基本信息或最新发展。由于我之前已经提供了一些基本信息，这次应该尝试提供更多具体领域的介绍或者最新的发展趋势。不过，为了确保提供的信息是最新的，并且符合用户的兴趣点，最好先通过检索工具获取一些相关资料。",
  "action": "retrieve(query=\"人工智能最新发展\", top_k=3)",
  "final_answer": null
}
```

---

**说明**:
- **Thought**: 用户再次提到了“SEARCH[人工智能]”，这可能意味着用户希望获取更多关于人工智能的基本信息或最新发展。由于我之前已经提供了一些基本信息，这次应该尝试提供更多具体领域的介绍或者最新的发展趋势。不过，...
- **Action**: retrieve(query="人工智能最新发展", top_k=3)
- **Final Answer**: N/A...

**下一步**: 阶段4将执行工具调用并更新对话历史
```

## 4 上下文更新

```
🔄 **阶段4完成** (22.83秒)

### ✅ 上下文更新完成

**状态**:
- 历史已更新: True
- 任务完成: False


**完整TAO记录**:
- **Thought**: 用户再次提到了“SEARCH[人工智能]”，这可能意味着用户希望获得更多关于人工智能的信息。由于之前已经提供了一些基本信息，这次可以尝试更深入地探讨一些话题或应用案例来满足用户的需求。
- **Action**: retrieve(query="人工智能的应用案例", top_k=3)
- **Observation**: [TextContent(type='text', text='{"status":"success","observation":{"reasoning":"","action":"search","query":"人工智能的应用案例","timestamp":"now","tool":"retrieve","result":"检索完成","documents":[],"total_found":0},"query":"人工智能的应用案例","documents":[],"total_found":0,"source":"dynamic_mcp_server","search_metadata":{"query_time":"real_time","index_size":0}}', annotations=None, meta=None)]


---

**流程说明**:
1. ✅ 解析LLM输出（Thought + Action）
2. ✅ 执行工具调用（获取Observation）
3. ✅ 更新对话历史（保存完整TAO）

**下一步**: 
- 对话历史已包含本轮交互
- 可以继续下一轮对话（基于历史上下文）
```

## 5 系统状态

[](10.png)

## 6 对话历史

[](11.png)

```
[
  {
    "user": "人工智能",
    "assistant": "您好！您提到的人工智能是一个非常广泛的话题，它包括了很多不同的方面，比如AI的基本概念、当前的应用情况以及未来的发展趋势等。请问您可以具体说明一下想了解哪方面的信息吗？这样我可以更好地为您提供帮助。",
    "thought": "用户输入了“人工智能”但没有提出具体问题。我需要先了解用户对于人工智能方面想要了解的具体内容是什么，比如定义、应用领域、未来发展等，因此需要进一步询问以明确用户意图。",
    "action": null,
    "observation": "已得出最终答案，任务完成",
    "final_answer": "您好！您提到的人工智能是一个非常广泛的话题，它包括了很多不同的方面，比如AI的基本概念、当前的应用情况以及未来的发展趋势等。请问您可以具体说明一下想了解哪方面的信息吗？这样我可以更好地为您提供帮助。",
    "timestamp": "2025-11-30T20:20:57.427763"
  },
  {
    "user": "查询今天北京的天气",
    "assistant": "Thought: 用户想要知道今天北京的天气情况，这类实时信息我需要通过特定工具来获取最新数据。\nAction: retrieve(query=\"今天北京天气\", top_k=1)",
    "thought": "用户想要知道今天北京的天气情况，这类实时信息我需要通过特定工具来获取最新数据。",
    "action": "retrieve(query=\"今天北京天气\", top_k=1)",
    "observation": "[TextContent(type='text', text='{\"status\":\"success\",\"observation\":{\"reasoning\":\"\",\"action\":\"search\",\"query\":\"今天北京天气\",\"timestamp\":\"now\",\"tool\":\"retrieve\",\"result\":\"检索完成\",\"documents\":[],\"total_found\":0},\"query\":\"今天北京天气\",\"documents\":[],\"total_found\":0,\"source\":\"dynamic_mcp_server\",\"search_metadata\":{\"query_time\":\"real_time\",\"index_size\":0}}', annotations=None, meta=None)]",
    "final_answer": null,
    "timestamp": "2025-11-30T20:29:04.196706"
  },
  {
    "user": "SEARCH[\"人工智能\"]",
    "assistant": "人工智能（AI）是指由人制造出来的具有一定智能的系统或软件，能够完成通常需要人类智慧才能完成的任务。它被广泛应用于语音识别、图像处理、自然语言处理等领域。如果您对某个特定领域感兴趣或者想要了解更多细节，请告诉我！",
    "thought": "用户再次提到了“人工智能”，但没有明确具体想了解的内容。考虑到之前已经询问过用户的具体需求，这次应该尝试提供一些基础性的信息来引导对话。",
    "action": null,
    "observation": "已得出最终答案，任务完成",
    "final_answer": "人工智能（AI）是指由人制造出来的具有一定智能的系统或软件，能够完成通常需要人类智慧才能完成的任务。它被广泛应用于语音识别、图像处理、自然语言处理等领域。如果您对某个特定领域感兴趣或者想要了解更多细节，请告诉我！",
    "timestamp": "2025-11-30T20:31:13.424461"
  },
  {
    "user": "SEARCH[\"人工智能\"]",
    "assistant": "Thought: 用户再次提到了“SEARCH[人工智能]”，这可能意味着用户希望获得更多关于人工智能的信息。由于之前已经提供了一些基本信息，这次可以尝试更深入地探讨一些话题或应用案例来满足用户的需求。\nAction: retrieve(query=\"人工智能的应用案例\", top_k=3)",
    "thought": "用户再次提到了“SEARCH[人工智能]”，这可能意味着用户希望获得更多关于人工智能的信息。由于之前已经提供了一些基本信息，这次可以尝试更深入地探讨一些话题或应用案例来满足用户的需求。",
    "action": "retrieve(query=\"人工智能的应用案例\", top_k=3)",
    "observation": "[TextContent(type='text', text='{\"status\":\"success\",\"observation\":{\"reasoning\":\"\",\"action\":\"search\",\"query\":\"人工智能的应用案例\",\"timestamp\":\"now\",\"tool\":\"retrieve\",\"result\":\"检索完成\",\"documents\":[],\"total_found\":0},\"query\":\"人工智能的应用案例\",\"documents\":[],\"total_found\":0,\"source\":\"dynamic_mcp_server\",\"search_metadata\":{\"query_time\":\"real_time\",\"index_size\":0}}', annotations=None, meta=None)]",
    "final_answer": null,
    "timestamp": "2025-11-30T20:34:54.896794"
  }
]
```

<!-- # 
## 1 模板选择

## 2 上下文装配

## 3 LLM推理

## 4 上下文更新 -->