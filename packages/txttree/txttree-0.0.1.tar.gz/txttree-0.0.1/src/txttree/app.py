"""
Entrypoint of the `typer` app.
See the documentation in the `help` sections of every parameter for more information, or run ``python -m asdfuzz --help``.
"""
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union, Dict

import typer

_TXT_EXTENSION = '.txt'
_JUNCTION = '├─ '
_STRAIGHT = '│  '
_STRAIGHT_SMALL = '│ '
_CORNER = '└─ '
_SPACES = '   '
# date format is one of 3 formats:
#     yymmdd
#     yyyymmdd
#     yyyy-mm-dd
SHORT_DATE_FORMAT = r'%y%m%d'
LONG_DATE_FORMAT = r'%Y%m%d'
ISO_DATE_FORMAT = r'%Y-%m-%d'

app = typer.Typer()


@dataclass
class Property:
    value: str
    date: Optional[datetime] = None


@dataclass
class File:
    path: Path
    symbols: List[str]
    is_last: bool
    print_own_name: bool = True
    # printing own name is not necessary for folder text files
    current_date: datetime = None

    def __post_init__(self):
        self.name = self.path.absolute().name

        # regex is 1-3 words, followed by a colon, followed by a value
        property_regex = r'\A(?P<key>[^: ]+( [^: ]+){0,2}): (?P<value>.+)\Z'
        self.properties: Dict[str, Property] = {}

        with open(self.path, 'r') as f:
            for line in f:
                text_line = line.strip('\r\n')
                property_match = re.match(
                    pattern=property_regex,
                    string=text_line,
                )
                if property_match:
                    self.properties[property_match.group('key')] = Property(
                        value=property_match.group('value'),
                        date=self.current_date,
                    )
                    continue

                try:
                    date_can_be_updated = datetime.strptime(
                        text_line,
                        SHORT_DATE_FORMAT,
                    )
                    self.current_date = date_can_be_updated
                    continue
                except:  # noqa
                    pass
                try:
                    date_can_be_updated = datetime.strptime(
                        text_line,
                        LONG_DATE_FORMAT,
                    )
                    self.current_date = date_can_be_updated
                    continue
                except:  # noqa
                    pass
                try:
                    date_can_be_updated = datetime.strptime(
                        text_line,
                        ISO_DATE_FORMAT,
                    )
                    self.current_date = date_can_be_updated
                    continue
                except:  # noqa
                    pass

    def write_output(self):
        prefix = "".join(_title_symbol(self.symbols, self.is_last))
        if self.print_own_name:
            typer.echo(prefix + typer.style(
                self.name[:-len(_TXT_EXTENSION)],
                bold=True
            ))
        for key, prop in self.properties.items():
            prefix = "".join(self.symbols + [_STRAIGHT_SMALL])
            text_to_print = prefix + key + ': ' + prop.value
            if self.current_date:
                text_to_print += '   (' + prop.date.strftime(
                    ISO_DATE_FORMAT
                ) + ')'
            typer.echo(text_to_print)


@dataclass
class Directory:
    path: Path
    symbols: List[str]
    is_last: bool

    def __post_init__(self):
        self.name: str = self.path.absolute().name
        self._recurse_into_files_and_directories()

    def _recurse_into_files_and_directories(self):
        folder_text_file_name = self.name + _TXT_EXTENSION
        folder_text_file = self.path / folder_text_file_name

        # determine files and directories that belong to this directory first,
        # so that we know the last element before the recursion
        text_file_paths = sorted(
            [
                item for item in self.path.iterdir()
                if item.is_file()
                and item.name.endswith(_TXT_EXTENSION)
                and item.name != folder_text_file_name
            ],
            key=lambda item: item.name
        )
        subdirectory_paths = sorted(
            [
                item for item in self.path.iterdir()
                if item.is_dir()
            ],
            key=lambda item: item.name
        )

        # recurse into files and directories
        self.text_files: List[File] = [
            File(
                path=text_file_path,
                symbols=_add_symbol(
                    symbols=self.symbols,
                    is_last=(
                        text_file_path == text_file_paths[-1]
                        and not subdirectory_paths
                    )  # a text file can be last if there are no subdirectories
                ),
                is_last=(
                    text_file_path == text_file_paths[-1]
                    and not subdirectory_paths
                )  # a text file can be last if there are no subdirectories
            )
            for text_file_path in text_file_paths
        ]
        self.subdirectories: List[Directory] = [
            Directory(
                path=subdirectory_path,
                symbols=_add_symbol(
                    symbols=self.symbols,
                    is_last=(subdirectory_path == subdirectory_paths[-1])
                ),
                is_last=(subdirectory_path == subdirectory_paths[-1]),
            ) for subdirectory_path in subdirectory_paths
        ]

        # set up the text file belonging to the folder to parse tags
        self.folder_text_file: Optional[File] = None
        if Path(folder_text_file).exists():
            self.folder_text_file = File(
                path=folder_text_file,
                symbols=self.symbols,
                is_last=False,  # does not matter
                print_own_name=False,
            )

    def write_output(self):
        prefix = "".join(_title_symbol(self.symbols, self.is_last))
        typer.echo(prefix+typer.style(self.name, bold=True))
        if self.folder_text_file:
            self.folder_text_file.write_output()
        for file_object in self.text_files:
            file_object.write_output()
        for directory in self.subdirectories:
            directory.write_output()


def main(
        root_directory_path: Path = typer.Argument(
            ..., help='Root directory for the hierarchy.',
        ),
):
    root_directory = Directory(
        path=root_directory_path,
        symbols=[],
        is_last=True,
    )
    root_directory.write_output()


def _add_symbol(
        symbols: List[str],
        is_last: bool,
):
    """ Add spaces for the last element, and a straight piece otherwise. """
    if is_last:
        return symbols + [_SPACES]

    return symbols + [_STRAIGHT]


def _title_symbol(
        symbols: List[str],
        is_last: bool,
):
    """ Make a corner for the last element, and a 3-way junction otherwise. """
    if not symbols:
        return []
    if not is_last:
        return symbols[:-1] + [_JUNCTION]
    return symbols[:-1] + [_CORNER]  # last element
