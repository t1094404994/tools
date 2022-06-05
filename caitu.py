# -*- coding: utf-8 -*-
#裁剪白鹭的MC和一般图集 因为MC数据不保存原图只保存原图。所以最好知道原图大小
import json
import os
from PIL import Image
def load(name):
    with open(name,"r") as json_file:
        data=json.loads(json_file.read())
        return data
#拆分白鹭MC图片函数
def caifen(imagePath,imageName): #图片所在路径和图片名字 注意MC和名字相同
    #图片与对应的JSON数据
    imagePath=imagePath
    jsonData=load(imagePath+imageName+".json")
    imgData=Image.open(imagePath+imageName+".png")
    print("\n正在裁剪"+imagePath+imageName+".png"+"...")
    #创建目录
    if(os.path.exists(imagePath+imageName)==False):
        os.makedirs(imagePath+imageName)
    #拆分MC格式的文件
    if("mc" in jsonData):
        jsonNameOffset={} #保存偏移量
        for key in jsonData["mc"][imageName]["frames"]:
            jsonNameOffset[key["res"]]=key
        for key in jsonData["res"]:
            #该图在大图中的位置
            s=jsonData["res"][key]
            #该图因为裁剪白边而需要的偏移
            offset=jsonNameOffset[key]
            #裁剪图片
            cropImage=imgData.crop((s["x"],s["y"],s["x"]+s["w"],s["y"]+s["h"]))
            #加上偏移后的真实宽高 因为MC数据并未保存图片的原宽高 所以不能完全还原原图
            h=s["h"]+offset["y"]
            w=s["w"]+offset["x"]
            #暂不加。直接规定一个宽高，不然会偏移
            newImage=Image.new("RGBA",(800,800))
            newImage.paste(cropImage,(offset["x"],offset["y"]))
            #保存图片
            newImageName=""
            if(len(key)>4 and (key.find("_png")!=-1 or key.find("_PNG")!=-1)):
                newImageName=key[0:(len(key)-4)]+".png"
            else:
                newImageName=key+".png"
            newImage.save(imagePath+imageName+"\\"+newImageName)
            print("生成文件:"+imagePath+imageName+"\\"+newImageName)
    else:#拆分普通格式的
        for key in jsonData["frames"]:
            info=jsonData["frames"][key]
            #裁剪对应的图片
            cropImage=imgData.crop((info["x"],info["y"],info["x"]+info["w"],info["y"]+info["h"]))
            newImage=Image.new("RGBA",(info["sourceW"],info["sourceH"]))
            newImage.paste(cropImage,(info["offX"],info["offY"]))
            #对于加了后缀的和没加后缀的分别处理
            newImageName=""
            if(len(key)>4 and (key.find("_png")!=-1 or key.find("_PNG")!=-1)):
                newImageName=key[0:(len(key)-4)]+".png"
            else:
                newImageName=key+".png"
            newImage.save(imagePath+imageName+"\\"+newImageName)
            print("生成文件:"+imagePath+imageName+"\\"+newImageName)
def readDir(path):
    fileList=os.listdir(path)
    for key in fileList:
        names=key.split(".")
        if(len(names)==2 and names[1]=="png"):
            caifen(path,names[0])
readDir(input("Cin Path\n"))
#TestMiniDom()