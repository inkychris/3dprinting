import argparse
import pathlib
import zipfile


script_dir = pathlib.Path(__file__).parent.resolve()
PROFILE_EXT = '.curaprofile'


def directory(path):
    path = pathlib.Path(path)
    if not path.is_dir():
        raise ValueError(f'path is not a directory: {path}')
    return path


def cura_profile(path):
    path = pathlib.Path(path)
    if not path.is_file():
        raise ValueError(f'path is not a file: {path}')
    if path.suffix != PROFILE_EXT:
        raise ValueError(f'expected file extension ".curaprofile", got {path.suffix}')
    return path


def pack_directory(path):
    filename = str(path) + PROFILE_EXT
    with zipfile.ZipFile(filename, 'w') as archive:
        for content in path.glob('**/*'):
            archive.write(content, content.name)
    print(filename)


def unpack_profile(path):
    extract_dir = script_dir / path.stem
    with zipfile.ZipFile(path, 'r') as archive:
        archive.extractall(extract_dir)
    print(extract_dir)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='commands', dest='command', required=True)

pack_parser = subparsers.add_parser('pack')
pack_parser.add_argument('directory', type=directory, help='profile directory')

unpack_parser = subparsers.add_parser('unpack')
unpack_parser.add_argument('cura_profile', type=cura_profile, help=f'cura config file ({PROFILE_EXT})')

args = parser.parse_args()
if args.command == 'pack':
    pack_directory(args.directory)
else:
    unpack_profile(args.cura_profile)
