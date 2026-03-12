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

`智慧议会` 的核心不是“列出十个人名”，而是：

让十位历史人物以自己的主人格和知识体系发言，再让他们辩论，最后才总结出行动方案。

## 怎么在 OpenClaw 里使用

这是一个给 OpenClaw 用的 Skill。最直接的用法，就是在 OpenClaw 对话里显式调用 `$wisdom-council`。

### 最小用法

```text
在 OpenClaw 里说：
用 $wisdom-council 帮我判断：我该不该辞职创业？
```

### 如果你想调试人物提示词

```text
在 OpenClaw 里说：
用 $wisdom-council 分析：怎么提升自己的工作效率。
请展示每位入选人物的人格提示词摘要、各自发言，以及他们的圆桌辩论。
```

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

- 不再把人物当成“视角标签”
- 每位人物都有自己的 `persona_instruction`
- 每位人物都要先独立发言
- 发言之后必须进入辩论
- 最后只保留一个行动方案总结

## 文件结构

- [`SKILL.md`](./SKILL.md)：技能工作流程与操作规则
- [`references/sages.json`](./references/sages.json)：结构化智者池与人格提示词
- [`references/taxonomy.json`](./references/taxonomy.json)：领域、冲突类型与规则
- [`references/router_prompt.md`](./references/router_prompt.md)：问题分类逻辑
- [`references/renderer_prompt.md`](./references/renderer_prompt.md)：人格发言、辩论与总结逻辑
- [`references/eval_cases.json`](./references/eval_cases.json)：测试案例

## 边界

系统不会：

- 编造历史名言
- 把明显伤害关系包装成修复关系
- 把法律、医疗、税务或投资问题当作纯智慧问题
- 以抽象鼓励作为结尾
