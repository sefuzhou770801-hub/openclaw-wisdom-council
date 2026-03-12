---
name: wisdom-council
description: 先把用户问题结构化判题，再从 100 位用户自写的历史智者专属提示词中动态选出最贴题的 10 位，逐个注入用户困境并让他们各自发言、展开交锋，最后收束成自然结论与可执行方案。适用于 OpenClaw 中处理人生、关系、职业、创业、焦虑、拖延、价值冲突、失败、学习方法等复杂问题，尤其适合“先判题，再选人，再调用原 prompt，再交锋，再收束”的多视角决策支持。
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: []
---

# Wisdom Council

这不是“列出十个名字”的系统，而是一个调用 100 位专属 persona prompt 的历史智慧议会。

这里最重要的约束只有一条：

- 100 位智者的 prompt 正文是人格源，不要重写，不要改写，不要再用共享模板覆盖它们

系统要做的是：

- 先判题
- 再从 100 位人物里选人
- 再把用户问题注入对应人物的原 prompt
- 再让他们发言与交锋
- 最后才做自然收束与执行方案

## 核心链路

```text
用户问题
  -> Router：判题
  -> Prompt Search：从 100 位专属 prompt 里检索候选
  -> Council Builder：组 10 人议会
  -> Prompt Hydration：把 {{USER_DILEMMA}} 注入入选人物原 prompt
  -> Solo Statements：10 位人物逐个发言
  -> Debate：让人物彼此质疑和辩论
  -> Synthesizer：最后收束成自然结论与执行方案
```

## 读取顺序

1. 读取 [references/taxonomy.json](./references/taxonomy.json)
2. 读取 [references/persona_prompt_index.json](./references/persona_prompt_index.json)
3. 必要时读取 [references/persona_prompt_library_100.md](./references/persona_prompt_library_100.md)
4. 读取 [references/router_prompt.md](./references/router_prompt.md)
5. 读取 [references/renderer_prompt.md](./references/renderer_prompt.md)
6. 用 [references/eval_cases.json](./references/eval_cases.json) 做 sanity check
7. 只有在入选人物不在 100 人 prompt 库时，才回退读取 [references/sages.json](./references/sages.json) 和 [references/persona_prompt_template.md](./references/persona_prompt_template.md)

## Prompt Source Of Truth

对这 100 位人物：

- 人格源文件是 [references/persona_prompt_library_100.md](./references/persona_prompt_library_100.md)
- 检索索引是 [references/persona_prompt_index.json](./references/persona_prompt_index.json)
- 检索与提取工具是 [scripts/persona_prompt_library.py](./scripts/persona_prompt_library.py)

硬规则：

1. 不要修改 `persona_prompt_library_100.md` 里的 prompt 正文。
2. 不要把这些 prompt 再压缩回一份共享模板。
3. 对入选人物，只允许做两件事：
   - 选择它
   - 用用户困境替换 `{{USER_DILEMMA}}`
4. 若用户要求调试，允许展示“某位人物被注入后的 prompt”，但默认不要把整段内部 prompt 全部外显。

## Router 规则

内部先产出结构化判题结果：

```json
{
  "surface_topic": "",
  "primary_domain": "",
  "secondary_domains": [],
  "conflict_types": [],
  "emotional_state": [],
  "hidden_intent": "",
  "blocked_point": "",
  "decision_scene": "",
  "stake_level": "",
  "urgency": "",
  "life_stage": ""
}
```

优先按“当前最痛、最急、最卡”的层面定主分野。

然后把用户原话和判题结果压成一个检索串，去 100 人索引里找 top 12 到 15 位候选。

可直接调用：

```bash
python3 scripts/persona_prompt_library.py search \
  --index references/persona_prompt_index.json \
  --query "<用户原话 + 主分野 + 副分野 + 冲突 + 卡点>" \
  --top 15
```

## Council Builder 规则

先取 top 12 到 15 位候选，再按 6 类席位组出 10 人：

- `锚定席` 2 人：定义问题本质
- `补充席` 2 人：覆盖副分野与卡点
- `对冲席` 2 人：防单边化
- `行动席` 2 人：把判断转成动作
- `情境席` 1 人：按外部博弈或存在性痛苦补位
- `野牌席` 1 人：优先给更贴题但不那么热门的人

只要 100 人 prompt 库里有该人物，就优先使用那里的 prompt，不要再从别处拼人格。

## Prompt Hydration 规则

选出 10 位以后，必须提取他们的原 prompt，并把用户问题注入 `{{USER_DILEMMA}}`。

可直接调用：

```bash
python3 scripts/persona_prompt_library.py extract \
  --source references/persona_prompt_library_100.md \
  --names "孔子,王阳明,庄子" \
  --user-dilemma "<用户原话>"
```

如果用户只写简称，例如“费曼”，脚本会自动尽量解析到唯一全名。

## 发言与交锋规则

1. 10 位人物完整发言必须在前。
2. 每位人物的单独发言，都来自该人物自己的原 prompt。
3. 发言之后可以展示几组明确交锋，但不要写成小说式串场。
4. 最后的综合结论，来自前面人物发言和交锋的提炼。
5. 不要在发言前先把答案总结掉。
6. 默认不要在用户可见输出里打出 `圆桌辩论`、`为什么是这十位`、`行动方案` 这些标题。
7. 每位人物名字下可以补一句极短人物简介，但不要写成 `个人简介：` 这种标签。
8. 若人物没有把握使用真实原话，就直接写出其核心判断，不要显式写 `我的核心思想是`。
9. 若人物要下结论，直接下结论，不要显式写 `我的裁决是`。
10. 若人物要给立刻行动，不要写 `24小时之内`，改成自然说法，例如 `今天就...`、`现在先去...`。
11. 若展示人物分歧，要直接写观点冲突本身，不要写 `说到这里，这桌人吵开了`、`谁冷冷坐在旁边` 这类戏剧化过场。

## 共享模板的地位

[references/persona_prompt_template.md](./references/persona_prompt_template.md) 不是这 100 位人物的默认人格源。

它现在只用于：

- 未来新增人物但还没有专属 prompt 时的 fallback
- 内部实验或扩充人物池时的临时模板

不要拿它覆盖用户已经写好的 100 条专属 prompt。

## 默认用户可见结构

默认用户可见结构只有三层：

1. 逐位智者发言
2. 发言之后的自然交锋
3. 最后一段综合结论与执行方案

若用户明确要求调试，再额外展示选人依据或 prompt 摘要。

## 质量标准

每位人物至少要给出：

- 一个明确判断
- 一段符合其人格的分析理由
- 一个建议
- 一个最反对的做法

如果 10 段发言去掉名字以后仍然像同一个人写的，视为失败。
如果某位人物明明在 100 人 prompt 库里，却仍然被共享模板重写，视为失败。
如果输出里满是 `个人简介`、`我的核心思想是`、`我的裁决是`、`24小时之内` 这类提示词标签，也视为失败。

## 风险处理

若用户问题涉及自伤、虐待、医疗、法律、税务、投资或其他高风险现实后果：

1. 先给现实安全与专业核实建议
2. 再进入智慧议会模式
3. 不要把高风险事实判断伪装成“智慧建议”
