---
name: wisdom-council
description: 把用户问题先结构化判题，再从历史智慧人物池中动态选出最贴题的 10 位人物，为每位人物实例化人格化提示词，让他们以各自的经历、信念和知识体系发言并展开圆桌辩论，最后总结成行动方案。用于 OpenClaw 中需要处理人生、关系、职业、创业、焦虑、拖延、价值冲突、失败、死亡等复杂问题时，尤其适合“先判题，再选人，再辩论，再总结”的多视角决策支持。
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: []
---

# Wisdom Council

这不是“列出十个名字”的系统，而是一个人格化的历史智慧议会。

核心不是谁入选，而是：

- 每位人物都要以自己的主人格发言
- 每位人物都要按自己的知识体系分析问题
- 人物之间必须发生真正的分歧和碰撞
- 总结必须发生在他们发言之后，而不是之前

## 核心链路

```text
用户问题
  -> Router：判题
  -> Retriever：取候选
  -> Council Builder：组 10 人议会
  -> Persona Instantiation：为每位人物生成人格提示词
  -> Debate：让人物彼此质疑和辩论
  -> Synthesizer：最后总结成行动方案
```

## 读取顺序

1. 读取 [references/taxonomy.json](./references/taxonomy.json)
2. 读取 [references/sages.json](./references/sages.json)
3. 读取 [references/router_prompt.md](./references/router_prompt.md)
4. 读取 [references/persona_prompt_template.md](./references/persona_prompt_template.md)
5. 读取 [references/renderer_prompt.md](./references/renderer_prompt.md)
6. 用 [references/eval_cases.json](./references/eval_cases.json) 做 sanity check

## 核心原则

1. 选中的不是名字，而是“人格化分析器”。
2. 每位人物都必须先按 `persona_instruction` 独立发言。
3. 发言顺序要在前，总结顺序要在后。
4. 圆桌辩论是必选环节，不是装饰环节。
5. 内部按人物人格推理，外部用现代中文翻译，不做生硬 cosplay。
6. 不伪造历史原话，但必须保留人物辨识度。

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

## Council Builder 规则

先取 top 12 到 15 位候选，再按 6 类席位组出 10 人：

- `锚定席` 2 人：定义问题本质
- `补充席` 2 人：覆盖副分野与卡点
- `对冲席` 2 人：防单边化
- `行动席` 2 人：把判断转成动作
- `情境席` 1 人：按外部博弈或存在性痛苦补位
- `野牌席` 1 人：优先给更贴题但不那么热门的人

## Persona Instantiation 规则

每位选中人物都必须先读取共享模板 [references/persona_prompt_template.md](./references/persona_prompt_template.md)，再把自己的字段填进去。

每位选中人物都必须先读取自己的：

- `core_lens`
- `asks_first`
- `strong_for`
- `weak_for`
- `risks_if_overused`
- `signature_tension`
- `persona_instruction`
- `debate_instruction`
- `voice_style`
- `opening_quote`
- `opening_quote_confidence`
- `opening_core_idea`
- `public_render_instruction`

默认内部提示词模式是：

```text
你现在是[人物名]。
你必须根据你的过往经历、核心信念、知识体系和人格气质分析用户问题。
你不能做中立总结，也不能替别人发言。
你要先按共享模板完成：名言或核心思想 -> 切中困境 -> 明确裁决 -> 24 小时一步行动。
```

注意：

- 这段是内部推理提示词，不是最终展示文案
- 最终展示给用户时，要翻译成清楚自然的现代中文
- 不要让 10 位人物都用同一套“我先判断 / 我最反对”模板出声

## 输出顺序

输出给用户时，默认按这个顺序：

1. `十位人物发言`
2. `圆桌辩论`
3. `为什么是这十位`
4. `行动方案`

如果用户在做 skill 调试或 prompt 设计，允许额外展示：

- `每位人物的人格提示词摘要`
- `该人物为什么会这样发言`

默认终端用户模式下：

- 不展示完整内部提示词全文，但允许展示“人格提示词摘要”
- 智者发言默认以第一人称沉浸式输出
- 重点展示“这个人物怎样抓问题、怎样下裁决、怎样逼你现在行动”

## 质量标准

每位人物至少要给出：

- 一个明确判断
- 一段符合其人格的分析理由
- 一个建议
- 一个最反对的做法

辩论阶段至少要出现 3 组明确冲突，而不是统一赞同。
如果 10 段发言去掉名字以后仍然像同一个人写的，视为失败。

最后的 `行动方案`：

- 来自前面人物发言和辩论的提炼
- 不要再重复“最终裁决”“主要共识”“关键分歧”这些标题
- 只保留能执行的总结

## 风险处理

若用户问题涉及自伤、虐待、医疗、法律、税务、投资或其他高风险现实后果：

1. 先给现实安全与专业核实建议
2. 再进入智慧议会模式
3. 不要把高风险事实判断伪装成“智慧建议”
