import os
import sys
import getopt
import subprocess
import shutil
import time
from colorama import init, Fore
from pprint import pprint
import ffmpeg
import proclib as p

init()

timestamp = round(time.time())

def showhelp():
    """
    Display the help information.
    """
    print("help")
    rs = '''
    -h, --help          show help
    -Q, --sequence      xxx
    -f, --x             xxx
'''
    # print(rs)
    # exit()


locationpath = os.getcwd()
dirname = os.getcwd()
basename = False
verbose = False
srcfile = False
testonly = False

# pprint(sys.argv)
# exit()

# print("args:",len(sys.argv))
if len(sys.argv) == 0:
    showhelp()

#^ if there is only one argument with no flags, then assume it is a filename
if len(sys.argv) < 3:
    print("1args")
    pprint(sys.argv)
    filename = sys.argv[1]
    basename = os.path.basename(locationpath)
    dirname = os.path.dirname(locationpath)

    fspec = False
else: #^ one or more switches exist
    pprint(sys.argv)
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hvtQ:y:", [
            "help",
            "verbose",
            "testonly",
        ])
    except Exception as e:
        p.errprint(str(e))

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            showhelp()
        if opt in ("-v", "--verbose"):
            verbose = True
        if opt in ("-t", "--testonly"):
            testonly = True
        if opt in ("-Q", "--sequence"):
            sequence = arg
            print(sequence)
        if opt in ("-y", "--yyy"):
            interx = int(arg)

basename, dirname, fspec, srcfile = p.getFnames(locationpath)

srcfile = f"{dirname}/{basename}"

print(f"dirname: {dirname}")
print(f"basename: {basename}")
print(f"srcfile: {srcfile}")
print(f"fspec: {fspec}")

id = p.getID(filename)
