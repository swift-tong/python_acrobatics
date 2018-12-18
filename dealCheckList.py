import xlrd
import xlwt
import sys
import re
import os
import codecs
from xlutils.copy import copy
import subprocess
#import win32com.client

dealSheet=""
listUnsignedApk=[]
listSignedApk=[]
listApk=[]
listSoBin=[]
itemColumn=0
originalIDColumn=0
originalMD5Column=0
targetIDColumn=0
targetMD5Column=0
packageColumn=0
thirdIndex=0
middleIndex=0
excelFile=""
unsigneddir=""
signeddir=""
fileinfo=""

def CallEccelFun():
    xls=win32com.client.Dispatch("Excel.Application")
    xls.Workbooks.Open(Filename="***.xls")
    ret = xls.Application.Run("foo", args)

def CheckSigned(apkstring):
    p=os.popen("jarsigner -verify %s"%apkstring)
    str=p.read()
    if "verified" in str:
        return "signed"
    else:
        return "unsigned"	
	
def SetDealSheet():
    global dealSheet
    dealSheet= input('please input the type of apk you want deal (th or mi):')
    print("dealSheet=",dealSheet)

def MergeApkList():
    for unsignApk in listUnsignedApk:
        for signApk in listSignedApk:
            if unsignApk[0] == 	signApk[0]:
                tmpApk=unsignApk+signApk[1:]
                listApk.append(tmpApk)
                break
            else:
                 continue

def GetExcelFile():
    global excelFile
    f_list = os.listdir(".")
    for i in f_list:
        if os.path.splitext(i)[1] == '.xls':
            excelFile=i
			
def CheckSheet():
    global excelFile
    rb = xlrd.open_workbook(excelFile)
    headList=["Item","原始ID","签名前MD5","改名后ID","签名后MD5","芯片","产品线","Source","dest","package","附录"]
    nameList=rb.sheet_names()
    wb=copy(rb)
    if "third" not in nameList:
        sheetThird=wb.add_sheet("third")
        for item,name in enumerate(headList):
            sheetThird.write(0,item,name)
    if "suying" not in nameList:
        sheetThird=wb.add_sheet("suying")
        for item,name in enumerate(headList):
            sheetThird.write(0,item,name)
    wb.save(excelFile)
			
def WriteExcel():
    nrows=0
    nomalRows=0
	
    rb = xlrd.open_workbook(excelFile)
    sheetIndex=0
    print("表单数量:", rb.nsheets)
    print("表单名称:", rb.sheet_names())
    nameList=rb.sheet_names()
    for index,name in enumerate(nameList):
        print("index=",index,"name=",name)
        if name == "third":
            thirdIndex=index
            print("thirdIndex=",thirdIndex)
        elif name=="suying":
            middleIndex=index
            print("middleIndex=",middleIndex)
    if dealSheet == "th":
        sheetIndex=thirdIndex
        print("sheetIndex=",sheetIndex)
    elif dealSheet == "mi":
        sheetIndex=middleIndex
        print("sheetIndex=",sheetIndex)		
    wb = copy(rb)
    print("sheetIndex=",sheetIndex)
    rsh = rb.sheet_by_index(sheetIndex)
    nrows = rsh.nrows
    print("nrows=",nrows)
    nomalRows=nrows
    ncols = rsh.ncols
    wsh=wb.get_sheet(sheetIndex)

    for i in range(ncols):
        cell_value=rsh.cell_value(0, i)
        print("cell_value=",cell_value)
        if cell_value=="Item":
            itemColumn=i
            print("itemColumn=",itemColumn)
        elif cell_value=="原始ID":
            originalIDColumn=i
            print("originalIDColumn=",originalIDColumn)
        elif cell_value=="签名前MD5":
            originalMD5Column=i
            print("originalMD5Column=",originalMD5Column)
        elif cell_value=="改名后ID":
            targetIDColumn=i
            print("targetIDColumn=",targetIDColumn)
        elif cell_value=="签名后MD5":
            targetMD5Column=i
            print("targetMD5Column=",targetMD5Column)
        elif cell_value=="package":
            packageColumn=i
            print("packageColumn=",packageColumn)

    for tup in listApk:
        flag=False
        for i in (range(nomalRows)):
            cell_value=rsh.cell_value(i,packageColumn)
            if cell_value==tup[0]:
                flag=True
                print("tup[0]=",tup[0])
                wsh.write(i,originalIDColumn,tup[1])
                wsh.write(i,originalMD5Column,tup[2])
                wsh.write(i,targetIDColumn,tup[3])
                wsh.write(i,targetMD5Column,tup[4])
        if flag==False:
                print("elsetup[0]=",tup[0])
                wsh.write(nrows,packageColumn,tup[0])
                wsh.write(nrows,originalIDColumn,tup[1])
                wsh.write(nrows,originalMD5Column,tup[2])
                wsh.write(nrows,targetIDColumn,tup[3])
                wsh.write(nrows,targetMD5Column,tup[4])
                nrows=nrows+1
				
    for tup in listSoBin:
        flag=False
        for i in (range(nomalRows)):
            cell_value=rsh.cell_value(i,originalIDColumn)
            if cell_value==tup[0]:
                flag=True
                print("tup[0]=",tup[0])
                wsh.write(i,originalIDColumn,tup[0])
                wsh.write(i,originalMD5Column,tup[1])
                wsh.write(i,targetIDColumn,tup[0])
                wsh.write(i,targetMD5Column,tup[1])
        if flag==False:
                print("elsetup[0]=",tup[0])
                wsh.write(nrows,originalIDColumn,tup[0])
                wsh.write(nrows,originalMD5Column,tup[1])
                wsh.write(nrows,targetIDColumn,tup[0])
                wsh.write(nrows,targetMD5Column,tup[1])
                nrows=nrows+1
    wb.save(excelFile)					

def GetPackageName(apkpath):
    pachageList=[]
    tmplist=[]
    p = subprocess.Popen("aapt dump badging %s" % apkpath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #p.wait()
    #p=os.popen("aapt dump badging %s" % apkpath)
    tmplist=p.stdout.readlines()
    print("ok")
    str=tmplist[0].decode()
    print(str)
    pachageList=str.split("'")
    return pachageList[1]

def GetMd5(apkpath):
    p=os.popen("certutil -hashfile %s MD5" %apkpath)
    str=p.read().split("\n")[1]
    x = str.split(' ')  
    md5Str = ''.join(x)  
    return md5Str

def DealDir():
    pathList=os.path.split(dir)
    signDir=pathList[-1]
    print("signDir=",signDir)
    if signDir == "unsigned":
       WriteExcel("org")
    elif signDir == "signed":
       WriteExcel("tag")

def Getdir():
    global unsigneddir
    global signeddir
    p=os.popen("echo %cd%")
    curdir=p.read().strip('\n')
    print(curdir)
    unsigneddir = os.path.join(curdir, "unsigned")
    signeddir = os.path.join(curdir, "signed")
    print("unsigneddir=",unsigneddir)
    print("signeddir=",signeddir)
	
def walk_dir(dir,topdown=True):
    for parent, dirs, files in os.walk(dir, topdown):
        for name in files:
            if name[-3:] == "apk":
                strName=os.path.join(parent,name)
                packageName=GetPackageName(strName)
                md5=GetMd5(strName)
                item=(packageName,name,md5)
                if dir.split("\\")[-1] == "unsigned":
                    listUnsignedApk.append(item)
                elif dir.split("\\")[-1] == "signed":
                    listSignedApk.append(item)				
                print(packageName)
            elif name[-2:] == "so":
                strName=os.path.join(parent,name)
                md5=GetMd5(strName)
                item2=(name,md5)
                listSoBin.append(item2)
            else:
                strName=os.path.join(parent,name)
                if os.path.isfile(strName) and  "."  not in name:
                    md5=GetMd5(strName)
                    item2=(name,md5)
                    listSoBin.append(item2)				
        for name in dirs:
            if name[-3:] == "apk":
                strName=os.path.join(dirs,name)
                packageName=GetPackageName(strName)
                md5=GetMd5(strName)
                item=(packageName,name,md5)
                if dir.split("\\")[-1] == "unsigned":
                    listUnsignedApk.append(item)
                elif dir.split("\\")[-1] == "signed":
                    listSignedApk.append(item)
                print(packageName)
            elif name[-2:] == "so":
                strName=os.path.join(parent,name)
                md5=GetMd5(strName)
                item2=(name,md5)
                listSoBin.append(item2)
            else:
                strName=os.path.join(parent,name)
                if os.path.isfile(strName) and "."  not in name:
                    md5=GetMd5(strName)
                    item2=(name,md5)
                    listSoBin.append(item2)

def WriteMiddleWareTxt():
    if dealSheet == "mi":
        fileinfo = open('middleware.txt','w')
        for tup in listApk:
            str='  '.join(list(tup))
            print("str=",str)
            fileinfo.write(str)
            fileinfo.write("\n-----------\n")			
        for tup in listSoBin:
            str=''.join(list(tup))
            print("str=",str)
            fileinfo.write(str)
            fileinfo.write("\n-----------\n")
        fileinfo.close()
			
if __name__ == "__main__":
    Getdir()
    GetExcelFile()
    CheckSheet()
    fileinfo = open('middleware.txt','w')
    SetDealSheet()
    walk_dir(unsigneddir,fileinfo)
    print(listUnsignedApk)
    walk_dir(signeddir,fileinfo)
    print(listSignedApk)
    MergeApkList()
    WriteMiddleWareTxt()
    print(listApk)
    print(listSoBin)
    WriteExcel()
    print("ok")






