import json
import re
from io import TextIOWrapper


def load_filters(request):
    file = request.files.get('filters')
    if file and file.filename:
        raw = file.read().decode('utf-8')
        filename = file.filename
    else:
        raw = ''
        filename = ''
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {'filters': []}
    enabled = [f for f in data.get('filters', []) if f.get('isEnabled')]
    return filename, enabled


def load_filenames(request):
    file = request.files.get('filenames_file')
    if file and file.filename:
        wrapper = TextIOWrapper(file.stream, encoding='utf-8')
        names = [line.strip() for line in wrapper if line.strip()]
        filename = file.filename
    else:
        text = request.form.get('filenames_text', '')
        names = [line.strip() for line in text.splitlines() if line.strip()]
        filename = ''
    return filename, names


def match_and_sort(filters, filenames):
    # build regex list and order
    order = {f['id']: idx for idx, f in enumerate(filters)}
    compiled = []
    for f in filters:
        try:
            compiled.append((f, re.compile(f['pattern'])))
        except re.error:
            pass

    temp = []
    for idx, name in enumerate(filenames):
        matches = []
        best = float('inf')
        for f, regex in compiled:
            if regex.search(name):
                val = order.get(f['id'], float('inf'))
                best = min(best, val)
                matches.append({
                    'name': f['name'],
                    'imageURL': f.get('imageURL', '').strip(),
                    'tagColor': f.get('tagColor', '#333'),
                    'textColor': f.get('textColor', '#fff')
                })
        temp.append((name, matches, best, idx))
    temp.sort(key=lambda x: (x[2], x[3]))
    return [{'name': t[0], 'tags': t[1]} for t in temp]