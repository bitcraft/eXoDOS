import os
import subprocess
import signal

def unzip(filename, dest=None, delete=False):
    if dest:
        args = ["7z", "-y", "x", filename, "-o" + dest]
    else:
        args = ["7z", "-y", "x", filename]

    p = subprocess.Popen(args)
    try:
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGKILL)
        print("\naborted.")

    if delete:
        os.unlink(filename)
    return p


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


r = task()
r()

import sys

sys.exit()

# test for re-install /eXoDOS/Games/!dos

if 0:
    unzip("LaunchBox.zip")
    unzip("XODOSMetadata.zip")
    unzip("!DOSmetadata.zip")

unzip("eXoDOS/util/util.zip", "util")
unzip("eXoDOS/util/Skins.zip", delete=True)
unzip("eXoDOS/util/mt32.zip", delete=True)
unzip("eXoDOS/util/meagre.zip", delete=True)
unzip("eXoDOS/util/scummvm.zip", delete=True)
unzip("eXoDOS/util/dosbox.zip", delete=True)


# TODO: scummvm cfg
# cp .\xml\MS-DOS.xml .\Data\Platforms\MS-DOS.xml
