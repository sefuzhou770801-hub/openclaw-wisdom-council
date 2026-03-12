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
- 一个独立调用层，让这 10 位人物分别单独生成
- 一个单独总结层，在第 11 次调用里收束成方案

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
请展示这次命中的人物、每个人对应的原 prompt 摘要、独立调用 runbook，以及用户困境如何被注入。
```

这里的关键是：

- 系统会优先调用你写好的原 prompt，而不是重新拼一份人格模板
- 10 位智者必须 10 次独立调用，不允许同轮合写
- 总结必须单独再跑一次，不能和人物正文混在一起
- 普通模式下不会把整段内部 prompt 全吐出来

## 输出结构

默认输出顺序是：

1. 十位人物发言
2. 综合结论与执行方案

## 这版 Skill 的关键变化

- 现在是“100 位专属 prompt 库 + 动态路由 + 原 prompt 注入 + 10 次独立调用 + 1 次独立总结”
- 人物人格的源头，是用户写好的 prompt 正文
- 路由层只负责判题和选人，不负责重写人物
- 默认不再强调人物之间的分歧，而是强调独立人格发言后的互补
- 共享模板只保留为 fallback，不再覆盖已有的专属 prompt

## 文件结构

- [`SKILL.md`](./SKILL.md)：技能工作流程与操作规则
- [`references/persona_prompt_library_100.md`](./references/persona_prompt_library_100.md)：100 位人物的原始 prompt 库
- [`references/persona_prompt_index.json`](./references/persona_prompt_index.json)：供检索用的 prompt 索引
- [`scripts/persona_prompt_library.py`](./scripts/persona_prompt_library.py)：检索与提取原 prompt 的脚本
- [`scripts/build_independent_council_runbook.py`](./scripts/build_independent_council_runbook.py)：生成 10 次独立调用 + 1 次总结调用的 runbook
- [`references/synthesis_prompt.md`](./references/synthesis_prompt.md)：单独总结调用使用的提示词
- [`references/taxonomy.json`](./references/taxonomy.json)：领域、冲突类型与规则
- [`references/router_prompt.md`](./references/router_prompt.md)：问题分类与选人逻辑
- [`references/renderer_prompt.md`](./references/renderer_prompt.md)：独立人物发言与收束逻辑
- [`references/eval_cases.json`](./references/eval_cases.json)：测试案例

## 边界

系统不会：

- 编造历史名言
- 把明显伤害关系包装成修复关系
- 把法律、医疗、税务或投资问题当作纯智慧问题
- 在人物已存在原 prompt 的情况下，偷偷改写成统一模板
- 把 10 位人物塞进同一次调用里合写
- 以抽象鼓励作为结尾
