# 🧠 Kidney Agent：基于 GPT 的肾病指标分析系统

## 1. 项目简介

`Kidney Agent` 是一个面向肾病相关检测场景的智能分析项目，核心思路是将：

- **规则引擎**
- **大语言模型（GPT API）**
- **FastAPI 后端服务**
- **历史记录与趋势分析**

结合起来，对患者的肾病相关指标进行结构化分析，并生成中文解释结果。

这个项目当前已经具备一个可运行的最小闭环：

1. 接收患者的结构化指标数据
2. 做基础数据校验
3. 使用规则引擎判断异常项、风险等级、CKD 分期
4. 调用 GPT 生成中文医学解释
5. 保存同一患者的历史分析记录
6. 提供趋势分析接口，判断指标是改善、恶化还是稳定

---

## 2. 项目目标

本项目的目标不是做“自动诊断”，而是做一个**辅助分析 Agent**，帮助完成以下工作：

- 对患者的肾病相关指标进行初步解读
- 给出结构化的异常项和风险提示
- 自动生成中文总结，减少人工解释成本
- 为医生端或患者端提供可读的分析报告
- 记录患者多次检测结果，用于长期随访和趋势判断

---

## 3. 适用场景

这个项目适合以下场景：

### 3.1 医疗辅助分析

用于对肾功能、蛋白尿、血压等指标进行自动初步解释。

### 3.2 患者随访

用于记录同一患者多次检测结果，观察肾功能是否恶化。

### 3.3 AI 项目展示

适合当作一个“规则引擎 + 大模型 + API 服务”的完整后端 AI 项目展示。

### 3.4 面试项目

适合用于展示以下能力：

- Python 后端开发
- FastAPI 接口设计
- OpenAI API 接入
- 规则引擎设计
- 多模块项目结构拆分
- 面向医疗场景的 AI 应用落地

---

## 4. 当前已实现功能

### 4.1 单次指标分析

系统支持输入一位患者的结构化指标，例如：

- 年龄
- 性别
- 血肌酐（Scr）
- eGFR
- ACR（尿白蛋白/肌酐比）
- 收缩压 / 舒张压
- 尿蛋白
- 病史

系统会输出：

- 风险等级
- CKD 分期
- eGFR 严重程度
- 异常项列表
- 规则引擎总结
- GPT 中文解释
- 建议项
- 注意事项

---

### 4.2 风险分层

系统根据规则引擎结果，对患者进行风险等级划分，例如：

- 低
- 低-中
- 中
- 高
- 极高

---

### 4.3 CKD 分期

基于 eGFR 对患者进行参考分期：

- G1
- G2
- G3a
- G3b
- G4
- G5

---

### 4.4 中文 GPT 输出

系统会调用 GPT API，根据：

- 患者原始指标
- 规则引擎结果

生成中文 JSON 结果，包括：

- 总体结论
- 指标解释
- 建议事项
- 风险提示

---

### 4.5 历史记录保存

当前版本支持将同一患者的多次分析结果保存在内存中。

说明：

- 使用 `patient_id` 区分不同患者
- 每次分析都会追加一条记录
- 当前为内存存储版本，重启服务后数据会丢失

---

### 4.6 趋势分析

系统支持对同一患者的历史记录进行趋势分析，判断：

- Scr 趋势：改善 / 恶化 / 稳定
- eGFR 趋势：改善 / 恶化 / 稳定
- ACR 趋势：改善 / 恶化 / 稳定
- 血压趋势：改善 / 恶化 / 稳定

并生成中文趋势总结。

---

## 5. 项目整体架构

系统采用分层设计，整体调用流程如下：

```text
客户端 / 测试脚本
        ↓
    FastAPI 接口层
        ↓
    AgentService 总调度
        ↓
 ┌─────────────────────────────┐
 │ 1. validator 数据校验       │
 │ 2. rule_engine 规则分析     │
 │ 3. prompts 构建提示词       │
 │ 4. gpt_service 调用模型     │
 │ 5. history_repository 存储  │
 │ 6. trend_service 趋势分析   │
 └─────────────────────────────┘
```

---

## 6. 项目目录结构

当前项目建议的核心目录结构如下：

```text
agent/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── analyze.py
│   │       ├── history.py
│   │       ├── health.py
│   │       └── patient.py
│   │
│   ├── core/
│   │   └── prompts.py
│   │
│   ├── repositories/
│   │   └── history_repository.py
│   │
│   ├── schemas/
│   │   └── patient.py
│   │
│   ├── services/
│   │   ├── agent_service.py
│   │   ├── gpt_service.py
│   │   ├── rule_engine.py
│   │   └── trend_service.py
│   │
│   ├── utils/
│   │   └── validator.py
│   │
│   ├── config.py
│   └── main.py
│
├── tests/
│   ├── manual_api_test.py
│   └── api_test.http
│
├── .env
├── requirements.txt
└── README.md
```

---

## 7. 各模块说明

## 7.1 `app/main.py`

FastAPI 应用入口文件，负责：

- 创建 `FastAPI` 实例
- 注册各个路由
- 启动整个后端服务

---

## 7.2 `app/config.py`

配置文件，负责读取环境变量，例如：

- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `APP_NAME`

通常会从 `.env` 文件中读取。

---

## 7.3 `app/api/routes/analyze.py`

分析接口路由文件。

主要负责：

- 接收前端或测试脚本发来的分析请求
- 将请求数据交给 `AgentService`
- 返回最终分析结果

对应接口：

```http
POST /analyze
```

---

## 7.4 `app/api/routes/history.py`

历史记录与趋势分析接口。

负责：

- 查询某个患者的历史记录
- 对该患者的历史指标做趋势分析

对应接口：

```http
GET /history/{patient_id}
GET /history/{patient_id}/trend
```

---

## 7.5 `app/api/routes/health.py`

健康检查接口。

用于快速判断服务是否正常运行。

对应接口：

```http
GET /health
```

---

## 7.6 `app/services/agent_service.py`

项目总调度层，也是项目的核心“大脑”。

主要流程：

1. 校验输入数据
2. 调用规则引擎
3. 构造 GPT prompt
4. 调用 GPT API
5. 合并规则分析结果和 GPT 输出
6. 保存历史记录
7. 返回最终 JSON

---

## 7.7 `app/services/rule_engine.py`

规则引擎模块。

负责根据医学规则对指标进行初步判断，例如：

- 血肌酐是否升高
- eGFR 是否下降
- ACR 是否异常
- 血压是否升高
- 是否提示蛋白尿风险

同时输出：

- `risk_level`
- `ckd_stage`
- `egfr_severity`
- `abnormal_items`
- `rule_based_summary`

---

## 7.8 `app/services/gpt_service.py`

模型调用模块。

负责：

- 初始化 OpenAI Client
- 调用 GPT API
- 获取模型返回结果
- 解析 JSON
- 将结果整理成统一字典结构

---

## 7.9 `app/services/trend_service.py`

趋势分析模块。

负责比较同一患者不同时间点的指标变化，例如：

- 第一条记录和最后一条记录对比
- 指标是否上升 / 下降
- 对应是改善还是恶化

---

## 7.10 `app/repositories/history_repository.py`

历史记录存储层。

当前版本为**内存存储**，主要用于：

- 保存单次分析后的记录
- 根据 `patient_id` 查询同一患者历史数据

后续可以升级为：

- SQLite
- MySQL
- PostgreSQL

---

## 7.11 `app/utils/validator.py`

输入数据校验模块。

负责：

- 必填字段校验
- 类型校验
- 数值字段合法性判断
- 性别字段值校验

---

## 7.12 `app/core/prompts.py`

Prompt 模板文件。

负责构建给 GPT 的系统提示词和用户输入内容，控制模型：

- 输出中文
- 输出 JSON
- 不要夸大结论
- 不要做明确诊断

---

## 8. 当前接口设计

## 8.1 健康检查接口

```http
GET /health
```

### 返回示例

```json
{
  "status": "ok",
  "message": "Kidney Agent is running"
}
```

---

## 8.2 分析接口

```http
POST /analyze
```

### 示例请求体

```json
{
  "patient_id": "P001",
  "age": 60,
  "gender": "male",
  "scr": 150,
  "egfr": 50,
  "acr": 120,
  "sbp": 150,
  "dbp": 95,
  "history": ["hypertension", "diabetes"]
}
```

### 示例返回体

```json
{
  "patient_id": "P001",
  "risk_level": "高",
  "ckd_stage": "G3b",
  "egfr_severity": "中重度下降",
  "abnormal_items": [
    "血肌酐升高",
    "eGFR下降",
    "尿白蛋白/肌酐比升高",
    "收缩压升高",
    "舒张压升高"
  ],
  "rule_based_summary": "规则分析提示存在肾脏相关异常，当前异常包括：血肌酐升高、eGFR下降、尿白蛋白/肌酐比升高、收缩压升高、舒张压升高。结合 eGFR 表现，当前可参考 CKD 分期为 G3b，肾功能严重程度判断为：中重度下降。整体风险等级为：高。",
  "gpt_summary": "当前指标提示患者存在较明显的肾功能受损及蛋白尿风险。",
  "gpt_explanation": "血肌酐升高及 eGFR 下降提示肾小球滤过功能可能受损，ACR 升高提示肾脏损伤风险增加，同时血压升高可能进一步加重肾脏负担。",
  "recommendations": [
    "建议复查肾功能相关指标",
    "建议复查尿白蛋白/肌酐比",
    "建议规律监测血压并结合临床进一步评估"
  ],
  "caution": "以上结果仅用于辅助分析，不能替代医生诊断，请结合临床表现和进一步检查由专业医生判断。"
}
```

---

## 8.3 历史记录接口

```http
GET /history/{patient_id}
```

### 返回内容

返回某个患者的所有历史分析记录。

---

## 8.4 趋势分析接口

```http
GET /history/{patient_id}/trend
```

### 返回内容

返回某个患者多次检测结果的变化趋势，例如：

- 血肌酐：恶化
- eGFR：恶化
- ACR：恶化
- 收缩压：恶化
- 舒张压：恶化

---

## 9. 当前输入字段说明

支持的主要输入字段如下：

| 字段名            | 类型          | 说明            |
| ----------------- | ------------- | --------------- |
| `patient_id`    | `str`       | 患者唯一标识    |
| `age`           | `int`       | 年龄            |
| `gender`        | `str`       | 性别            |
| `scr`           | `float`     | 血肌酐          |
| `bun`           | `float`     | 尿素氮          |
| `egfr`          | `float`     | 肾小球滤过率    |
| `acr`           | `float`     | 尿白蛋白/肌酐比 |
| `urine_protein` | `str`       | 尿蛋白结果      |
| `sbp`           | `float`     | 收缩压          |
| `dbp`           | `float`     | 舒张压          |
| `history`       | `list[str]` | 既往病史        |

---

## 10. 风险判断逻辑概述

当前项目中的规则判断是一个简化版原型，核心思路如下：

### 10.1 Scr

如果 `scr > 133`，提示：

- 血肌酐升高

---

### 10.2 eGFR

根据 eGFR 判断：

- 是否下降
- CKD 分期
- 严重程度
- 风险等级

参考逻辑：

- `>= 90`：G1
- `>= 60`：G2
- `>= 45`：G3a
- `>= 30`：G3b
- `>= 15`：G4
- `< 15`：G5

---

### 10.3 ACR

如果：

- `ACR >= 30`：提示升高
- `ACR >= 300`：提示重度升高

---

### 10.4 血压

如果：

- `SBP >= 140`：收缩压升高
- `DBP >= 90`：舒张压升高

---

### 10.5 尿蛋白

若结果为：

- `positive`
- `+`
- `1+`
- `2+`
- `3+`

则提示尿蛋白异常。

---

## 11. 中文 GPT 输出说明

系统通过 `prompts.py` 控制 GPT 输出，要求模型：

- 使用中文
- 输出严格 JSON
- 不输出 markdown
- 不做明确诊断
- 输出谨慎、专业的解释

返回字段包括：

- `summary`
- `explanation`
- `recommendations`
- `caution`

---

## 12. 测试方式

当前支持以下测试方式。

## 12.1 Swagger 文档测试

启动服务后，打开：

```text
http://127.0.0.1:8000/docs
```

可以直接在页面里测试：

- `POST /analyze`
- `GET /history/{patient_id}`
- `GET /history/{patient_id}/trend`

---

## 12.2 Python 测试脚本

可通过：

```bash
python tests/manual_api_test.py
```

对接口进行顺序测试。

建议顺序：

1. 第一次调用 `POST /analyze`
2. 第二次调用 `POST /analyze`
3. 查询 `GET /history/P001`
4. 查询 `GET /history/P001/trend`

---

## 12.3 `.http` 文件测试

如果使用 VS Code + REST Client 插件，可在：

```text
tests/api_test.http
```

中编写请求进行测试。

---

## 13. 启动说明

## 13.1 安装依赖

```bash
pip install fastapi uvicorn openai python-dotenv requests
```

---

## 13.2 配置环境变量

项目根目录创建 `.env` 文件：

```env
OPENAI_API_KEY=你的OpenAI_API_Key
OPENAI_MODEL=gpt-5.4-mini
APP_NAME=Kidney Agent
```

---

## 13.3 启动服务

```bash
uvicorn app.main:app --reload
```

启动成功后访问：

```text
http://127.0.0.1:8000/docs
```

---

## 14. 当前项目亮点

这个项目的亮点主要在于：

### 14.1 规则引擎 + 大模型结合

不是纯 GPT 生成，而是先经过规则引擎判断，再交给 GPT 做语言解释。

这样有两个好处：

- 结果更稳定
- 更容易解释给面试官或业务方

---

### 14.2 结构化 + 自然语言双输出

系统既能输出结构化字段：

- 风险等级
- CKD 分期
- 异常项

也能输出自然语言说明：

- 中文总结
- 中文解释
- 建议项

---

### 14.3 医疗场景化

项目不只是普通聊天，而是具体到：

- 肾病指标分析
- 风险分层
- 随访趋势判断

更有行业场景感。

---

### 14.4 可扩展性强

当前虽然是原型，但后续非常容易继续扩展为正式系统，例如：

- 接数据库
- 接前端
- 接 RAG 医学知识库
- 支持批量分析
- 增加图表展示
- 接医生审核流程

---

## 15. 当前限制

目前项目仍是一个原型系统，存在以下限制：

### 15.1 历史记录为内存存储

服务一重启，历史数据就会丢失。

### 15.2 规则引擎仍是简化版

目前规则主要是演示级逻辑，还不是完整临床规则库。

### 15.3 未接入真实数据库

当前尚未实现 SQLite / MySQL / PostgreSQL 存储。

### 15.4 未接入知识库

当前 GPT 分析主要依赖 prompt 和规则结果，还未接入医学文献或权威指南知识库。

### 15.5 不具备临床诊断资格

本项目仅用于辅助分析和技术展示，不能替代医生判断。

---

## 16. 后续优化方向

后续建议优先做以下升级：

### 16.1 SQLite 数据库

把历史记录从内存存储升级为 SQLite，避免服务重启后数据丢失。

### 16.2 用户与患者管理

增加：

- 患者建档
- 患者列表
- 患者详情

### 16.3 批量导入分析

支持上传：

- CSV
- Excel

一次性分析多位患者。

### 16.4 前端页面

增加 Web 页面，用图表显示：

- Scr 趋势
- eGFR 趋势
- ACR 趋势

### 16.5 知识库增强

引入 CKD 指南、肾病文献或本地知识库，做更稳的医学解释。

### 16.6 更精细的指标体系

加入更多指标：

- BUN
- Cystatin C
- Albumin
- Hb
- K、Na、Ca、P
