# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, logging, tinytag

def sort_dir(fpath):
    files = os.listdir(fpath)
    logging.debug(f'Files in {fpath}: {files}')
    
    for fname in files:
        full_path = f'{fpath}/{fname}'
        if os.path.isdir(full_path):
            logging.debug(f'Directory: {full_path}')
            sort_dir(full_path)
            if len(os.listdir(full_path)) == 0:
                os.rmdir(full_path)
                logging.info(f'Directory deleted: {full_path}')
                
        elif os.path.isfile(full_path):
            logging.debug(f'File: {full_path}')
            new_fpath, new_fname = get_new_path(fpath,fname)
            if not os.path.isdir(new_fpath):
                os.mkdir(new_fpath)
                logging.info(f'Directory created: {new_fpath}')
                
            os.rename(full_path, f'{new_fpath}/{new_fname}')
            logging.info(f'File renamed: {full_path} -> {new_fpath}/{new_fname}')
        else:            
            logging.warning(f'Unknown: {str(fpath)}')

def get_new_path(old_path, old_file):
    global CWD
    
    file_name, file_extension = os.path.splitext(old_file)
    
    if file_extension in ['.jpg','.png']:
        logging.debug(f'Album Art: {file_name}{file_extension}')
        file_album = 'Album Art'
        new_file = old_file
        
    if file_extension in ['.mp3','.m4a']:
        logging.debug(f'Audio File: {file_name}{file_extension}')
        tag = tinytag.TinyTag.get(f'{old_path}/{old_file}')
        file_album = ''.join(filter(lambda i: i.isalnum() or i in ' -_', str(tag.album)))
        file_track = int(tag.track)
        file_title = ''.join(filter(lambda i: i.isalnum() or i in ' -_', str(tag.title)))
        new_file = f'{file_track:0>2} {file_title}{file_extension}'
        
    new_path = f'{CWD}/{file_album}'
    return new_path, new_file

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print('Sorting Audio...')
    
    CWD = str(os.getcwd())
    CWD = str(os.getcwd()+'/test')
    logging.debug(f'CWD is {CWD}')
    
    sort_dir(CWD)