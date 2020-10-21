import os
import re
import shutil
import signal
import subprocess
from typing import List, Iterable

from .config import huey

from collections import namedtuple

FileTextReplacement = namedtuple("FileTextReplacement", ["pattern", "replacement"])


@huey.task()
def unzip(filename, dest=None, delete=False):
    root, basename = os.path.split(filename)
    root = dest if dest else root
    if root:
        args = ["7z", "-y", "x", filename, "-o" + root]
    else:
        args = ["7z", "-y", "x", filename]
    p = subprocess.Popen(args)
    result = None
    try:
        result = p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGKILL)
        print("\naborted.")

    if delete:
        os.unlink(filename)

    return result


@huey.task()
def rmrf(path):
    return subprocess.run(["rm", "-rf", path])


@huey.task()
def replace(path, patterns: Iterable[FileTextReplacement]):
    with open(path, "r") as fp:
        string = fp.read()
        for op in patterns:
            string = re.sub(op.pattern, op.replacement, string)
    with open(path, "w") as fp:
        fp.write(string)


@huey.task()
def copyfile(src, dst):
    shutil.copyfile(src, dst)


@huey.task()
def verify_samba_configuarion():
    pass