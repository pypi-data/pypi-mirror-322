#!/usr/bin/env python3
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright © 2014, 2018, 2022 XCG Consulting
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import os
import os.path
import sys
from collections.abc import Mapping


def main():
    if len(sys.argv) != 4:
        print("usage: autotodo.py <folder> <exts> <tags>")
        sys.exit(1)

    folder = sys.argv[1]
    exts = sys.argv[2].split(",")
    tags = sys.argv[3].split(",")
    todolist = {tag: [] for tag in tags}
    path_file_length: Mapping[str, int] = {}

    for root, _dirs, files in os.walk(folder):
        scan_folder((exts, tags, todolist, path_file_length), root, files)
    create_autotodo(folder, todolist, path_file_length)


def write_info(f, infos, folder, path_file_length: Mapping[str, int]):
    # Check sphinx version for lineno-start support

    import sphinx

    if sphinx.version_info < (1, 3):
        lineno_start = False
    else:
        lineno_start = True

    for i in infos:
        path = i[0]
        line = i[1]
        lines = (line - 3, min(line + 4, path_file_length[path]))
        class_name = ":class:`%s`" % os.path.basename(os.path.splitext(path)[0])
        f.write(
            "%s\n"
            "%s\n\n"
            "Line %s\n"
            "\t.. literalinclude:: %s\n"
            "\t\t:language: python\n"
            "\t\t:lines: %s-%s\n"
            "\t\t:emphasize-lines: %s\n"
            % (
                class_name,
                "-" * len(class_name),
                line,
                path,
                lines[0],
                lines[1],
                4,
            )
        )
        if lineno_start:
            f.write("\t\t:lineno-start: %s\n" % lines[0])
        f.write("\n")


def create_autotodo(folder, todolist, path_file_length: Mapping[str, int]):
    with open("autotodo", "w+") as f:
        for tag, info in list(todolist.items()):
            f.write("%s\n%s\n\n" % (tag, "=" * len(tag)))
            write_info(f, info, folder, path_file_length)


def scan_folder(data_tuple, dirname, names):
    (exts, tags, res, path_file_length) = data_tuple
    for name in names:
        (root, ext) = os.path.splitext(name)
        if ext in exts:
            path = os.path.join(dirname, name)
            file_info, length = scan_file(path, tags)
            path_file_length[path] = length
            for tag, info in list(file_info.items()):
                if info:
                    res[tag].extend(info)


def scan_file(filename, tags) -> tuple[dict[str, list[tuple[str, int, str]]], int]:
    res: dict[str, list[tuple[str, int, str]]] = {tag: [] for tag in tags}
    line_num: int = 0
    with open(filename, "r") as f:
        for line_num, line in enumerate(f):
            for tag in tags:
                if tag in line:
                    res[tag].append((filename, line_num, line[:-1].strip()))
    return res, line_num


if __name__ == "__main__":
    main()
