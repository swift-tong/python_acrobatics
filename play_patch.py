import os
import logging
import sys
 
def add_coloring_to_emit_ansi(fn):
    def new(*args):
        levelno = args[1].levelno
        if(levelno>=50):
            color = '\x1b[34m' # deep red/fatal
        elif(levelno>=40):
            color = '\x1b[31m' # red/error
        elif(levelno>=30):
            color = '\x1b[32m' # yellow/warn
        elif(levelno>=20):
            color = '\x1b[37m' # white/info
        elif(levelno>=10):
            color = '\x1b[35m' # pink/debug
        else:
            color = '\x1b[0m' # normal
        args[1].msg = color + args[1].msg +  '\x1b[0m'  # normal
        return fn(*args)
    return new 

logging.StreamHandler.emit = add_coloring_to_emit_ansi(logging.StreamHandler.emit)
log = logging.getLogger("build check")
log.setLevel(logging.DEBUG)
hdlr = logging.StreamHandler()
formatter = logging.Formatter('%(message)s\n')
hdlr.setFormatter(formatter)
log.addHandler(hdlr)

class PlayPatch():
    def __init__(self):
        self.root_dir=""
        self.worspace=os.environ["HOME"]+"/workspace/"

    def set_root_dir(self):
        ans=raw_input("Please input the dir of your patch:")
        log.warn("ans={}".format(ans))
        if ans[-1] == "/":
            self.root_dir=ans
        else:
            self.root_dir=ans+"/"
        log.warn("self.root_dir={}".format(self.root_dir))

    def question_1(self):
        ans = raw_input("If check Done,please select continue(1) or break(2):")
        if ans == "continue" or ans == "1":
            log.warn("Continue Play patch!")
        elif ans == "break" or ans == "2":
            log.warn("Will exit")
            sys.exit()
        else:
            log.error("Select error!,please select again!")
            self.question_1()

    def question_2(self):
        ans = raw_input("If deal Done,please select continue(1) or break(2):")
        if ans == "continue" or ans == "1":
            log.warn("Continue Play patch!")
        elif ans == "break" or ans == "2":
            log.warn("Will exit")
            sys.exit()
        else:
            log.error("Select error!,please select again!")
            self.question_2()

    def play_patch(self,patch,walk_dir):
        os.chdir(self.worspace+walk_dir)
        statue_ret=os.popen('git status').read()
        log.warn(statue_ret)
        if 'git am --continue' in statue_ret or 'git am --skip' in statue_ret or 'git am --abort' in statue_ret:
            log.error("'git status' on {} wrong,please check!".format(walk_dir))
            self.question_1()

        am_ret=os.popen('git am {}'.format(patch)).read()
        log.warn(am_ret)
        if "git am --abort" in am_ret:
            log.error("Patch '{}' wrong,Please go  '{}' deal it.".format(patch,walk_dir))
            self.question_2()


    def walk_patch(self):
        for root,dirs,files in os.walk(self.root_dir):
            log.warn(str(files))
            files.sort()
            for fi in files:
                if fi.endswith(".patch"):
                    patch=os.path.join(root,fi)
                    log.warn(patch)
                    walk_dir=patch.split(self.root_dir)[-1].split(fi)[0]
                    log.warn(walk_dir)
                    self.play_patch(patch,walk_dir)


if __name__ == "__main__":
    pp=PlayPatch()
    pp.set_root_dir()
    pp.walk_patch()













