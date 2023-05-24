import cupy as cp
import cupyx
from cupyx import scipy
from cupyx.scipy import ndimage
import h5py, imageio
import os
import glob
import time
import numpy as np


#input_path=input("please type the input file folder path:")
#output_path=input("please type the output file folder path:")
input_path='/home/beams12/S1IDUSER/xiaoxu/laue/XEOL'
output_path='/home/beams12/S1IDUSER/xiaoxu/laue/XEOLOt'
input_file=input_path+'/*.tif'

list_temp=sorted(glob.glob(input_file))
list_img=list_temp[15:16]

img=[]

User_input_times_of_Coarse_median_filter=5
User_input_size_of_Coarse_median_filter=40
User_input_Threshold=10
User_input_size_of_Fine_median_filter=4
 
for img_name in list_img:
 start_time = time.time()
 print(img_name)
 
 temp=img_name.split("XEOL/")[1]
 temp=temp.split(".tif")[0]
 temp=int(''.join(filter(str.isdigit,temp)))
 name_digit="%06d" % temp
 temp='HASlong_laue_'+name_digit

 
 old_image_gpu=imageio.imread(img_name)
 old_image_gpu=cp.array(old_image_gpu)
 old_image_gpu=old_image_gpu.astype(cp.uint16)
 
 #Detect the image size#
 Height=old_image_gpu.shape[0]
 Width=old_image_gpu.shape[1]
 old_image_background_gpu=old_image_gpu
 
 #apply coarse median filter, calculate the background in gpu, then copy to cpu#
 for median_times in range(User_input_times_of_Coarse_median_filter):
  old_image_background_gpu=ndimage.median_filter(old_image_background_gpu,size=User_input_size_of_Coarse_median_filter)
  median_times=median_times+1
  old_image_background_cpu=cp.asnumpy(old_image_background_gpu)
  
 
 #add threshold to the background#
 old_image_background_gpu=old_image_background_gpu+User_input_Threshold
 new_image_raw_gpu=old_image_gpu
 new_image_raw_gpu=new_image_raw_gpu.astype(cp.uint16)
 old_image_background_cpu=cp.asnumpy(old_image_background_gpu)
 old_image_cpu=cp.asnumpy(old_image_gpu)
 
 for i in range(Height):
  for j in range(Width):
     if(old_image_background_cpu[i,j]>old_image_cpu[i,j]):
      old_image_background_cpu[i,j]=old_image_cpu[i,j]
      
 #remove the background#
 new_image_raw_cpu=old_image_cpu-old_image_background_cpu
 new_image_raw_gpu=cp.asarray(new_image_raw_cpu)
 
 #apply the fine median filter to the whole image with the background correction#
 new_image_gpu=ndimage.median_filter(new_image_raw_gpu,size=User_input_size_of_Fine_median_filter)
 new_image_cpu=cp.asnumpy(new_image_gpu)
 
 #imageio.imwrite(f"{output_path}/{temp}.tif",old_image_background_cpu.astype('uint16'))
 imageio.imwrite(f"{output_path}/{temp}.tif",new_image_cpu.astype('uint16'))
 print("--- %s seconds ---" % (time.time() - start_time))

 
