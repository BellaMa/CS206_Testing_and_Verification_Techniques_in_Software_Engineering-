import os
import sys
import math
import random
import glob
import filecmp

def readInFile(filename):
    if os.path.isfile(filename):
        with open(filename) as f:
            lines = [line.rstrip('\n') for line in open(filename)]
    else:
        lines = []
    return lines

def commandLineExeuction_0(programName,testCase,outputfileName):
    ## compile    
    commandLineStatement = 'gcc -g  ' + programName
    commandLineStatement += '.c -o ' + programName + ' 2>tem1.txt'

    os.system(commandLineStatement)

    ## run program
    commandLine = programName + ' ' + testCase + ' >>' + outputfileName
    os.system(commandLine)

      
def commandLineExeuction(programName,testSet,outputfileName):
    for testCase_tem in testSet[:]:
    	commandLineExeuction_0(programName,testCase_tem,outputfileName)


# is fault return 1, else return 0
def exposeFault(correct_version,fault_version):
	if len(correct_version) != len(fault_version):
		return 1
	for i in range(len(correct_version[:])):
		if correct_version[i] != fault_version[i]:
			return 1

	return 0



    

# generate an result.txt to store the correct output form a given test suite

# read in test suite
programName = 'replace'
FAULTYNUMBER = 3


output_file_correct_names = ['output_rand_state_ori.txt', 'output_rand_branch_ori.txt','output_rand_combined_ori.txt','output_total_state_ori.txt','output_total_branch_ori.txt','output_total_combined_ori.txt','output_add_state_ori.txt','output_add_branch_ori.txt','output_add_combined_ori.txt']
for item in output_file_correct_names[:]:
    if os.path.isfile(item):
        os.remove(item)
    else:    ## Show an error ##
        #print("Error: %s file not found" % item)
        pass


testSuite_rand_state = readInFile('output_rand_state.txt')
testSuite_rand_branch = readInFile('output_rand_branch.txt')
testSuite_rand_combined = readInFile('output_rand_combined.txt')

testSuite_total_state = readInFile('output_total_state.txt')
testSuite_total_branch = readInFile('output_total_branch.txt')
testSuite_total_combined = readInFile('output_total_combined.txt')

testSuite_add_state = readInFile('output_add_state.txt')
testSuite_add_branch = readInFile('output_add_branch.txt')
testSuite_add_combined = readInFile('output_add_combined.txt')

# run each test suite and results stored in outputfileName.txt
commandLineExeuction(programName,testSuite_rand_state,'output_rand_state_ori.txt')
commandLineExeuction(programName,testSuite_rand_branch,'output_rand_branch_ori.txt')
commandLineExeuction(programName,testSuite_rand_combined,'output_rand_combined_ori.txt')

commandLineExeuction(programName,testSuite_total_state,'output_total_state_ori.txt')
commandLineExeuction(programName,testSuite_total_branch,'output_total_branch_ori.txt')
commandLineExeuction(programName,testSuite_total_combined,'output_total_combined_ori.txt')

commandLineExeuction(programName,testSuite_add_state,'output_add_state_ori.txt')
commandLineExeuction(programName,testSuite_add_branch,'output_add_branch_ori.txt')
commandLineExeuction(programName,testSuite_add_combined,'output_add_combined_ori.txt')

output_file_correct = []

for i in output_file_correct_names[:]:
    tem_readin_correct = readInFile(i)
    output_file_correct.append(tem_readin_correct)
    


home_path = os.getcwd()
output_fault_names = []
output_fault = []



# now run the faultversion on each test suite ant output into *_v1.txt
for i in range(FAULTYNUMBER):
	tem = i+1
	tem_path = home_path + '/v'+ str(tem)
	os.chdir(tem_path)
	
	
	tem_output = []
	

	
	tem_filename_1 = 'output_rand_state_ori' + '_v' + str(tem) + '.txt'
	tem_filename_2 = 'output_rand_branch_ori'+ '_v' + str(tem) + '.txt'
	tem_filename_3 = 'output_rand_combined_ori'+ '_v' + str(tem) + '.txt'
	tem_filename_4 = 'output_total_state_ori' + '_v' + str(tem) + '.txt'
	tem_filename_5 = 'output_total_branch_ori' + '_v' + str(tem) + '.txt'
	tem_filename_6 = 'output_total_combined_ori' + '_v' + str(tem) + '.txt'
	tem_filename_7 = 'output_add_state_ori' + '_v' + str(tem) + '.txt'
	tem_filename_8 = 'output_add_branch_ori' + '_v' + str(tem) + '.txt'
	tem_filename_9 = 'output_add_combined_ori' + '_v' + str(tem) + '.txt'
	
	tem_output_filename = [tem_filename_1,tem_filename_2,tem_filename_3,tem_filename_4,tem_filename_5,tem_filename_6,tem_filename_7,tem_filename_8,tem_filename_9]
	
	for tem_f in tem_output_filename[:]:
	    if os.path.isfile(tem_f):
	        os.remove(tem_f)
	
	
	commandLineExeuction(programName,testSuite_rand_state,'output_rand_state_ori' + '_v' + str(tem) + '.txt')
	commandLineExeuction(programName,testSuite_rand_branch,'output_rand_branch_ori'+ '_v' + str(tem) + '.txt')
	commandLineExeuction(programName,testSuite_rand_combined,'output_rand_combined_ori'+ '_v' + str(tem) + '.txt')

	commandLineExeuction(programName,testSuite_total_state,'output_total_state_ori' + '_v' + str(tem) + '.txt')
	commandLineExeuction(programName,testSuite_total_branch,'output_total_branch_ori' + '_v' + str(tem) + '.txt')
	commandLineExeuction(programName,testSuite_total_combined,'output_total_combined_ori' + '_v' + str(tem) + '.txt')

	commandLineExeuction(programName,testSuite_add_state,'output_add_state_ori' + '_v' + str(tem) + '.txt')
	commandLineExeuction(programName,testSuite_add_branch,'output_add_branch_ori' + '_v' + str(tem) + '.txt')
	commandLineExeuction(programName,testSuite_add_combined,'output_add_combined_ori' + '_v' + str(tem) + '.txt')

	
	
	
	#tem_readin_1 = readInFile(tem_filename_1)
	#print tem_readin_1
	for i in tem_output_filename[:]:
	    tem_readin = readInFile(i)
	    tem_output.append(tem_readin)
	    
	
	output_fault.append(tem_output)
	#print output_fault
	
	#print "tem_output: ",tem_output
	
	os.chdir(home_path)


#print output_fault
count_0 = 0
count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0
count_6 = 0
count_7 = 0
count_8 = 0

result_detail_0 = []
result_detail_1 = []
result_detail_2 = []

result_detail_3 = []
result_detail_4 = []
result_detail_5 = []

result_detail_6 = []
result_detail_7 = []
result_detail_8 = []

for i in range(FAULTYNUMBER):
    
    
    v = i+1
    
    if output_fault[i][0] != output_file_correct[0]:
        count_0 += 1
        result_detail_0.append(v)
    if output_fault[i][1] != output_file_correct[1]:
        count_1 += 1
        result_detail_1.append(v)
    if output_fault[i][2] != output_file_correct[2]:
        count_2 += 1
        result_detail_2.append(v)

    if output_fault[i][3] != output_file_correct[3]:
        count_3 += 1
        result_detail_3.append(v)
    if output_fault[i][4] != output_file_correct[4]:
        count_4 += 1
        result_detail_4.append(v)
    if output_fault[i][5] != output_file_correct[5]:
        count_5 += 1
        result_detail_5.append(v)

    if output_fault[i][6] != output_file_correct[6]:
        count_6 += 1
        result_detail_6.append(v)
    if output_fault[i][7] != output_file_correct[7]:
        count_7 += 1
        result_detail_7.append(v)
    if output_fault[i][8] != output_file_correct[8]:
        count_8 += 1
        result_detail_8.append(v)

result = open('results.txt','w')
result.write('total faultversion: ')
result.write(str(FAULTYNUMBER))
result.write( '\nexposed faults: \n')

result.write( 'rand state: ')
result.write(str(count_0))
result.write('\nversion number: ')
result.write(str(result_detail_0))

result.write( '\n\nrand branch: ')
result.write(str(count_1))
result.write('\nversion number: ')
result.write(str(result_detail_1))

result.write('\n\nrand combined: ')
result.write(str(count_2))
result.write('\nversion number: ')
result.write(str(result_detail_2))

result.write('\n')
result.write('\n\ntotal state: ')
result.write(str(count_3))
result.write('\nversion number: ')
result.write(str(result_detail_3))

result.write('\n\ntotal branch: ')
result.write(str(count_4))
result.write('\nversion number: ')
result.write(str(result_detail_4))

result.write('\n\ntotal combined: ')
result.write(str(count_5))
result.write('\nversion number: ')
result.write(str(result_detail_5))

result.write('\n')
result.write( '\n\nadd state: ')
result.write(str(count_6))
result.write('\nversion number: ')
result.write(str(result_detail_6))

result.write( '\n\nadd branch: ')
result.write(str(count_7))
result.write('\nversion number: ')
result.write(str(result_detail_7))


result.write( '\n\nadd combined: ')
result.write(str(count_8))
result.write('\nversion number: ')
result.write(str(result_detail_8))

result.close()
