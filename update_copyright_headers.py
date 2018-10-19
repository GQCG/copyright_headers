import os
import glob
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('header_path', metavar='H', type=str, help="The path to the file that contains the copyright header to be included in the source code files.")
parser.add_argument('root_path', metavar='R', type=str, help="The path to the root of the project directory that contains the source code files.")
arguments = parser.parse_args()


def prepend_code(text, prepending_characters):
    """Prepend and :return :param text (a string of source code) with :param prepending_characters
    at the beginning of a new line.

    This function is used to insert commenting characters in front of a block of text.
    """
    text = prepending_characters + text  # prepend the first line
    text = text.replace('\n', '\n' + prepending_characters)  # prepend the other lines
    return text


# Find the relevant files and directories
root_path = os.path.abspath(arguments.root_path)

include_directory_path = os.path.join(root_path, 'include')
header_files = glob.glob(include_directory_path + "/**/*.hpp", recursive=True)
header_files.extend(glob.glob(include_directory_path + "/**/*.in", recursive=True))

src_directory_path = os.path.join(root_path, 'src')
source_files = glob.glob(src_directory_path + "/**/*.cpp", recursive=True)

exe_directory_path = os.path.join(root_path, 'exe')
executable_files = glob.glob(exe_directory_path + "/**/*.cpp", recursive=True)

tests_directory_path = os.path.join(root_path, 'tests')
executable_files = glob.glob(tests_directory_path + "/**/*.cpp", recursive=True)


# Add or update the header in every header (.hpp) or source file (.cpp)
with open(arguments.header_path, 'r') as f_header:
    header_text = f_header.read()  # read in the whole header
    header_text_commented = prepend_code(header_text, '// ')  # '//' for comments in C++
    header_text_commented += '\n'  # we need an extra (non-commented) newline at the end

    for filename in (header_files + source_files + executable_files):

        with open(filename, 'r') as f_original:
            original_source_code = f_original.read()  # read the whole source code

        # Add the header in the case that the copyright header isn't included yet
        if original_source_code[0] == '#':
            file_is_raw = True
        elif original_source_code[0] == '/':
            file_is_raw = False
        else:
            raise ValueError("{filename} has an unexpected character {character} at position 0".
                             format(filename=filename, character=original_source_code[0]))

        with open(filename, 'w') as f_modified:
            if file_is_raw:  # needs 'adding' of the copyright header
                    f_modified.write(header_text_commented + original_source_code)

            else:  # needs 'updating' of the copyright header
                # Splitting at the first occurrence splits off the copyright header, but we'll have
                # to add the '#' again later
                original_source_code_without_copyright = original_source_code.split('#', 1)[1]

                f_modified.write(header_text_commented + '#'
                                 + original_source_code_without_copyright)
