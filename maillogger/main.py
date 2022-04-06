from maillogger.cli import parse_options
from maillogger.file.loader import Loader
from maillogger.file.writer import write
from maillogger.parser import parse


def main() -> None:
    options = parse_options()

    loader = Loader(options.source_file)
    contents = loader.handle()

    parse_to = True
    parse_from = True
    if options.fmt in ("csv", "tsv"):
        parse_from = False

    parsed_contents = []
    for c in contents:
        result = parse(c, parse_to, parse_from)
        if result:
            parsed_contents.append(result)

    write(
        filepath=options.target_file, records=parsed_contents,
        fmt=options.fmt, compress=options.compress)


if __name__ == '__main__':
    main()
