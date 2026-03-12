#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List

HEADING_RE = re.compile(r'^##\s+(\d+)\.\s+(.+?)\s*$', re.M)
BLOCK_RE = re.compile(r'^##\s+(\d+)\.\s+(.+?)\s*\n\n```text\n(.*?)\n```\s*', re.M | re.S)
CHINESE_OR_WORD_RE = re.compile(r'[\u4e00-\u9fff]+|[A-Za-z0-9]+')


def parse_library(text: str) -> List[Dict[str, str]]:
    entries: List[Dict[str, str]] = []
    for match in BLOCK_RE.finditer(text):
        idx, name, prompt = match.groups()
        profile = extract_profile_block(prompt)
        entries.append(
            {
                'id': idx,
                'name': name.strip(),
                'prompt_template': prompt.strip(),
                'profile': profile,
                'strengths': extract_field(prompt, '最擅长处理'),
                'approach': extract_field(prompt, '你面对来访者时的基调：'),
                'voice': extract_field(prompt, '你的个人语气：'),
                'imagery': extract_field(prompt, '画面与意象尽量贴近'),
                'last_action_hint': extract_last_action(prompt),
                'searchable_text': build_searchable_text(name.strip(), prompt),
            }
        )
    return entries


def extract_field(prompt: str, marker: str) -> str:
    pattern = re.compile(rf'-\s*{re.escape(marker)}\s*(.+)')
    m = pattern.search(prompt)
    return m.group(1).strip() if m else ''


def extract_last_action(prompt: str) -> str:
    lines = [line.strip()[2:].strip() for line in prompt.splitlines() if line.strip().startswith('- 最后一步')]
    return ' '.join(lines)


def extract_profile_block(prompt: str) -> str:
    m = re.search(r'身份底色：\n(.*?)\n\n用户当前困境：', prompt, re.S)
    if not m:
        return ''
    lines = []
    for raw_line in m.group(1).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith('- '):
            line = line[2:].strip()
        lines.append(line)
    return ' '.join(lines)


def build_searchable_text(name: str, prompt: str) -> str:
    profile = extract_profile_block(prompt)
    parts = [name]
    if profile:
        parts.append(profile)
    last_action = extract_last_action(prompt)
    if last_action:
        parts.append(last_action)
    strengths = extract_field(prompt, '最擅长处理')
    if strengths:
        parts.append(strengths)
    return '\n'.join(parts)


def tokenize(text: str) -> List[str]:
    tokens: List[str] = []
    for part in CHINESE_OR_WORD_RE.findall(text.lower()):
        if re.fullmatch(r'[a-z0-9]+', part):
            tokens.append(part)
            continue
        if len(part) == 1:
            tokens.append(part)
            continue
        tokens.append(part)
        for i in range(len(part) - 1):
            tokens.append(part[i:i + 2])
    return tokens


def build_doc_stats(entries: List[Dict[str, str]]):
    doc_freq: Counter[str] = Counter()
    doc_tokens: Dict[str, Counter[str]] = {}
    doc_lengths: Dict[str, int] = {}
    for entry in entries:
        key = entry['name']
        counts = Counter(tokenize(entry['searchable_text']))
        doc_tokens[key] = counts
        doc_lengths[key] = sum(counts.values())
        for token in counts:
            doc_freq[token] += 1
    avg_len = (sum(doc_lengths.values()) / len(doc_lengths)) if entries else 0.0
    return doc_tokens, doc_lengths, doc_freq, avg_len


def bm25_score(query: str, entry: Dict[str, str], doc_tokens, doc_lengths, doc_freq, avg_len) -> float:
    q_tokens = tokenize(query)
    if not q_tokens:
        return 0.0
    counts = doc_tokens[entry['name']]
    score = 0.0
    total_docs = max(len(doc_tokens), 1)
    dl = max(doc_lengths[entry['name']], 1)
    for token in q_tokens:
        tf = counts.get(token, 0)
        if tf == 0:
            continue
        df = doc_freq.get(token, 0)
        idf = math.log(1 + (total_docs - df + 0.5) / (df + 0.5))
        numerator = tf * (1.2 + 1)
        denominator = tf + 1.2 * (1 - 0.75 + 0.75 * dl / (avg_len or 1.0))
        score += idf * (numerator / denominator)
    if entry['name'] in query:
        score += 8.0
    return score


def cmd_build_index(args: argparse.Namespace) -> int:
    source = Path(args.source)
    output = Path(args.output)
    entries = parse_library(source.read_text())
    payload = {
        'source_file': str(source),
        'entry_count': len(entries),
        'entries': [
            {
                'id': e['id'],
                'name': e['name'],
                'profile': e['profile'],
                'strengths': e['strengths'],
                'approach': e['approach'],
                'voice': e['voice'],
                'imagery': e['imagery'],
                'last_action_hint': e['last_action_hint'],
                'searchable_text': e['searchable_text'],
            }
            for e in entries
        ],
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'ok': True, 'source': str(source), 'output': str(output), 'entry_count': len(entries)}, ensure_ascii=False))
    return 0


def load_entries(source: Path | None, index: Path | None) -> List[Dict[str, str]]:
    if source:
        return parse_library(source.read_text())
    if index:
        payload = json.loads(index.read_text())
        return payload['entries']
    raise ValueError('source or index is required')


def cmd_search(args: argparse.Namespace) -> int:
    source = Path(args.source) if args.source else None
    index = Path(args.index) if args.index else None
    entries = load_entries(source, index)
    doc_tokens, doc_lengths, doc_freq, avg_len = build_doc_stats(entries)
    results = []
    for entry in entries:
        score = bm25_score(args.query, entry, doc_tokens, doc_lengths, doc_freq, avg_len)
        if score <= 0:
            continue
        results.append(
            {
                'id': entry['id'],
                'name': entry['name'],
                'score': round(score, 4),
                'strengths': entry.get('strengths', ''),
                'approach': entry.get('approach', ''),
                'voice': entry.get('voice', ''),
                'last_action_hint': entry.get('last_action_hint', ''),
            }
        )
    results.sort(key=lambda item: item['score'], reverse=True)
    print(json.dumps({'query': args.query, 'results': results[: args.top]}, ensure_ascii=False, indent=2))
    return 0


def canonicalize_name(value: str) -> str:
    return re.sub(r'[\s·\-_.]+', '', value).lower()


def resolve_entry(entries: List[Dict[str, str]], wanted_name: str) -> Dict[str, str] | None:
    exact = next((entry for entry in entries if entry['name'] == wanted_name), None)
    if exact:
        return exact

    wanted_canon = canonicalize_name(wanted_name)
    canon_matches = [entry for entry in entries if canonicalize_name(entry['name']) == wanted_canon]
    if len(canon_matches) == 1:
        return canon_matches[0]

    contains_matches = [
        entry for entry in entries
        if wanted_name in entry['name']
        or entry['name'] in wanted_name
        or wanted_canon in canonicalize_name(entry['name'])
        or canonicalize_name(entry['name']) in wanted_canon
    ]
    if len(contains_matches) == 1:
        return contains_matches[0]

    return None


def cmd_extract(args: argparse.Namespace) -> int:
    source = Path(args.source)
    entries = parse_library(source.read_text())
    wanted = [name.strip() for name in args.names.split(',') if name.strip()]
    output = []
    for name in wanted:
        entry = resolve_entry(entries, name)
        if not entry:
            output.append({'name': name, 'found': False})
            continue
        prompt = entry['prompt_template']
        if args.user_dilemma is not None:
            prompt = prompt.replace('{{USER_DILEMMA}}', args.user_dilemma)
        output.append({'name': name, 'resolved_name': entry['name'], 'found': True, 'prompt': prompt})
    print(json.dumps({'source': str(source), 'results': output}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Index, search, and extract immutable persona prompts.')
    sub = parser.add_subparsers(dest='command', required=True)

    build = sub.add_parser('build-index')
    build.add_argument('--source', required=True)
    build.add_argument('--output', required=True)
    build.set_defaults(func=cmd_build_index)

    search = sub.add_parser('search')
    search.add_argument('--query', required=True)
    search.add_argument('--top', type=int, default=15)
    search.add_argument('--source')
    search.add_argument('--index')
    search.set_defaults(func=cmd_search)

    extract = sub.add_parser('extract')
    extract.add_argument('--source', required=True)
    extract.add_argument('--names', required=True, help='Comma-separated sage names')
    extract.add_argument('--user-dilemma')
    extract.set_defaults(func=cmd_extract)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
