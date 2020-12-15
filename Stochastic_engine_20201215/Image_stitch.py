# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 11:03:23 2020

@author: 11487
"""
import os, shutil
from PIL import Image

def picMerge(imgDir='Correlation matrix/2005-2034_1003/',w=None,h=None,row=2,col=3,save_path='demo.png'):
    '''
    将多张图片以子图的形式合并到一张图片中去
    '''
    img_list=[Image.open(imgDir+one) for one in os.listdir(imgDir)]
    
    
    image1=img_list[0];
    image2=img_list[1];
    
    image1_size = image1.size
    image2_size = image2.size
    
    new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))
    new_image.paste(image1,(0,0))
    new_image.paste(image2,(image1_size[0],0))
    
    
    new_image.show()
    new_image.save(save_path)
    
    
    
    if w and h:
        pass
    else:
        w,h=img_list[0].size
        result=Image.new(img_list[0].mode,(w*col,h*row))
    
    if col==1:
        for i,im in enumerate(img_list):
            new_im=im.resize((w,h),Image.ANTIALIAS)
            result.paste(new_im,box=(0,i*h))
    else:
        cut_list=cutList(img_list,c=col)
    
    for j in range(len(cut_list)):
        for i,im in enumerate(cut_list[j]):
            new_im=im.resize((w,h),Image.ANTIALIAS)
            result.paste(new_im,box=(j*w,i*h))
    result.save(save_path)
    
    return None

picMerge(imgDir='Correlation matrix/2005-2034_1003/',w=None,h=None,row=2,col=3,save_path='demo.png')
a=0