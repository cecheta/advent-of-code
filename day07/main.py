from typing import Optional


class File:
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size


class Directory:
    root: 'Directory'

    def __init__(self, name: str = '/', parent: Optional['Directory'] = None) -> None:
        self.name = name
        self.parent = parent

        # dict where each key is the file name and each value is the file
        self.files: dict[str, File] = {}
 
        # dict where each key is the direcotory name and each value is directory
        self.directories: dict[str, Directory] = {}

        if name == '/':
            Directory.root = self

    def add_file(self, name: str, size: int) -> File:
        file = File(name, size)

        # Add the file into the dict
        self.files[name] = file

        return file

    def change_directory(self, name: str) -> 'Directory':
        if name == '/':
            return Directory.root

        if name == '..':
            parent = self.parent

            if parent is None:
                raise Exception('Root directory does not have parent')

            return parent

        # Use the directory name to find and return the directory
        return self.directories[name]

    def make_directory(self, name: str) -> 'Directory':
        directory = Directory(name, self)

        # Add the directory into the dict
        self.directories[name] = directory

        return directory


def create_tree(commands: list[str]) -> Directory:
    # Create the root directory, which is where to start
    root = curr_dir = Directory()

    for command in commands:
        if command.startswith('cd'):
            # Extract the directory name
            dir = command.split(' ')[1]

            curr_dir = curr_dir.change_directory(dir)
        elif command.startswith('ls'):
            # Extract the contents of the directory, ignoring the first line (which contains `ls`)
            contents = command.splitlines()[1:]

            for content in contents:
                key, value = content.split(' ')

                if key == 'dir':
                    # value - the name of the directory
                    curr_dir.make_directory(value)
                else:
                    # key - the size of the file
                    # value - the name of the file
                    curr_dir.add_file(value, int(key))
        else:
            raise Exception('Invalid command')

    return root


def part_one(input: str):
    # Obtain a list of commands by removing the first '$ ', then
    # split at each '\n$ ' to obtain the full list
    input = input[2:]
    commands = input.split('\n$ ')

    # Root directory
    root = create_tree(commands)

    total = 0
    LIMIT = 100000

    # Recursive function which calculates the size of a directory from the size of its
    # files and sub-directories, and adds the size to `total` if it is smaller than `LIMIT`
    def calculate_sizes(dir: Directory) -> int:
        nonlocal total
        size = 0

        for file in dir.files.values():
            size += file.size

        for child_dir in dir.directories.values():
            size += calculate_sizes(child_dir)

        if size <= LIMIT:
            total += size

        return size

    calculate_sizes(root)

    print(total)


def part_two(input: str):
    # Obtain a list of commands by removing the first '$ ', then
    # split at each '\n$ ' to obtain the full list
    input = input[2:]
    commands = input.split('\n$ ')

    # Root directory
    root = create_tree(commands)

    TOTAL_SPACE = 70000000
    REQUIRED_SPACE = 30000000

    # list to keep track of the sizes of each directory
    sizes: list[int] = []

    # Recursive function which calculates the size of a directory from the size of its
    # files and sub-directories, and adds the size to the `sizes` list
    def calculate_sizes(dir: Directory) -> int:
        size = 0

        for file in dir.files.values():
            size += file.size

        for child_dir in dir.directories.values():
            size += calculate_sizes(child_dir)

        sizes.append(size)

        return size

    root_size = calculate_sizes(root)

    free_space = TOTAL_SPACE - root_size

    # Sort the directory sizes, smallest first
    sizes.sort()

    result = -1

    for dir_size in sizes:
        if free_space + dir_size >= REQUIRED_SPACE:
            # Deleting this directory will gives us enough free space
            result = dir_size
            break

    print(result)


with open('input.txt') as f:
    input = f.read()

part_one(input)
part_two(input)
