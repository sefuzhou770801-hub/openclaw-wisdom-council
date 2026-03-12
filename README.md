[![中文](https://img.shields.io/badge/Language-%E4%B8%AD%E6%96%87-ff6b6b?style=for-the-badge)](./README.md)
[![English](https://img.shields.io/badge/Language-English-4c8bf5?style=for-the-badge)](./README.en.md)
[![Open Skill Spec](https://img.shields.io/badge/Page-Skill%20Spec-111111?style=for-the-badge)](./SKILL.md)

# 智慧议会

针对真实用户困境的历史智慧决策系统。

很多问题不是缺信息，而是缺判断。

- 我该不该离婚
- 我该不该辞职创业
- 我的合伙人越来越不可靠
- 我知道该做什么，却一直拖延
- 我太在意别人的看法

`智慧议会` 不是“十个古人轮流说话”的角色扮演，而是一个帮助人做决定的思考系统。

它会把用户问题变成决策结构，再动态选择最合适的十种历史智慧视角，让它们围绕同一个问题产生分歧，最后收敛成一个明确判断和可执行的行动方案。

## Workflow

```text
User Question
  -> Router
  -> Retriever
  -> Council Builder
  -> Renderer
  -> Synthesizer
  -> Quality Checker
  -> Final Decision
```

## 用户会得到什么

- 问题重述
- 为什么选择这十个视角
- 十个不同判断角度
- 主要共识
- 关键分歧
- 最终裁决
- 24 小时行动
- 7 天行动计划

## 边界

- 不编造历史名言
- 不把明显伤害关系包装成修复关系
- 不把法律、医疗、税务或投资问题当作纯智慧问题
- 不以抽象鼓励作为结尾

## 文件结构

- [`SKILL.md`](./SKILL.md)
- [`references/sages.json`](./references/sages.json)
- [`references/taxonomy.json`](./references/taxonomy.json)
- [`references/router_prompt.md`](./references/router_prompt.md)
- [`references/renderer_prompt.md`](./references/renderer_prompt.md)
- [`references/eval_cases.json`](./references/eval_cases.json)

一句话理解：

把一个人的困境，变成一场真正的思想碰撞，最后收敛成一个可以执行的决定。
