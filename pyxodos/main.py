# main.py
import os
import zipfile
from collections import defaultdict

from .tasks import unzip, FileTextReplacement, replace, copyfile
from .config import huey


def ini():
    pass


"""
[Main]
Width=1280
Height=740
UFEPath=%REPLACE%\
BGColor=clGray
LastSelectedGame=0
RememberLastSelected=1
[Fields]
Number=
Name=
Folder=
Subfolder=
Genre=
SubGenre=
SubGenre2=
Publisher=
Developer=
Year=
Executable=
DBConf/ScummID=
Emulator=
Setup=
Front01=
Back01=
Media01=
Title01=
Screen01=
Manual=
Platform=
Designer=
Designer2=
Series=
Series2=
Extra1=
ExtraLink1=
Extra2=
ExtraLink2=
Extra3=
ExtraLink3=
Extra4=
ExtraLink4=
Extra5=
ExtraLink5=
About=
[Subfolders]
!win3x=
!dos=
"""


class DB:
    def __init__(self, path):
        self.path = path

    @staticmethod
    def filename_db(path):
        pass


class ZipFiles(DB):
    def filename_db(self):
        zip = zipfile.ZipFile(self.path)
        filenames = defaultdict(set)
        for path in zip.namelist():
            if path.endswith("conf"):
                root, filename = os.path.split(path)
                filenames[filename].add(path)
        return filenames


class FileSystemFiles(DB):
    def filename_db(self):
        filenames = defaultdict(set)
        for root, dirs, files in os.walk(self.path):
            for filename in files:
                if filename.endswith("conf"):
                    path = os.path.join(root, filename)
                    filenames[filename].add(path)
        return filenames


class DOSBoxManager:
    dbcp = {
        "fullscreen": ["true", "false"],
        "aspect": ["true", "false"],
        "output": ["overlay", "surface"],
    }

    def meta(self, name, value):
        if value:
            pat1 = self.dbcp[name][1]
            pat2 = self.dbcp[name][0]
        else:
            pat1 = self.dbcp[name][0]
            pat2 = self.dbcp[name][1]
        return FileTextReplacement(f"{name}={pat1}", f"{name}={pat2}")

    def fullscreen(self, value):
        yield self.meta("fullscreen", value)

    def aspect_ratio(self, value):
        yield self.meta("aspect", value)
        yield self.meta("output", value)


def queue(ops):
    all_ops = defaultdict(set)
    targets = ["dosbox.conf", "dosbox_tandy.conf", "dosbox_ece.conf", "dosbox2.conf", "ssp.conf"]
    for target in targets:
        for path in db[target]:
            all_ops[path].update(ops)
    return all_ops.items()


def enable_adult_games(value):
    if value:
        copyfile("xml/MS-DOS.xml", "Data/Platforms/MS-DOS.xml")
    else:
        copyfile("xml/DOSFAMILY.xml", "Data/Platforms/MS-DOS.xml")


def clean():
    to_clean = [
        "eXoDOS/dosbox",
        "eXoDOS/scummvm",
        "eXoDOS/DataCache.txt",
        "eXoDOS/util/!NEVRLCK.EXE",
        "eXoDOS/util/!PATCHER.EXE",
        "eXoDOS/util/!RAWCOPY.EXE",
        "eXoDOS/util/BRC32.exe",
        "eXoDOS/util/CHOICE.EXE",
        "eXoDOS/util/Crack Aid.rar",
        "eXoDOS/util/Crock.rar",
        "eXoDOS/util/Locksmith.rar",
        "eXoDOS/util/locksmith131.zip",
        "eXoDOS/util/dosbox.zip",
        "eXoDOS/util/meagre.zip",
        "eXoDOS/util/ssr.exe",
        "eXoDOS/util/scummvm.zip",
        "eXoDOS/util/Skins.zip",
        # "eXoDOS/Games/!dos",
    ]
    for path in to_clean:
        print(f"deleting: {path}")
        subprocess.run(["rm", "-rf", path])


def fix_perms():
    print("fixing file permissions")
    p = subprocess.run("""find . -type f -iname "*exe" -exec chmod +x '{}' \;""", shell=True)


# print("unzipping files...")
# unzip("LaunchBox.zip")
# unzip("XODOSMetadata.zip")
# unzip("!DOSmetadata.zip")
# unzip("eXoDOS/util/util.zip", "eXoDOS/util")
# unzip("eXoDOS/util/Skins.zip", "eXoDOS", delete=True)
# unzip("eXoDOS/util/mt32.zip", "eXoDOS", delete=True)
# unzip("eXoDOS/util/meagre.zip", "eXoDOS", delete=True)
# unzip("eXoDOS/util/scummvm.zip", "eXoDOS", delete=True)
# unzip("eXoDOS/util/dosbox.zip", "eXoDOS", delete=True)

# this step requires !DOSmetadata
print("gathering files...")
db = ZipFiles("!DOSmetadata.zip").filename_db()
# db2 = FileSystemFiles("eXoDOS/Games/!dos").filename_db()

print("queueing operations...")
cfg_diff = set()
cfg = DOSBoxManager()
cfg_diff.update(cfg.fullscreen(True))
cfg_diff.update(cfg.aspect_ratio(True))
operations = queue(cfg_diff)
# TODO: the operations queue can be removed if file locks are implemented
print("applying operations...")

enable_adult_games(True)

for path, operations in operations:
    replace(path, operations)
