# encodint:utf8

import click
import os
import re
import datetime


def is_keep(file_name: str, daykeep: int) -> bool:
    '''
    check the daykeep rule
    '''
    ret = re.search(r"([ios_|android_]_\d{4})", file_name)
    if not ret:
        return True
    day: str = ret.group().split("_")[-1]
    f_data = datetime.datetime(2023, int(day[:2]), int(day[2:]))
    cur_data = datetime.datetime.now()
    if abs((cur_data - f_data).days) > daykeep:
        return False
    return True


def iter_chk(file_path: str, daykeep: int) -> bool:
    '''
    handle the match action
    '''
    file_name = file_path.split(os.sep)[-1]
    if not is_keep(file_name, daykeep):
        print("to remove filename->", file_name)
        # os.remove(file_path)


@click.command()
@click.option("--re", help="python re match str fmt", default=r"(_\d{4})")
@click.option("--daykeep", help="file keep day count", default=3)
@click.option("--path", help="path to execute check-keep&delete", default=os.curdir)
def run(path, daykeep: int):
    print("start run file auto del...")
    try:
        for root, _,  files in os.walk(path):
            for f in files:
                iter_chk(os.path.join(root, f), daykeep)
    except:
        print("raise error!")
    print("done!")


if __name__ == "__main__":
    run()
