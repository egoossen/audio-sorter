# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, tinytag, logging

def fmt_dir(path):
    global PATH
    
    files = os.listdir(path)
    logging.debug(f'Files in directory: {files}')

    for i in range(len(files)):
        fpath = path+files[i]
        logging.debug(f'Current file name: {fpath}')

        if os.path.isdir(fpath):
            logging.debug(f'Entering directory {fpath}')
            fmt_dir(f'{fpath}/')
        else:
            file_name, file_extension = os.path.splitext(files[i])

            if file_extension == '.jpg':
                logging.debug(f'Album Art detected: {files[i]}')
                par_dir = 'Album Art/'
                file_name = files[i]
            else:
                try:
                    tag = tinytag.TinyTag.get(fpath)
                    file_album = ''.join(filter(lambda i: i.isalnum() or i in ' -_',str(tag.album)))
                    file_track = f'{str(tag.track):0>2}'
                    file_title = ''.join(filter(lambda i: i.isalnum() or i in ' -_',str(tag.title)))

                    par_dir = f'{file_album}/'
                    file_name = f'{file_track:0>2} {file_title}{file_extension}'
                except BaseException as e:
                    logging.warning(str(e)+f'({files[i]})')
                    continue

            try:
                os.mkdir(PATH+par_dir)
                logging.info(f'Directory {par_dir} created')
            except FileExistsError as e:
                logging.info(str(e)+' Directory not created.')                      
            try:
                new_fpath = PATH+par_dir+file_name
                os.rename(fpath,new_fpath)
                logging.info(f'File {new_fpath} moved successfully.')
            except FileExistsError as e:
                logging.info(str(e)+'File not moved.')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    PATH = './'
    fmt_dir(f'{PATH}')