[![中文](https://img.shields.io/badge/Language-%E4%B8%AD%E6%96%87-ff6b6b?style=for-the-badge)](./README.md)
[![English](https://img.shields.io/badge/Language-English-4c8bf5?style=for-the-badge)](./README.en.md)
[![Open Skill Spec](https://img.shields.io/badge/Page-Skill%20Spec-111111?style=for-the-badge)](./SKILL.md)

# 智慧议会

一个给 OpenClaw 使用的历史智慧决策 Skill。

很多问题不是缺信息，而是缺判断。

- 我该不该离婚
- 我该不该辞职创业
- 我的合伙人越来越不可靠
- 我知道该做什么，却一直拖延
- 我太在意别人的看法

这些问题往往没有标准答案，但又必须做决定。

`智慧议会` 的核心不是“列出十个人名”，也不是“拿一份共享模板给十个人套壳”。

它现在的主引擎是：

- 一份 100 位历史人物的专属 prompt 库
- 一个路由层，先判断用户问题属于什么分野
- 一个检索层，从 100 人里挑最贴题的 10 位
- 一个注入层，把用户困境塞进这 10 位人物各自的原 prompt
- 一个辩论与总结层，让他们先发言、再交锋、最后收敛成行动方案

## 怎么在 OpenClaw 里使用

这是一个给 OpenClaw 用的 Skill。最直接的用法，就是在 OpenClaw 对话里显式调用 `$wisdom-council`。

### 最小用法

```text
在 OpenClaw 里说：
用 $wisdom-council 帮我判断：我该不该辞职创业？
```

### 如果你想调试 100 人 prompt 库

```text
在 OpenClaw 里说：
用 $wisdom-council 分析：我应该怎么学英语？
请展示这次命中的人物、每个人对应的原 prompt 摘要、用户困境如何被注入，以及他们的圆桌辩论。
```

这里的关键是：

- 系统会优先调用你写好的原 prompt，而不是重新拼一份人格模板
- 普通模式下不会把整段内部 prompt 全吐出来
- 外部展示给用户的，是保留人物判断风格、但仍然能直接读懂的中文
- 如果结果读起来还像模板，说明路由或渲染失败，需要重写

### 更好的提问方式

如果你在 OpenClaw 里多给一点上下文，系统会更容易判题和选人。建议补充：

- 你现在在什么处境
- 你有哪些现实选项
- 你最担心失去什么
- 你最不能接受的结果是什么
- 这个决定的时间窗口有多长

## 输出结构

默认输出顺序是：

1. 十位人物发言
2. 圆桌辩论
3. 为什么是这十位
4. 行动方案

## 这版 Skill 的关键变化

- 现在是“100 位专属 prompt 库 + 动态路由 + 原 prompt 注入”，不是“1 个共享模板 + 10 个换名实例”
- 人物人格的源头，是用户写好的 prompt 正文
- 路由层只负责判题和选人，不负责重写人物
- 辩论和总结发生在人物发言之后
- 共享模板只保留为 fallback，不再覆盖已有的专属 prompt

## 文件结构

- [`SKILL.md`](./SKILL.md)：技能工作流程与操作规则
- [`references/persona_prompt_library_100.md`](./references/persona_prompt_library_100.md)：100 位人物的原始 prompt 库
- [`references/persona_prompt_index.json`](./references/persona_prompt_index.json)：供检索用的 prompt 索引
- [`scripts/persona_prompt_library.py`](./scripts/persona_prompt_library.py)：检索与提取原 prompt 的脚本
- [`references/taxonomy.json`](./references/taxonomy.json)：领域、冲突类型与规则
- [`references/router_prompt.md`](./references/router_prompt.md)：问题分类与选人逻辑
- [`references/renderer_prompt.md`](./references/renderer_prompt.md)：人物发言、辩论与总结逻辑
- [`references/eval_cases.json`](./references/eval_cases.json)：测试案例

## 边界

系统不会：

- 编造历史名言
- 把明显伤害关系包装成修复关系
- 把法律、医疗、税务或投资问题当作纯智慧问题
- 在人物已存在原 prompt 的情况下，偷偷改写成统一模板
- 以抽象鼓励作为结尾
