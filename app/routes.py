import json
from io import TextIOWrapper
from flask import Blueprint, request, render_template
from .utils import (
    load_filters,
    load_filenames,
    compile_filters,
    tag_and_sort_files
)

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    results_list = None
    context = {
        'filenames_text': '',
        'filters_data_raw': '',
        'filters_filename': '',
        'filenames_file_name': ''
    }

    if request.method == 'POST':
        # Load filters
        filters_data_raw, context['filters_filename'] = load_filters(request)
        context['filters_data_raw'] = filters_data_raw
        filters = compile_filters(filters_data_raw)

        # Load filenames
        filenames, context['filenames_text'], context['filenames_file_name'] = load_filenames(request)

        # Tag and sort
        results_list = tag_and_sort_files(filenames, filters)

    return render_template('index.html', results_list=results_list, **context)