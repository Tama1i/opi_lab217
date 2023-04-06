#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os.path
import click


@click.group()
def cli():
    pass


@cli.command(help="Add")
@click.option("-nm", "--name", required=True, help="Name worker's")
@click.option("-n", "--num", type=int, required=True, help="Number of the worker")
@click.option("-y", "--year", required=True, help="burthday worker")
@click.argument("filename")
def add(name, num, year, filename):
    pep = load_workers(filename)
    pep = add_wrk(pep, name, num, year)
    save_workers(filename, pep)


@cli.command(help="Display")
@click.argument("filename")
def display(filename):
    pep = load_workers(filename)
    li(pep)


@cli.command(help="Select")
@click.option("-s", "--select", help="The required select")
@click.argument("filename")
def select(select, filename):
    pep = load_workers(filename)
    select = sel(pep, select)
    li(select)


def add_wrk(pep, name, num, year):
    pep.append(
        {
            'name': name,
            'num': num,
            'year': year
        }
    )
    return pep


def li(pep):
     line = '+-{}-+-{}-+-{}-+-{}-+'.format(
                '-' * 4,
                '-' * 30,
                '-' * 20,
                '-' * 8
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


def sel(pep, numb):
    ot = []
    # Проверить сведения работников из списка.
    for chel in pep:
        if numb in str(chel.values()):
            ot.append(chel)
    return ot


def save_workers(file_name, staff):
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_workers(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8", errors="ignore") as fin:
            return json.load(fin)
    else:
        return []


if __name__ == '__main__':
    cli()
