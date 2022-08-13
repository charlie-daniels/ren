from enum import Enum, auto
from os.path import getmtime, getsize, splitext
import glob
from os import rename

class SortingMethod(Enum):
    ALPHABETICAL = auto()
    CHRONOLOGICAL = auto()
    FILE_SIZE = auto()

def print_welcome_screen() -> None:
    print('Welcome to ren!')

def get_target_directory() -> str:
    '''Returns the directory the user wants to manipulate and confirms it with them.'''
    print('\nEnter directory: ',end='')
    current_directory = str(input())
    print('Confirm directory: ',end='')
    confirm_directory = str(input())
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
    print('\nSelect sorting method: ',end='')

    return SortingMethod(int(input()))

def handle_sort(target_directory: str, selected_sort: SortingMethod) -> list[str]: 
    '''Applies the selected SortingMethod to the files in a directory.'''
    file_type = '*.*'
    file_list = glob.glob(target_directory + file_type)

    if selected_sort == SortingMethod.ALPHABETICAL:
        return sorted(file_list)
    elif selected_sort == SortingMethod.CHRONOLOGICAL:     
        return sorted(file_list,key=getmtime)
    elif selected_sort == SortingMethod.FILE_SIZE:
        return sorted(file_list,key=getsize) # Returns largest last

def rename_file_list(target_directory: str, sorted_files: list[str], bulk_name: str) -> list[str]:
    '''Applies the set naming convention to a new list of filepaths.'''
    renamed_files = []
    for file_index, current_file in enumerate(sorted_files):
        _path, file_ext = splitext(current_file)
        new_file_name = f'{target_directory}{str(file_index).zfill(len(str(len(sorted_files))))}{bulk_name}{file_ext}'
        renamed_files.append(new_file_name)
        
    return renamed_files

def apply_rename(renamed_files: list[str], original_files: list[str]) -> None:
    for index, original in enumerate(original_files):
        current = renamed_files[index]
        rename(original, current)

def main():
    print_welcome_screen()
    
    target_directory = get_target_directory()
    selected_sort = get_sorting_method()

    sorted_files = handle_sort(target_directory,selected_sort)

    print('\nEnter name for all files: ', end='')
    bulk_name = input()
    renamed_files = rename_file_list(target_directory, sorted_files, bulk_name)
    apply_rename(renamed_files, sorted_files)
    print('Files renamed.')

if __name__ == '__main__':
    main()

