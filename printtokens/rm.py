import shutil 
import os
import sys
import errno

path_home =os.getcwd()
S = path_home+'/inputs'



v = 4
for i in range(v):
    tem = i+4
    Des = path_home + '/v' + str(tem) + '/inputs'
    #print Des
    #copy(S,Des)
    shutil.rmtree(Des)
