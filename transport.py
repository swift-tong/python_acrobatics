import csv
from decimal import *
import re

class TransportPrice():
    def __init__(self):
        self.ori_file="./outbound_rates_7.12.18.csv"
        self.out_file="./outbound_rates_new.csv"
        self.head=['目的地','前缀','第一区间','第二区间','美元','人民币','2倍人民币']
        self.fi_list=[]
        self.fi_list.append(self.head)
        self.parities=6.8909


    def make_new_list(self,li):
        real_price=float(li[-1]) * self.parities
        real_double_price=real_price*2
        print('real_price={}'.format(real_price))
        print('real_double_price={}'.format(real_double_price))
        interception_price=Decimal(str(real_price)).quantize(Decimal('0.0000'))
        interception_doubel_price=Decimal(str(real_double_price)).quantize(Decimal('0.0000'))
        abs_price=str(interception_price)
        abs_double_price = str(interception_doubel_price)
        print('abs_price={}'.format(abs_price))
        print('abs_double_price={}'.format(abs_double_price))
        new_li=li
        new_li.append(abs_price)
        new_li.append(abs_double_price)
        print('new_li={}'.format(new_li))
        self.fi_list.append(new_li)

    def write_file(self):
        with open(self.out_file,'a',encoding='gbk') as out:
            wri=csv.writer(out,dialect='excel')
            for line in self.fi_list:
                wri.writerow(line)

    def read_file(self):
        partten='\d+.\d+'
        count=0
        with open(self.ori_file,'r',encoding="utf-8") as f:
            lines=csv.reader(f)
            for line in lines:
                p=re.search(partten,line[-1])
                if p:
                    print('---------------')
                    print(line[-1])
                    self.make_new_list(line)


if __name__ == "__main__":
    tp=TransportPrice()
    tp.read_file()
    tp.write_file()