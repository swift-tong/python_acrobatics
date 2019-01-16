#-*- encoding=utf-8 -*-
import logging
import re
import os
import json
import csv


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

class GetPartitionTable():
    def __init__(self):
        self.parameter=""
        self.base_dir=os.path.dirname(os.path.abspath(__file__))
        self.partition_list=[]
        self.partition_dict={}
        self.rules_list=[]
        self.partition_file="PartitionTable.txt"

    def get_parameter(self):
        path=raw_input("Please input the path of parameter: ")
        if path.startswith('/'):
            self.parameter=path
        else:
            self.parameter=os.path.join(self.base_dir,path)
        log.warn("self.parameter={}".format(self.parameter))

    def get_partition_list(self):
        partten='0x(\w+)@0x(\w+)\((\w+)\)'
        partten2='-@0x(\w+)\((\w+)\)'
        partten3='\w*0x(\w+)'
        with open(self.parameter,"r") as f:
            ret_str=f.read()
            ret_list=re.findall(partten,ret_str)
            for item in ret_list:
                tmp_list=[item[2],item[1],item[0]]
                self.partition_list.append(tmp_list)
            p=re.search(partten2,ret_str)
            if p:
                a=p.group(1);b=p.group(2)
                tmp_list2=['',a,b]
                # int_x=int(a,16)
                # last_2=self.partition_list[-1][1]
                # int_y=int(last_2,16)
                # log.warn('int_y={}'.format(int_y))
                # log.warn('int_x={}'.format(int_x))
                # last_1=hex(int_y-int_x)
                # p2=re.search(partten3,last_1)
                # if p2:
                #     last_1=p2.group(1)
                # else:
                #     log.error("Some metirc happen,please check!")
                # log.warn('last_1={}'.format(last_1))
                # tmp_list2[0]=last_1
                tmp_list2.reverse()
                log.warn("tmp_list3={}".format(tmp_list2))
                self.partition_list.append(tmp_list2)

            log.warn(str(self.partition_list))


    def write_to_json(self):
        for item in self.partition_list:
            key=item[0]
            value=[{"起始位置" : item[1]},
                   {"大小" : item[2]}
                    ]
            self.partition_dict[key]=value
        json_str=json.dumps(self.partition_dict,ensure_ascii=False,indent=4)
        log.warn(json_str)

    def write_to_txt(self):
        flag=False
        totle=0
        self.partition_list.insert(0,['分区','起始位置','大小'])
        len1=0;len2=0;len3=0
        for item in self.partition_list:
            len1=len(item[0]) if len(item[0]) > len1 else len1
            len2 = len(item[1]) if len(item[1]) > len2 else len2
            len3 = len(item[2]) if len(item[2]) > len3 else len3
        log.warn("len1={}".format(len1))
        log.warn("len2={}".format(len2))
        log.warn("len3={}".format(len3))

        for item in self.partition_list:
            if flag:
                tmp_str=item[0]+' '*(len1-len(item[0]))+' '+"0x"+item[1]+' '*(len2-len(item[1]))+' '+item[2]+' '*(len3-len(item[2]))+'\n'
                if item[2][-1] == "M":
                    totle+=int(item[2][:-1])
            else:
                tmp_str=item[0]+' ' * (len1 - len(item[0])/2)+' '+item[1] + ' '*(len2 - len(item[1])/2)+' '+ item[2] + ' '*(len3 - len(item[2])/2)+'\n'
                flag=True
            self.rules_list.append(tmp_str)
        self.rules_list.append("totle : {}M".format(totle))
        log.warn(str(self.rules_list))

        with open(self.partition_file,"wb") as f:
            f.writelines(self.rules_list)

    def calc_partition(self):
        for item in self.partition_list:
            if item[2]:
                block=int(item[2],16)
            else:
                block=0
            mbytes=block*512
            if mbytes:
                size=str(mbytes/1024/1024)+"M"
            else:
                size="--"
            item[2]=size
        log.warn("partition_list={}".format(str(self.partition_list)))


if __name__=="__main__":
    gpt=GetPartitionTable()
    gpt.get_parameter()
    gpt.get_partition_list()
    gpt.calc_partition()
    #gpt.write_to_json()
    gpt.write_to_txt()












