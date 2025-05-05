import json
from io import TextIOWrapper
from flask import Blueprint, request, render_template, flash
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
       # 1) Load filters JSON and filename, always
        filters_data_raw, context['filters_filename'] = load_filters(request)
        context['filters_data_raw'] = filters_data_raw
        # 2) Try to compile filters, possibly flash on error
        try:
            filters = compile_filters(filters_data_raw)
        except json.JSONDecodeError:
            filters = None
            flash('⚠️ Please upload a valid filters JSON before tagging.', 'error')
        
        # 3) Always load filenames so the textarea persists
        filenames, context['filenames_text'], context['filenames_file_name'] = load_filenames(request)

        # 4) Only do the tagging & sorting if filters parsed OK
        if filters:
            results_list = tag_and_sort_files(filenames, filters)

    return render_template('index.html', results_list=results_list, **context)