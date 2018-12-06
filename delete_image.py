import os
import sys
import logging
import re

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

class DeleteImage():
    def __init__(self):
        self.root_dir=""

    def set_root_dir(self):
        ans=input("Please input the base dir,you want walk:")
        log.warn("ans={}".format(ans))
        if ans[-1] == "/":
            self.root_dir=ans
        else:
            self.root_dir=ans+"/"
        log.warn("self.root_dir={}".format(self.root_dir))

    def delete_img(self):
        for root,dirs,files in os.walk(self.root_dir):
            for fi in files:
                if fi.endswith('.img'):
                    abs_img=os.path.join(root,fi)
                    abs_zip=abs_img[:-4]+".zip"
                    abs_zip2 = abs_img[:-4] + "_int.zip"
                    log.warn('Will delete {}'.format(abs_zip))
                    log.warn('Will delete {}'.format(abs_zip2))
                    os.remove(abs_img)
                    os.remove(abs_zip)
                    os.remove(abs_zip2)

    def absolute_delete(self):
        partten1='.*R\d.\d{2}.\d{2}.zip'
        partten2 = '.*R\d.\d{2}.\d{2}_int.zip'
        for root,dirs,files in os.walk(self.root_dir):
            for fi in files:
                p1=re.search(partten1,fi)
                p2=re.search(partten2,fi)
                if p1:
                    abs_fi = os.path.join(root, p1.group())
                    log.warn('Will delete {}'.format(abs_fi))
                    os.remove(abs_fi)
                if p2:
                    abs_fi2 = os.path.join(root, p2.group())
                    log.warn('Will delete {}'.format(abs_fi2))
                    os.remove(abs_fi2)

if __name__ == "__main__":
    di=DeleteImage()
    di.set_root_dir()
    di.delete_img()
    di.absolute_delete()











