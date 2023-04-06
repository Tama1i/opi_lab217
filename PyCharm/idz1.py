#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import argparse
import os.path


def add_wrk(pep,name,num,year):
    pep.append(
        {
            'name': name,
            'num': num,
            'year': year
        }
    )
    return pep


def display_wrk(pep):
    if pep:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 18
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
                "№",
                "F.I.O.",
                "NUMBER",
                "BRDAY"
            )
        )
        print(line)

        for idx, chel in enumerate(pep, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                    idx,
                    chel.get('name', ''),
                    chel.get('num', ''),
                    chel.get('year', 0)
                )
            )
            print(line)
    else:
        print('list empty')


def select_wrk(pep, n):
    result = []
    for chel in pep:
        if n in str(chel.values()):
            result.append(chel)
    return result


def save_wrk(file_name, pep):
    with open(file_name, "w", encoding="utf-8", errors="ignore") as fout:
        json.dump(pep, fout, ensure_ascii=False, indent=4)


def load_wrk(file_name):
    with open(file_name, "r", encoding="utf-8", errors="ignore") as fin:
        return json.load(fin)


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("pep")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления работника.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new worker"
    )
    add.add_argument(
        "-nm",
        "--name",
        action="store",
        required=True,
        help="The worker's name"
    )
    add.add_argument(
        "-n",
        "--num",
        action="store",
        type=int,
        required=True,
        help="Number of the worker"
    )
    add.add_argument(
        "-y",
        "--year",
        action="store",
        type=int,
        required=True,
        help="The date of worker's birth"
    )

    # Создать субпарсер для отображения всех работников.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all workers"
    )

    # Создать субпарсер для выбора работников.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the workers"
    )
    select.add_argument(
        "-s",
        "--select",
        action="store",
        required=True,
        help="The required select"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить всех работников из файла, если файл существует .
    is_dirty = False
    if os.path.exists(args.filename):
        pep = list(load_wrk(args.filename))
    else:
        pep = []


    # Добавить работника.
    if args.command == "add":
        pep = add_wrk(
            pep,
            args.name,
            args.num,
            args.year
        )
        is_dirty = True

    # Отобразить всех работников.
    elif args.command == "display":
        display_wrk(pep)

    # Выбрать требуемых рааботников.
    elif args.command == "select":
        selected = select_wrk(pep, args.select)
        display_wrk(selected)

    # Сохранить данные в файл, если список работников был изменен.
    if is_dirty:
        save_wrk(args.filename, pep)


if __name__ == '__main__':
    main()