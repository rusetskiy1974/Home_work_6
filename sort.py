import os
import sys
import re
from pathlib import Path
import shutil




search_folder_files = {'archives': ('ZIP', 'GZ', 'TAR'),
                         'video':('AVI', 'MP4', 'MOV', 'MKV'),
                           'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
                             'documents':('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
                               'images':('JPEG', 'PNG', 'JPG', 'SVG')}

search_files = {'archives': [],
                   'video':[],
                      'audio': [],
                         'documents':[],
                            'images':[]}
extension_files = set()
unknow_ext_files = set()




def obhod_folder_(path, level = 1):   # обход папок через модуль pathlib
    path = normalize(path, True)
    p = Path(path)
    print(p)
    movin_files(p)
    # if next(p.iterdir(), None) == None:
    #             p.rmdir()
    #             return
    
    
    for f in p.iterdir():
        print ('++', f)

        if f.is_dir() and  f.name not in search_folder_files.keys():
            
            # if  next(Path(path +'\\'+ f.name).iterdir(),None)  == None :
            #     Path(path +'\\'+ f.name).rmdir()
            #     continue
            # else:     
                # print ('Спускаемось',(path + '\\'+ f.name))
            obhod_folder_((path +'\\'+ f.name), level+1)
                # print ('Вертаємося в ', path)

def movin_files (folder_n):
    for f in folder_n.iterdir():
        if f.is_file():
            # print (f.name)
            mov_fil = select_folder(f.name)
            # print (mov_fil)
            f_name =  normalize(f.name)
            # print (f_name)
            new_way = search_path + '\\' + str(mov_fil) + '\\' + f_name
            # print ((new_way))
            # print(f_name)
            # mov_fil = select_folder(f_name)
            if mov_fil:
                if mov_fil != 'archives':
                      shutil.move(f, new_way) 
                else:
                    shutil.unpack_archive(f, new_way.rsplit('.')[-2])
                    Path(f).unlink()



 
def normalize(file_nam, fold = False):
    
    if fold:
        fold_name = file_nam.rsplit('\\', 1)[-1]
        fold_name = fold_name.translate(TRANS)
        fold_name = fold_name.replace(' ', '_')
        # fold_name  = ''.join(fold_name.split())
        fold_name = re.sub(r"\W+", r'_', fold_name) 
        new_fold_name = file_nam.rsplit('\\', 1)[-2] + '\\' + fold_name 
        print (type(new_fold_name))
        print (' -- ', new_fold_name)
        if file_nam == new_fold_name:
            return file_nam
        else:
             os.rename(file_nam, new_fold_name)
             return new_fold_name
         
    file_transl = file_nam.translate(TRANS)

    file_transl = file_transl.replace(' ', '_')
    # file_transl = ''.join(file_transl.split())

    fil_name = re.sub(r"\W+", r'_', file_transl[:file_transl.rfind('.')]) + '.' +  file_transl[file_transl.rfind('.')+1:]
    
    #fil_name = re.sub(r"\W+", r'_', file_transl.split('.',1)[-2])+'.'+ file_transl.split('.',1)[-1]

    return fil_name


def select_folder(file_name):
    file_type = file_name.rsplit('.')[-1]
     
    for key,value  in search_folder_files.items():
         
        if re.search(file_type, str(value), flags  = re.IGNORECASE):
            search_files[key].append(file_name)
            extension_files.add(file_type)
            return key 
    unknow_ext_files.add(file_type) 
    return '' 

def del_empty_fold(path):
    for f in os.listdir(path):
        # print (f)
        fo_n = os.path.join(path, f)
        if os.path.isdir(fo_n) and  f not in search_folder_files.keys():
             del_empty_fold(fo_n)
             if not os.listdir(fo_n):
                 os.rmdir(fo_n)
             
             



CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()



search_path = sys.argv[1] 

for key in search_folder_files:
     if  os.path.isdir(search_path + '\\' + key):
         continue
     else:
         os.mkdir(search_path+'\\'+ key)


if __name__ == '__main__':

    obhod_folder_(search_path)
    
    
    del_empty_fold(search_path)
    
    
    print('Списки знайдених  файлів :', '\n') 
    for value in search_files.items():
        print (value)
        
    
    print ('Include extension : ', extension_files)
    print ('Unknown extension : ', unknow_ext_files)






