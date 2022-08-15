from dataclasses import dataclass
from enum import Enum, auto
from os.path import getmtime, getsize, splitext
import glob
from os import rename
from datetime import datetime

class SortingMethod(Enum):
    ALPHABETICAL = auto()
    CHRONOLOGICAL = auto()
    FILE_SIZE = auto()

@dataclass
class SortingOptions:
    reverse: bool = False
    add_date: bool = False
    file_ext: str = '*.*'

def print_welcome_screen() -> None:
    print('Welcome to ren!')

def get_target_directory() -> str:
    '''Returns the directory the user wants to manipulate and confirms it with them.'''
    current_directory = str(input('\nEnter directory: '))
    confirm_directory = str(input('Confirm directory: '))
    if (current_directory == confirm_directory):
        return current_directory
    else:
        print('\nDirectories did not match. Please reattempt.')
        return get_target_directory()

def get_sorting_method() -> SortingMethod:
    '''Returns the sorting method the user wants to use.'''
    print()
    for method in SortingMethod:
        print(f'{method.value}. {method.name}')

    return SortingMethod(int(input('\nSelect sorting method: ')))

def handle_sort(target_directory: str, method: SortingMethod, options: SortingOptions) -> list[str]: 
    '''Applies the selected SortingMethod to the selected file type in a directory.'''
    file_list = glob.glob(target_directory + options.file_ext)

    if method == SortingMethod.ALPHABETICAL:
        return sorted(file_list, reverse=options.reverse)
    elif method == SortingMethod.CHRONOLOGICAL:     
        return sorted(file_list, key=getmtime, reverse=options.reverse)
    elif method == SortingMethod.FILE_SIZE:
        return sorted(file_list, key=getsize, reverse=options.reverse) # Returns largest last

def rename_file_list(target_directory: str, sorted_files: list[str], bulk_name: str, add_date: bool) -> list[str]:
    '''Applies the set naming convention to a new list of filepaths.'''
    renamed_files = []
    for file_index, current_file in enumerate(sorted_files):
        _path, file_ext = splitext(current_file)
        # Add zero placeholders of length of list
        file_index_zfill = str(file_index).zfill(len(str(len(sorted_files))))     

        if add_date:
            current_date = datetime.today().strftime('%Y-%m-%d')
            new_file_name = f'{target_directory}{current_date}_{file_index_zfill}_{bulk_name}{file_ext}'
        else:
            new_file_name = f'{target_directory}{file_index_zfill}_{bulk_name}{file_ext}'
        renamed_files.append(new_file_name)
    return renamed_files

def apply_rename(original_files: list[str], renamed_files: list[str]) -> None:
    '''Applies rename to the first list of paths to the second.'''
    for index, original in enumerate(original_files):
        renamed = renamed_files[index]
        rename(original, renamed)
    return 

def get_sorting_options() -> SortingOptions:
    print('\nEnter 1 for true, 0 for false')

    reverse = bool(int(input('\nReverse order: ')))
    add_date = bool(int(input('\nUse date: ')))

    print('\nFor any file type, use .*')
    file_ext = input('Enter file type: ')
    file_ext = f'*{file_ext}'

    options = SortingOptions(reverse=reverse, add_date=add_date, file_ext=file_ext)

    return options

def main():
    print_welcome_screen()
    
    target_directory = get_target_directory()
    selected_sort = get_sorting_method()
    sorting_options = get_sorting_options()
    sorted_files = handle_sort(target_directory, selected_sort, sorting_options)

    bulk_name = input('\nEnter name for all files: ')
    renamed_files = rename_file_list(target_directory, sorted_files, bulk_name, sorting_options.add_date)
    apply_rename(sorted_files, renamed_files)
    print('Files renamed.')

if __name__ == '__main__':
    main()


