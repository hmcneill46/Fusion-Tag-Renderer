import json
import re
from io import TextIOWrapper


def load_filters(request):
    file = request.files.get('filters')
    if file and file.filename:
        raw = file.read().decode('utf-8')
        name = file.filename
    else:
        raw = request.form.get('filters_data', '')
        name = request.form.get('filters-filename-hidden', '')
    # Ensure valid JSON
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {'filters': []}
    return raw, name


def compile_filters(raw_json):
    data = json.loads(raw_json)
    enabled = [f for f in data.get('filters', []) if f.get('isEnabled')]
    compiled = []
    for f in enabled:
        try:
            regex = re.compile(f['pattern'])
            compiled.append((f, regex))
        except re.error:
            continue
    # Preserve order
    order_map = {f['id']: idx for idx, f in enumerate(enabled)}
    return {'compiled': compiled, 'order_map': order_map}


def load_filenames(request):
    file_obj = request.files.get('filenames_file')
    if file_obj and file_obj.filename:
        wrapper = TextIOWrapper(file_obj.stream, encoding='utf-8')
        filenames = [line.strip() for line in wrapper if line.strip()]
        text = '\n'.join(filenames)
        name = file_obj.filename
    else:
        text = request.form.get('filenames_text', '')
        name = request.form.get('files_text', '')
        filenames = [line.strip() for line in text.splitlines() if line.strip()]

    # ─── remove duplicates (preserve original order) ───
    seen = set()
    unique = []
    for fn in filenames:
        if fn not in seen:
            seen.add(fn)
            unique.append(fn)
    filenames = unique
    text = '\n'.join(filenames)  # if you want the textarea to reflect the de-duped list

    return filenames, text, name



def tag_and_sort_files(filenames, filters):
    compiled = filters['compiled']
    order_map = filters['order_map']

    temp = []
    for idx, name in enumerate(filenames):
        matched = []
        indices = []
        for f, regex in compiled:
            if regex.search(name):
                indices.append(order_map.get(f['id'], float('inf')))
                matched.append({
                    'name': f['name'],
                    'imageURL': f.get('imageURL','').strip(),
                    'tagColor': f.get('tagColor','#333'),
                    'textColor': f.get('textColor','#fff')
                })
        indices.sort()
        temp.append((name, matched, indices, idx))

    max_len = max((len(t[2]) for t in temp), default=0)

    def sort_key(entry):
        _, _, indices, orig = entry
        padded = indices + [float('inf')] * (max_len - len(indices))
        return (*padded, orig)

    temp.sort(key=sort_key)
    return [{'name': t[0], 'tags': t[1]} for t in temp]