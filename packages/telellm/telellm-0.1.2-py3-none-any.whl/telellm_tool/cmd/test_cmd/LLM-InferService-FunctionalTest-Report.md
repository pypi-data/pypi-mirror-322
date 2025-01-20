### 1. 测试描述

服务名称：{{ SERVICE_NAME }}推理服务。

模型名称：{{ MODEL_NAME }}

文档更新时间：{{ CURRENT_TIME }}


### 2. 常规问答测试

提供常见不同类型的问题进行提问，获取模型的输出内容。

{{ REGULAR_QA_RESULT }}


### 3. 错误码测试

提供了 error_case_list 错误样例、good_case_list 正确样例。其中 error_case_list 覆盖了 接口文档中提供的错误码。

样例测试结果：

> {{ ERROR_CODE_RESULT }}

