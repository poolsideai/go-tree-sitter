#!/usr/bin/env python3

import datetime
import os
import shutil

lang_dirs = [
    'ada',
    'c',
    'lua',
    'csharp',
    'cpp',
    'elixir',
    'elm',
    'golang',
    'java',
    'javascript',
    'ocaml',
    'objc',
    'php',
    'python',
    'ruby',
    'rust',
    # typescript has a slightly different directory structure. Right now it works without fixing up headers. 
    #'typescript', 
    'kotlin',
    'scala',
    'zig'
]


file_map = { 
  'alloc.h': 'ocaml/alloc.h'
}

# flatten a directory
def flatten_dir(root):
    print(f'Flattening {root}')
    for dir, _, filenames in os.walk(root):
        if dir == root:
            continue
        for filename in filenames:
            src = os.path.join(dir, filename)
            dst = os.path.join(root, filename)
            force_move_file(src, dst)

# list files in directory (not including its subdirs) that ends with any of the given extensions
def ls_exts(directory, extensions):
    files = os.listdir(directory)
    return [os.path.join(directory, file) for file in files 
            if os.path.isfile(os.path.join(directory, file)) and endswith_any(file, extensions)]


# fix_headers assumes some pre-processing is already done. Then it changes:
# #include "../bar.h"
# #include "./bar.h"
# #include "foo/bar.h"
# all into #include "bar.h"
def fix_headers(file_path):
    print(f'Fixing headers in {os.path.abspath(file_path)}')
    file_dir = os.path.dirname(os.path.abspath(file_path))
    with open(file_path, 'r') as file:
        content = file.read()
    new_content = []
    needs_write = False
    for line in content.split('\n'):
        if not line.startswith('#include') or line.count('"') == 0:
            new_content.append(line)
            continue
        header = line.split('"')[1]
        idx = header.find('/')
        if idx == -1:
            new_content.append(line)
            continue
        needs_write = True
        if header.startswith('../'):
            copy_recur(os.path.join(file_dir, header), file_dir)
            line = line.replace('../', '')
        elif header.startswith('./'):
            line = line.replace('./', '')
        else:
            # this is a big assumption: That is the header it tries to include here is in a subdir we already flattened
            base = os.path.basename(header)
            line = f'#include "{base}"'
        line += ' // modified by Poolside fork'
        new_content.append(line)
    if needs_write:
        with open(file_path, 'w') as file:
            file.write('\n'.join(new_content))

def add_extra_line(file_path, extra_line):
    with open(file_path, 'r') as file:
        content = file.read()
    with open(file_path, 'w') as file:
        file.write(extra_line + content + extra_line)

# generate a comment header/footer to make it clear a file is modified by us, not directly from upstream
def make_comments():
    comment_line = '////////////////////////////////////////////////////////////////////////////////\n'
    return f'\n\n{comment_line}// Poolside modification in the fork, generated at {datetime.datetime.now()} //\n{comment_line}\n\n'


# move file from src to dst if src exists, overwrite dst if it exists.
def force_move_file(src, dst):
    # if src no longer exists, we proabably done moving it already. Abort:
    if not os.path.exists(src):
        print(f'File {src} no longer exists, not going to move anything.')
        return
    # if dst exists, we want to overwrite it
    if os.path.exists(dst):
        print(f'Warning: removing existing file {dst}')
        os.remove(dst)
    os.rename(src, dst)
    add_extra_line(dst, make_comments())
    print(f'File {src} has been moved to {dst}.')


def endswith_any(filename, extenstions):
    return any(filename.endswith(extension) for extension in extenstions)


def op_recur(src, dst_dir, operation):
    headers = []
    with open(src, 'r') as f:
        for lines in f:
            if lines.startswith('#include') and lines.count('"') > 0:
                headers.append(lines.split('"')[1])
    for h in headers:
        op_recur(h, dst_dir, operation)
    operation(src, os.path.join(dst_dir)) 


def copy_with_extra_commends(src, dst):
    if os.path.basename(src) in file_map.keys():
        src = file_map[os.path.basename(src)]
    shutil.copy2(src, dst)
    add_extra_line(os.path.join(dst, os.path.basename(src)), make_comments())

def copy_recur(src, dst_dir):
    op_recur(src, dst_dir, copy_with_extra_commends)
    print(f'File {src} has been copied to {dst_dir}.')


# (1) Fix up go-tree-sitter root level headers so they do not have #include "./foo.h"
# (2) Flatten a list of language subdirs that we care about. No more go-tree-sitter/{lang}/foo/bar.h
# (3) Then in these flatten subdirs, fix up any header inclusion that isn't directly a sibling file.
if __name__ == '__main__':
    root_dir_headers = ls_exts(os.getcwd(), ['.h'])
    for h in root_dir_headers:
        fix_headers(h)
    for dir in lang_dirs:
        flatten_dir(dir)
        for f in ls_exts(dir, ['.h', '.c']):
            fix_headers(f)
