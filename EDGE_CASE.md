# Edge Case: 成绩超出有效范围

## 识别的边界情况

当通过 `POST /students` 创建学生或 `PUT /students/<id>` 更新学生时，如果提供的 `mark` 值不是 0 到 100 之间的整数（例如 -5、150、或浮点数 85.5），系统应该拒绝该请求。

## 处理方式

在 `create_student` 和 `update_student` 两个接口中，对 `mark` 字段进行了以下验证：

```python
if not isinstance(mark, int) or mark < 0 or mark > 100:
    return jsonify({"error": "Mark must be an integer between 0 and 100"}), 404
```

如果 `mark` 不满足条件，返回 404 错误和描述性错误信息，不会写入数据库。

## 原因

成绩系统中分数通常有明确的上下限（0-100），允许超出范围的分数写入数据库会导致数据不一致，影响 `/stats` 接口计算出的统计数据（如平均分、最大值等）的准确性。通过在写入前验证，可以保证数据库中的数据始终合法。
