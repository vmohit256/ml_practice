"""
This file contains utility functions for analyzing Wikipedia snapshot data.
"""

import time, traceback, json, random

def normalized_page_name(page_name):
    return page_name.lower().split('#')[0]

"""
Loads the page name to page id mapping from the page_info.tsv file in the data_root_dir.
"""
def load_page_name_to_id_map(data_root_dir, log_level='ERROR', silent=False):
    page_name_to_page_id = {}
    page_id_to_page_name = {}
    fail_count, success_count = 0, 0
    error_counts = {}
    start_time = time.time()
    with open(data_root_dir + 'page_info.tsv', 'r') as f:
        line_no = 0
        for line in f:
            line_no += 1
            if line_no==1: continue
            try:
                page_name, _, page_id = line.split('\t')[:3]
                page_id = int(page_id)
                page_name = normalized_page_name(page_name)
            except:
                if log_level in ['WARN', 'INFO'] and not silent:
                    print(f"Unable to parse this weird line: \"{line}\"")
                fail_count += 1
                error_details = traceback.format_exc()
                error_counts[error_details] = error_counts.get(error_details, 0) + 1
                continue
            page_name_to_page_id[page_name] = page_id
            page_id_to_page_name[page_id] = page_name
            success_count += 1
            total_count = fail_count + success_count
            if total_count % 1000000 == 0 and not silent:
                print(f"Processed {total_count} lines. Fail count: {fail_count}. Success count: {success_count}. Time taken: {(time.time() - start_time) / 60} minutes.")

    if not silent:
        print(f"Failed to parse {fail_count} / {fail_count + success_count} ({(fail_count / (fail_count + success_count)) * 100}%) lines.")
    
    return page_name_to_page_id, page_id_to_page_name, error_counts

"""
load source_page_id to destination_page_id for redirect pages
this is used to resolve redirects in various places
"""
def load_page_redirect_mapping(data_root_dir, page_name_to_page_id, log_level='ERROR', silent=False):
    source_page_id_to_destination_page_id = {}
    fail_count, success_count = 0, 0
    log_level = 'ERROR'
    error_counts = {}
    start_time = time.time()
    with open(data_root_dir + 'page_info.tsv', 'r') as f:
        line_no = 0
        for line in f:
            line_no += 1
            if line_no==1: continue
            try:
                page_name, redirect_title, page_id = line.split('\t')[:3]
                page_id = int(page_id)
                if redirect_title:
                    source_page_id_to_destination_page_id[page_id] = page_name_to_page_id[normalized_page_name(redirect_title)]
            except:
                if log_level in ['WARN', 'INFO']:
                    print(f"Unable to parse this weird line: \"{line}\"")
                fail_count += 1
                error_details = line + "\n\n\n" + traceback.format_exc()
                error_counts[error_details] = error_counts.get(error_details, 0) + 1
                continue
            success_count += 1
            total_count = fail_count + success_count
            if total_count % 1000000 == 0 and not silent:
                print(f"Processed {total_count} lines. Fail count: {fail_count}. Success count: {success_count}. Time taken: {(time.time() - start_time) / 60} minutes.")
    return source_page_id_to_destination_page_id, error_counts


"""
Loads sample category pages for sanity checks
"""
def load_category_pages(data_root_dir, selected_categories=set(), probability_of_selection=0.00001, silent=False):
    category_pages = {
        'selected': [],
        'random': []
    }
    norm = normalized_page_name
    selected_categories = set([norm(category) for category in selected_categories])

    start_time = time.time()
    for partition in range(10):
        with open(data_root_dir + f'category_pages/part-{partition}.txt', 'r') as f:
            for line in f:
                if line=='': continue
                data = json.loads(line)
                if norm(data['category_name']) in selected_categories:
                    category_pages['selected'].append(data)
                if random.random() < probability_of_selection:
                    category_pages['random'].append(data)
        if not silent:
            print(f"Processed till part {partition} in {(time.time() - start_time) / 60} minutes")
    return category_pages

"""
Loads category name to id mappings
"""
def load_category_name_to_id_map(data_root_dir, silent=False):
    categories = {
        'id_to_name': {},
        'name_to_id': {}
    }
    failure_counts = {
        'MissingCategoryId': 0
    }
    start_time = time.time()
    success_count = 0
    for partition in range(10):
        with open(data_root_dir + f'category_pages/part-{partition}.txt', 'r') as f:
            for line in f:
                if line=='': continue
                data = json.loads(line)
                if 'category_id' not in data:
                    failure_counts['MissingCategoryId'] += 1
                    continue
                categories['id_to_name'][int(data['category_id'])] = data['category_name']
                categories['name_to_id'][data['category_name']] = int(data['category_id'])
                success_count += 1
        if not silent:
            print(f"Processed till part {partition} in {(time.time() - start_time) / 60} minutes")

    if not silent:
        print (success_count, failure_counts)
        print (len(categories['id_to_name']), len(categories['name_to_id']))
    return categories, failure_counts
