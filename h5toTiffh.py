import h5py, imageio
import numpy as np 
import os
import glob

folder_name=input("please type the input file folder path:")

file_names=os.listdir(folder_name)
for name in file_names:
 if (name.endswith("h5")):
  old_name=folder_name+'/'+name
  temp=name.split(".")[0]
  temp=int(''.join(filter(str.isdigit,temp)))
  print(temp)
  name_digit="%06d" % temp
  new_name=folder_name+'/'+'HASlong_laue_'+name_digit+'.h5'
  os.rename(old_name,new_name)

input_file=folder_name+'/*.h5'
list_temp=sorted(glob.glob(input_file))
list_img=list_temp[0:100]

for img_name in list_img:
 print(img_name)
 temp=img_name.split("HASlong_laue/")[1]
 temp=temp.split(".h5")[0]
 old_image=h5py.File(img_name, "r")
 g2=old_image['entry1/data/data']
 imageio.imwrite(f"{folder_name}/{temp}.tif",g2.astype('uint16'))
 

 
 
 
            
    
