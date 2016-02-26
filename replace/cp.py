import shutil 
import os
import sys
import errno
path_home =os.getcwd()
S1 = path_home+'/input'
S2 = path_home+'/moni'
S3 = path_home+'/temp-test'

 
def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)
            



print path_home
v = 31
for i in range(v):
    tem = i+1
    Des1 = path_home + '/v' + str(tem) + '/input'
    Des2 = path_home + '/v' +str (tem) + '/moni'
    Des3 = path_home + '/v' +str (tem) + '/temp-test'
    #print Des
    copy(S1,Des1)
    copy(S2,Des2)
    copy(S3,Des3)
    
    
    

    
    

