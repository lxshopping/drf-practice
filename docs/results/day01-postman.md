# Day01 Postman 验证记录

- 日期：2026-07-24
- 分支：`practice/day01-finish`
- 最终 commit：
- 本地启动命令：`python manage.py runserver`

> 只填写真实执行结果。不要预先勾选，也不要粘贴大段响应；保留状态码、关键字段和错误即可。

| 场景 | 实际状态码 | 实际关键结果 | 是否通过 |
|---|---:|---|---|
| 合法生产发布单，app_code 首尾空格 + 大写 |  |  | [ ] |
| 输入 status=SUCCESS，保存后仍为 CREATED |  |  | [ ] |
| app_code 含内部空格 |  |  | [ ] |
| prod + feature/test |  |  | [ ] |
| prod + master |  |  | [ ] |
| test + feature/test |  |  | [ ] |
| GET 列表包含 status_display |  |  | [ ] |

## 静态检查

~~~text
python manage.py check：
python manage.py makemigrations --check --dry-run：
GitHub Check：
~~~

## 今天发现并修正的问题

1.
2.

## 两条源码结论

1. 只读 status 为什么不进入 validated_data：
2. status_display 为什么能出现在响应中：

## 仍未掌握

- 无则填写“无”；有则只写一个最具体的问题：
