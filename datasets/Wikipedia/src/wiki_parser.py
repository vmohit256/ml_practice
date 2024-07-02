"""
Simple parser for wikipedia snapshot dump
"""

import bz2
import traceback
from tracemalloc import start
import mwxml
import pyperclip
import mwparserfromhell
import re
import time
import random
import json
import pandas as pd
import concurrent.futures
from io import BytesIO
import sys

# Increase the recursion limit to 4000
sys.setrecursionlimit(4000)

class BZ2FileSegmentReader:
    def __init__(self, file_reader, blocks, prefix_data=b'', suffix_data=b'</mediawiki>'):
        self.file_reader = file_reader
        self.current_byte_pos = 0
        self.blocks = sorted(blocks)
        self.next_block_idx = 0
        self.current_byte_stream = BytesIO(prefix_data)
        self.suffix_data = suffix_data

    def read(self, num_bytes) -> bytes:
        data = self.current_byte_stream.read(num_bytes)
        if len(data) < num_bytes:
            if self.next_block_idx < len(self.blocks):
                offset, block_size = self.blocks[self.next_block_idx]
                self.next_block_idx += 1
                if self.current_byte_pos != offset:
                    self.file_reader.seek(offset)
                self.current_byte_stream = BytesIO(bz2.decompress(self.file_reader.read(block_size)))
            else:
                self.current_byte_stream = BytesIO(self.suffix_data)
            return data + self.read(num_bytes - len(data))
        else:
            return data
    
    def close(self):
        pass

def parse_summary_from_raw_text(raw_wiki_article_text):
    page_dict = {}
    page_dict['categories'] = []
    page_dict['internal_links'] = []
    page_dict['text_length'] = 0
    page_dict['num_unique_words'] = 0
    page_dict['number_of_files'] = 0
    page_dict['number_of_external_links'] = 0
    page_dict['number_of_info_boxes'] = 0
    page_dict['number_of_sections'] = 0
    wikicode = mwparserfromhell.parse(raw_wiki_article_text)
    for link in wikicode.filter_wikilinks():
        if link.title.startswith('Category:'):
            page_dict['categories'].append(str(link.title)[9:])
        elif link.title.startswith('File:'):
            page_dict['number_of_files'] += 1
        elif not re.match(r'\w+:', str(link.title)):
            page_dict['internal_links'].append(str(link.title))
    page_dict['categories'] = list(set(page_dict['categories']))
    page_dict['internal_links'] = list(set(page_dict['internal_links']))
    tokens = wikicode.strip_code().replace('\n', '').split()
    page_dict['text_length'] = len(tokens)
    page_dict['num_unique_words'] = len(set(tokens))
    page_dict['number_of_external_links'] = len(list(wikicode.filter_external_links()))
    page_dict['number_of_info_boxes'] = len(list(wikicode.filter_templates(matches='Infobox')))
    page_dict['number_of_sections'] = len(list(wikicode.get_sections()))
    return page_dict

"""
This function reads wikipedia dump in blocks and parses the pages in each block.
It saves the parsed pages in a file named <output_dir>/part-<thread_id>.txt
This function is supposed to run inside a thread/process. 
"""
def parse_wikidump_blocks(args):
    start_time = time.time()
    blocks, thread_id, bz2_dump_path, output_dir, preamble_data, namespaces_to_include = args
    counts = {
        'thead_id': thread_id,
        'num_pages_seen': 0,
        'num_pages_saved': 0,
        'num_pages_failed_parsing': 0
    }
    with open(bz2_dump_path, 'rb') as f:
        with open(f"{output_dir}/part-{thread_id}.txt", 'w') as f_out:
            for page in mwxml.Dump.from_file(BZ2FileSegmentReader(f, blocks, prefix_data=preamble_data)):
                counts['num_pages_seen'] += 1
                if counts['num_pages_seen'] % 10000 == 0:
                    print(f"Thread {thread_id} processed {counts['num_pages_seen']} pages in {(time.time() - start_time) / 60} minutes")
                if page.namespace not in namespaces_to_include:
                    continue
                try:
                    page_dict = parse_summary_from_raw_text(next(page).text)
                    page_dict['page_id'] = page.id
                    page_dict['title'] = page.title
                    page_dict['redirect_title'] = page.redirect
                    page_dict['namespace'] = page.namespace
                    f_out.write(json.dumps(page_dict) + '\n')
                    counts['num_pages_saved'] += 1
                except Exception as e:
                    print(f"Error processing page: {page.title} inside thread {thread_id}")
                    traceback.print_exc()
                    counts['num_pages_failed_parsing'] += 1
    return counts

class WikiParser:
    """
    Parser for multistream wikipedia snapshot dump downloaded from here:
    https://dumps.wikimedia.org/enwiki/
    Pass paths to uncompressed .bz2 files for both index and dump.
    """
    def __init__(self, bz2_index_path, bz2_dump_path):
        self.bz2_index_path = bz2_index_path
        self.bz2_dump_path = bz2_dump_path
        self._load_index()

        with open(self.bz2_dump_path, 'rb') as f:
            self.preamble_data = bz2.decompress(f.read(self.min_offset))

    """WARNING: this will read the index and will take ~1 min
    """
    def _load_index(self):
        self.id_to_offset = {}
        with bz2.open(self.bz2_index_path, 'rt') as f:
            for line in f:
                line = line.strip()
                if line.startswith('SPECIAL:'):
                    continue
                parts = line.split(':')
                self.id_to_offset[int(parts[1])] = int(parts[0])
                # if len(self.id_to_offset) > 100000:
                #     break
        self.offset_to_next_offset = {}
        offsets = sorted(list(set([offset for offset in self.id_to_offset.values()])))
        for i in range(len(offsets)-1):
            self.offset_to_next_offset[offsets[i]] = offsets[i+1]
        
        self.min_offset = min([offset for offset in self.offset_to_next_offset])
        self.max_offset = max([offset for offset in self.id_to_offset.values()])

    """
    Obtains a sorted list of block offsets for the given set of page ids
    """
    def get_block_offsets(self, page_ids):
        page_ids = set(page_ids)
        offsets = sorted(list(set([self.id_to_offset[page_id] for page_id in page_ids])))
        blocks = [(offset, self.offset_to_next_offset.get(offset, offset + int(1e7)) - offset) for offset in offsets]
        return blocks

    """
    Fetches a given list of pages 
    Args:
        page_ids: set of page ids to fetch. WARNING: order of pages in the output is not guaranteed to be same as input
        include_text: whether to include the text of the page

    Returns:
        generator of page dictionaries with these keys:
            page_id
            title
            redirect_title
            namespace
            text (if include_text is True)
    """
    def page_stream(self, page_ids, include_text=True):
        page_ids = set(page_ids)
        blocks = self.get_block_offsets(page_ids)

        # read the blocks and parse the pages
        num_pages_seen = 0
        with open(self.bz2_dump_path, 'rb') as f:
            for page in mwxml.Dump.from_file(BZ2FileSegmentReader(f, blocks, prefix_data=self.preamble_data)):
                # print(page.id, page.title)
                if page.id in page_ids:
                    page_dict = {}
                    page_dict['page_id'] = page.id
                    page_dict['title'] = page.title
                    page_dict['redirect_title'] = page.redirect
                    page_dict['namespace'] = page.namespace
                    if include_text:
                        revision = next(page)
                        page_dict['text'] = revision.text
                    num_pages_seen += 1
                    yield page_dict
                if num_pages_seen == len(page_ids):
                    break                    

    """
    Scans the full dump and extract summary of each page. Scan is done parallely using multiple threads.
    Each thread stores the summaries in files like <outputdir>/<thread_id>.txt where each line is a json object.
    Args:
        output_dir: directory to store the output files
        fraction: fraction of blocks to scan. If None, scans all blocks. default is None.
        num_parallel_threads: number of parallel threads to use for scanning. default is 1.
        random_seed: random seed for shuffling the blocks. default is 1.
        block_selection_strategy: strategy to select blocks. Its either prefix or random. default is 'random'.
    Returns an iterator of dictionaries with these keys:
        page_id
        redirect_title: id of the page to which this page redirects. None if no redirect.
        title: title of the page
        categories: list of categories
        internal_links: list of page titles linked from this page
        text_length: length of the text
        num_unique_words: number of unique words in the text
        number_of_images: number of images
        number_of_references: number of references
        number_of_external_links: number of external links
        number_of_info_boxes: number of info boxes
        number_of_sections: number of sections
    """
    def dump_page_summary(self, 
                          output_dir, 
                          fraction=None, 
                          block_selection_strategy='random',
                          num_parallel_threads=1, 
                          namespaces_to_include=[0, 14],
                          random_seed=1):
        offsets = sorted(list(self.offset_to_next_offset.keys()))
        blocks = [(offset, self.offset_to_next_offset.get(offset, offset + int(1e7)) - offset) for offset in offsets]

        if fraction is not None:
            if block_selection_strategy == 'prefix':
                blocks = blocks[:int(fraction * len(blocks))]
            elif block_selection_strategy == 'random':
                random.seed(random_seed)
                random.shuffle(blocks)
                blocks = sorted(blocks[:int(fraction * len(blocks))])
            else:
                raise ValueError(f"Invalid block_selection_strategy: {block_selection_strategy}. Must be either prefix or random")

        # distribute the blocks to threads
        blocks_per_thread = len(blocks) // num_parallel_threads
        blocks_list = [blocks[i:i+blocks_per_thread] for i in range(0, len(blocks), blocks_per_thread)]
        if len(blocks_list) > num_parallel_threads:
            blocks_list[-2] += blocks_list[-1]
            blocks_list = blocks_list[:-1]

        # Create a ThreadPoolExecutor
        threadwise_status_counts = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_parallel_threads) as executor:
            # Start a new thread for each block
            futures = {executor.submit(parse_wikidump_blocks, 
                                       (blocks, i, self.bz2_dump_path, output_dir, self.preamble_data, namespaces_to_include)): i for i, blocks in enumerate(blocks_list)}

            for future in concurrent.futures.as_completed(futures):
                counts = future.result()
                threadwise_status_counts.append(counts)
                print(f"Thread {counts['thead_id']} completed. Pages seen: {counts['num_pages_seen']}, Pages saved: {counts['num_pages_saved']}, Pages failed parsing: {counts['num_pages_failed_parsing']}")
        return pd.DataFrame(threadwise_status_counts)

