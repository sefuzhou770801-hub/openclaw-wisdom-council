#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from persona_prompt_library import parse_library, resolve_entry


def build_runbook(source: Path, synthesis_ref: Path, names: List[str], user_dilemma: str) -> Dict[str, Any]:
    entries = parse_library(source.read_text())
    council = []
    for order, raw_name in enumerate(names, start=1):
        name = raw_name.strip()
        if not name:
            continue
        entry = resolve_entry(entries, name)
        if not entry:
            council.append(
                {
                    'order': order,
                    'requested_name': name,
                    'found': False,
                }
            )
            continue
        prompt = entry['prompt_template'].replace('{{USER_DILEMMA}}', user_dilemma)
        council.append(
            {
                'order': order,
                'requested_name': name,
                'resolved_name': entry['name'],
                'found': True,
                'independent_call_required': True,
                'prompt': prompt,
            }
        )

    return {
        'user_dilemma': user_dilemma,
        'prompt_source': str(source),
        'independent_call_contract': {
            'required': True,
            'rule': 'Each sage must be run in a separate generation pass. Do not ask one model response to play multiple sages at once.',
            'synthesis_must_be_separate': True,
        },
        'council': council,
        'synthesis': {
            'required': True,
            'run_after_all_sages_complete': True,
            'prompt_reference': str(synthesis_ref),
            'prompt': synthesis_ref.read_text(),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description='Build a runbook for 10 independent sage calls plus a separate synthesis pass.')
    parser.add_argument('--source', required=True, help='Path to persona_prompt_library_100.md')
    parser.add_argument('--names', required=True, help='Comma-separated sage names')
    parser.add_argument('--user-dilemma', required=True, help='User dilemma to inject into the prompts')
    parser.add_argument('--synthesis-reference', required=True, help='Path to synthesis_prompt.md')
    parser.add_argument('--output', help='Optional JSON output path')
    args = parser.parse_args()

    runbook = build_runbook(
        source=Path(args.source),
        synthesis_ref=Path(args.synthesis_reference),
        names=[part for part in args.names.split(',')],
        user_dilemma=args.user_dilemma,
    )

    payload = json.dumps(runbook, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(payload + '\n')
    print(payload)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
