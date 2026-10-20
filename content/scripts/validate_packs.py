import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
errors = []
for path in sorted((ROOT / 'packs').glob('*.json')):
    data = json.loads(path.read_text())
    ids = set()
    for question in data.get('questions', []):
        if question['id'] in ids: errors.append(f'{path}: duplicate question id {question["id"]}')
        ids.add(question['id'])
        if not question.get('explanation', {}).get('english', {}).get('short'): errors.append(f'{path}: missing English explanation')
        if not question.get('explanation', {}).get('pidgin', {}).get('short'): errors.append(f'{path}: missing Pidgin explanation')
        if question['answer'] >= len(question['options']): errors.append(f'{path}: answer out of range for {question["id"]}')
print(f'Validated {len(list((ROOT / "packs").glob("*.json")))} pack files')
if errors:
    raise SystemExit('\n'.join(errors))
