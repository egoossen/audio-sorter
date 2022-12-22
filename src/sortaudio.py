# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging, logging.config, json
import os, time, tinytag

def sort_dir(fpath=None):
    files = os.listdir(fpath)
    if fpath == None:
        logger.debug(f'Files in CWD: {files}')
        fpathdir = ''
    else:
        logger.debug(f'Files in {fpath}: {files}')
        fpathdir = f'{fpath}/'
    
    for fname in files:
        full_path = f'{fpathdir}{fname}'
        logger.debug(f'Current file: {full_path}')
        if os.path.isdir(full_path):
            logger.debug(f'Directory: {full_path}')
            sort_dir(full_path)
            if len(os.listdir(full_path)) == 0:
                os.rmdir(full_path)
                logger.info(f'Directory deleted: {full_path}')
                
        elif os.path.isfile(full_path):
            logger.debug(f'File: {full_path}')
            new_path = get_new_path(fpath,fname)
            if not new_path:
                continue
                
            new_fpath, new_fname = new_path
            
            if not os.path.isdir(new_fpath):
                os.mkdir(new_fpath)
                logger.info(f'Directory created: {new_fpath}')
            
            new_full_path = f'{new_fpath}/{new_fname}'
            
            if new_full_path == full_path:
                logger.debug(f'No Change: Skipping {full_path}')       
            elif os.path.isfile(f'{new_fpath}/{new_fname}'):
                logger.warning(f'File Exists ({new_fpath}/{new_fname}): Skipping {full_path}')
            else:
                os.rename(full_path, f'{new_fpath}/{new_fname}')
                logger.info(f'File renamed: {full_path} -> {new_fpath}/{new_fname}')
                
        else:            
            logger.error(f'Unknown: {str(fpath)}')

def get_new_path(old_path, old_file):
    if old_path == None:
        old_path = '.'
    
    file_name, file_extension = os.path.splitext(old_file)
    has_warning = False
    
    if file_extension in ['.jpg','.png']:
        logger.debug(f'Album Art: {file_name}{file_extension}')
        file_album = 'Album Art'
        new_file = old_file
        
    elif file_extension in ['.mp3','.m4a']:
        logger.debug(f'Audio File: {file_name}{file_extension}')
        
        try:
            tag = tinytag.TinyTag.get(f'{old_path}/{old_file}')

            if tag.album == None or tag.album == '':
                file_album = 'Unknown Album'
                logger.debug('Unknown Album!')
                has_warning = True
            else:
                file_album = ''.join(filter(lambda i: i.isalnum() or i in ' -_', str(tag.album)))

            if tag.track == None or tag.track == '0':
                file_track = 'XX'
                logger.debug('Unknown Track Number!')
                has_warning = True
            else:
                file_track = int(tag.track)

            if tag.title == None or tag.title == '':
                file_title = 'Unknown Track'
                logger.debug('Unknown Track!')
                has_warning = True
            else:
                file_title = ''.join(filter(lambda i: i.isalnum() or i in ' -_', str(tag.title)))

            new_file = f'{file_track:0>2} {file_title}{file_extension}'
        
        except BaseException as e:
            logger.info(str(e))
            logger.error(f'Error processing {old_file}. Saving in Errors.')
            file_album = 'Errors'
            new_file = old_file
    
    else:
        logger.error(f'Unrecognized file type: {file_extension}, Skipping {old_file}')
        return False
        
    new_path = f'{file_album}'
    
    if has_warning:
        logger.warning(f'Incomplete Metadata: Saving as {file_album}/{new_file}')
    
    return new_path, new_file

if __name__ == '__main__':
    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    with open(f'{dir_path}/cfglogging.json') as f:
        cfg = json.load(f)
        
    logging.config.dictConfig(cfg)
    logger = logging.getLogger('simplelogger')
    
    logger.info('%s: Sorting Audio...',time.strftime("%H:%M:%S",time.localtime()))
    print('Sorting Audio...')
    
    sort_dir()  
