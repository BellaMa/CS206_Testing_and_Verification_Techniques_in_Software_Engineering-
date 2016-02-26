import os
import sys
import math
import random
import glob

#### this read in files and return a list ####
def readInFile(filename):
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in open(filename)]

    return lines


#### this part will compile *.c program and has a .out file named as * ###
#### program name is the .out file name, arguments are the lines from  ###
#### universe.txt                                                      ###
#### command comes from list lines                                     ###
#### this will generate the coverage report !                          ###
def commandLineExeuction(programName,testCase):
    ## compile    
    commandLineStatement = 'gcc -g -fprofile-arcs -ftest-coverage ' + programName
    commandLineStatement += '.c -o ' + programName + ' 2>tem1.txt'

    os.system(commandLineStatement)

    ## run program
    commandLine = programName + ' ' + testCase + ' >>tem1.txt'
    os.system(commandLine)

    ## generate coverage report file ###
    ## report file name: program.c.gcov ###
    commandLine_coverage_report = 'gcov -b -c ' + programName + ' >>tem1.txt'
    os.system(commandLine_coverage_report)
        

#### used to delete coverage report, otherwise it will accumulate    ####
def  deleteCoverageFile(programName):
    filename1 = programName + '.c.gcov'
    filename2 = programName + '.gcda'
    filename3 = programName + '.gcno'
    #filename4 = programName
    if os.path.isfile(filename1):
        os.remove(filename1)
    else:    ## Show an error ##
        print("Error: %s file not found" % filename1)

    if os.path.isfile(filename2):
        os.remove(filename2)
    else:    ## Show an error ##
        print("Error: %s file not found" % filename2)

    if os.path.isfile(filename3):
        os.remove(filename3)
    else:    ## Show an error ##
        print("Error: %s file not found" % filename3)

    #if os.path.isfile(filename4):
    #    os.remove(filename4)
    #else:    ## Show an error ##
    #    print("Error: %s file not found" % filename4)


#### generate a list by randomlize its index ####


class TestData:
    # list for branch/statement/combined are 
    # generated from their orders in the coverage report
    # 0 -- not covered; 1 -- covered
    

    def __init__(self, testCase_current,programName):
        self.branch = []
        self.statement = []
        self.combined = []

        self.branchNumber = 0 # updates to len(branch)
        self.statementNumber = 0
        self.combinedNumber = 0
        ## generated report file: programName.c.gcov ###
        commandLineExeuction(programName,testCase_current)
        ## read in report
        self.lines = readInFile(programName + '.c.gcov')
        ## anaylsis report
        for i in range(len(self.lines[:])):
            tem_line = self.lines[i]
            if tem_line[0] == 'b': 
                # this line is about a branch
                if tem_line[10] == 'n':
                    # this branch never executed
                    self.branch.append(0)
                    self.combined.append(0)
                elif tem_line[16] is '0':               
                     # this branch is taken 0 times
                     self.branch.append(0)
                     self.combined.append(0)
                else:
                    # this branch is taken 
                    self.branch.append(1)
                    self.combined.append(1)

            if tem_line[0] == ' ':
                # this line is about a statement
                if tem_line[8] == '#':
                    # this statement never executed
                    self.statement.append(0)
                    self.combined.append(0)
                elif tem_line[8] == '-':
                    pass 
                else:
                    self.statement.append(1)
                    self.combined.append(1)

        ## initilise the size of each list
        self.statementNumber = len(self.statement)
        self.branchNumber = len(self.branch)
        self.combinedNumber = len(self.combined)
        deleteCoverageFile(programName)

def findStatement_ALL(all_test_data):
    #result = all_test_data[0].statement
    result = [0 for x in range(len(all_test_data[0].statement))]
    for i in range(len(all_test_data[:])):
        if i == 0:
            for j in range(len(all_test_data[i].statement[:])):
                result[j] += all_test_data[i].statement[j]
        if i != 0:
            for j in range(len(all_test_data[i].statement[:])):
                result[j] += all_test_data[i].statement[j]

    return result

def findStatementUnreachable(statement_all):
    indices = [i for i, x in enumerate(statement_all) if x == 0]
    return indices

def findBranch_ALL(all_test_data):
    #result = all_test_data[0].branch
    result = [0 for x in range(len(all_test_data[0].branch))]
    for i in range(len(all_test_data)):
        if i == 0:
            for j in range(len(all_test_data[i].branch[:])):
                result[j] += all_test_data[i].branch[j]
        if i != 0:
            for j in range(len(all_test_data[i].branch[:])):
                result[j] += all_test_data[i].branch[j]

    
    return result

def findBranchUnreachable(branch_all):
    indices = [i for i, x in enumerate(branch_all) if x == 0]
    return indices

def findCombined_ALL(all_test_data):
    #result = all_test_data[0].combined
    result = [0 for x in range(len(all_test_data[0].combined))]
    for i in range(len(all_test_data)):
        if i == 0:
            for j in range(len(all_test_data[i].combined[:])):
                result[j] += all_test_data[i].combined[j]
        if i != 0:
            for j in range(len(all_test_data[i].combined)):
                result[j] += all_test_data[i].combined[j]

    return result

def findCombinedUnreachable(combined_all):
    indices = [i for i, x in enumerate(combined_all) if x == 0]
    return indices

def findTestCase(current,next):
    # return true if next test case needs to add to current test set
    # rturn false otherwise
    current_indices_0 = [i for i, x in enumerate(current) if x == 0]
    for i in current_indices_0:
        if next[i] != 0:
            return True

    return False

def randomList(a):
    b = []
    for i in range(len(a)):
        element = random.choice(a)
        a.remove(element)
        b.append(element)
    
    return b

#### return the line numbers in universal.txt i.e. the line number for the test case ###
def randomTest(dataSet,unreachable_line_number):
    testCase_Number = len(dataSet)
    rand_Test_line_number = [x for x in range(testCase_Number)]
    
    rand_Test_line_number = randomList(rand_Test_line_number)
    
    tem_rand_test_number = rand_Test_line_number[0]
    current = dataSet[tem_rand_test_number][:]
  
    result = [tem_rand_test_number]
    
    for i in unreachable_line_number:       
        current[i] = 1
        
    for tem_rand_test_number in rand_Test_line_number[:]:
        next = dataSet[tem_rand_test_number]
        if findTestCase(current,next) is True:
            # update current and result
            for i in range(len(current)):
                current[i] += next[i]
            result.append(tem_rand_test_number)
    
    return result

#### return the line numbers in universal.txt i.e. the line number for the test case ###
def totalTest(dataSet,unreachable_line_number):
    testCase_Number = len(dataSet)
    result = []
    
    coverage = []
    for i in range(testCase_Number):
        tem = sum(dataSet[i])
        coverage.append(tem)
    
    # now coverage = [ (line_number, coverage_data) ...]
    line_number = [x for x in range(len(coverage))]
    coverage = zip(line_number,coverage)
    
    # sort line numbers by coverage from high to low
    coverage.sort(key = lambda tup: tup[1], reverse=True)   
    result.append(coverage[0][0])      
    first_line_number = coverage[0][0]    
    current = dataSet[first_line_number][:]
    
    # ignore unreachables
    for i in unreachable_line_number:       
        current[i] = 1
    
    for i in range(testCase_Number):
        tem_line_number = coverage[i][0]
        next_test = dataSet[tem_line_number]
        if findTestCase(current,next_test) is True:
            # update result and current
            for i in range(len(current)):
                current[i] += next_test[i]
            result.append(tem_line_number)
        
    #current_indices_0 = [i for i, x in enumerate(current) if x == 0]
    
    return result
    
def computeCoverage(data_test,line_for_coverage):
     # data_test is a single test case report 
     # line_for_coverage is the remaining uncovered statement/branch/combined lines in the report
     summation = 0
     for i in line_for_coverage:
          summation += data_test[i]
     
     return summation


#### return the line numbers in universal.txt i.e. the line number for the test case ###
def additionalTest(dataSet,unreachable_line_number):
    testCase_Number = len(dataSet)
    result = []
    
    coverage = []
    coverage_tem = []
    for i in range(testCase_Number):
        tem = sum(dataSet[i])
        coverage_tem.append(tem)
    # now coverage_tem = [ (line_number, coverage_data) ...]
    line_number = [x for x in range(len(coverage_tem))]
    coverage_tem = zip(line_number,coverage_tem)
    for item in coverage_tem:
         coverage.append(list(item))
    
    coverage.sort(key = lambda tup: tup[1], reverse=True)
    tem_line_number = coverage[0][0]
    current = dataSet[tem_line_number][:]
    result.append(tem_line_number)
    for i in unreachable_line_number[:]:       
        current[i] = 1
    current_not_covered_statment_or_branch = [] 
    for i in range(len(current)):    
         if current[i] == 0:
              current_not_covered_statment_or_branch.append(i)
    
    while len(current_not_covered_statment_or_branch) != 0:
        # update coverge
        for i in range(len(coverage)):
             cur_line = coverage[i][0]
             cur_test = dataSet[cur_line][:]
             coverage[i][1] = computeCoverage(cur_test,current_not_covered_statment_or_branch)
        coverage.sort(key = lambda tup: tup[1], reverse=True)
        tem_line_number = coverage[0][0]
        result.append(tem_line_number)
        current = dataSet[tem_line_number][:]
        # update current_not_covered_statment_or_branch
        old_not_covered_statment_or_branch = current_not_covered_statment_or_branch[:]
        for i in range(len(old_not_covered_statment_or_branch[:])):
             tem_uncovered_line_number = old_not_covered_statment_or_branch[i]
             tem_number = old_not_covered_statment_or_branch[i]
             if current[tem_uncovered_line_number] != 0:
                  current_not_covered_statment_or_branch.remove(tem_number)
             

    return result
     










#### main ###
programName = 'schedule'
testCase = readInFile('universe.txt')

## generate a list containing 3 kinds of coverage information
allTestData = [] # length is the total test cases
for cur_testCase in testCase[:]:
    tem_data = TestData(cur_testCase,programName)
    allTestData.append(tem_data)



## write to file
out_file = open('output.txt','w')
out_file.write('total test case: ')
out_file.write(str(len(testCase)))
out_file.write('\n')
out_file.write('total testdata length: ')
out_file.write(str(len(allTestData)))
out_file.write('\n')


## find the unreachables
statement_all = findStatement_ALL(allTestData)
branch_all = findBranch_ALL(allTestData)
combined_all = findCombined_ALL(allTestData)

unreachable_Statement_line_number = findStatementUnreachable(statement_all)
unreachable_Branch_line_number = findBranchUnreachable(branch_all)
unreachable_Combined_line_number = findCombinedUnreachable(combined_all)

out_file.write('------------- gneral info --------')
out_file.write('\n')
out_file.write('total statement number: ')
out_file.write(str(len(statement_all)))
out_file.write('\n')
out_file.write('unreachable_Statement total number: ')
out_file.write(str(len(unreachable_Statement_line_number)))
out_file.write('\n')
out_file.write('unreachable_Statement_line_number:\n')
for tem in unreachable_Statement_line_number:
     out_file.write(str(tem))
     out_file.write('\n')


out_file.write('\n')
out_file.write('total branch number: ')
out_file.write(str(len(branch_all)))
out_file.write('\n')
out_file.write('unreachable_Branch total number: ')
out_file.write(str(len(unreachable_Branch_line_number)))
out_file.write('\n')
out_file.write('unreachable_Branch_line_number:\n')
for tem in unreachable_Branch_line_number:
     out_file.write(str(tem))
     out_file.write('\n')


out_file.write('\n')
out_file.write('total statements and branches combined  number: ')
out_file.write(str(len(branch_all)))
out_file.write('\n')
out_file.write('unreachable_Combined total number: ')
out_file.write(str(len(unreachable_Combined_line_number)))
out_file.write('\n')
out_file.write('unreachable_Combined_line_number:\n')
for tem in unreachable_Combined_line_number:
     out_file.write(str(tem))
     out_file.write('\n')


#### prep                                            ###
statementTestData = []
branchTestData = []
combinedTestData = []
for i in range(len(allTestData)):
    statementTestData.append(allTestData[i].statement)
    branchTestData.append(allTestData[i].branch)
    combinedTestData.append(allTestData[i].combined)




#####  Random                                         ###
out_file.write('\n')
out_file.write('------------- random prioritization ------------')
output_rand_state = open('output_rand_state.txt','w')
output_rand_branch = open('output_rand_branch.txt','w')
output_rand_combined = open('output_rand_combined.txt','w')

out_file.write('\n')
randomTestSet_line_number_statement = randomTest(statementTestData,unreachable_Statement_line_number)
randomTestSet_line_number_branch = randomTest(branchTestData,unreachable_Branch_line_number)
randomTestSet_line_number_combined = randomTest(combinedTestData,unreachable_Combined_line_number)


out_file.write('test cases number (statement coverage):  ')
out_file.write(str(len(randomTestSet_line_number_statement)))
out_file.write(' \nthese test cases are: \n')
for i in randomTestSet_line_number_statement:
     tem = testCase[i]
     output_rand_state.write(str(tem))
     output_rand_state.write('\n')  


out_file.write('\n') 
out_file.write('\n')
out_file.write('test cases number (branch coverage):  ')
out_file.write(str(len(randomTestSet_line_number_branch)))
out_file.write(' \nthese test cases are: \n')
for i in randomTestSet_line_number_branch:
     tem = testCase[i]  
     output_rand_branch.write(str(tem))
     output_rand_branch.write('\n')  


out_file.write('\n') 
out_file.write('\n')
out_file.write('test cases number (combined coverage):  ')
out_file.write(str(len(randomTestSet_line_number_combined)))
out_file.write(' \nthese test cases are: \n')
for i in randomTestSet_line_number_combined:
     tem = testCase[i]   
     output_rand_combined.write(str(tem))
     output_rand_combined.write('\n')  



####  Total                                           ###
output_total_state = open('output_total_state.txt','w')
output_total_branch = open('output_total_branch.txt','w')
output_total_combined = open('output_total_combined.txt','w')


out_file.write('\n')
out_file.write('\n')
out_file.write('------------- total prioritization -------------')
out_file.write('\n')
totalTestSet_line_number_statement = totalTest(statementTestData,unreachable_Statement_line_number)
totalTestSet_line_number_branch = totalTest(branchTestData,unreachable_Branch_line_number)
totalTestSet_line_number_combined = totalTest(combinedTestData,unreachable_Combined_line_number)


out_file.write('test cases number (statement coverage):  ')
out_file.write(str(len(totalTestSet_line_number_statement)))
out_file.write(' \nthese test cases are: \n')
for i in totalTestSet_line_number_statement:
     tem = testCase[i]  
     output_total_state.write(str(tem))
     output_total_state.write('\n')  

out_file.write('\n')
out_file.write('\n')
out_file.write('test cases number (branch coverage):  ')
out_file.write(str(len(totalTestSet_line_number_branch)))
out_file.write(' \nthese test cases are: \n')
for i in totalTestSet_line_number_branch:
     tem = testCase[i]  
     output_total_branch.write(str(tem))
     output_total_branch.write('\n')  

out_file.write('\n')
out_file.write('\n')
out_file.write('test cases number (combined coverage):  ')
out_file.write(str(len(totalTestSet_line_number_combined)))
out_file.write(' \nthese test cases are: \n')
for i in totalTestSet_line_number_combined:
     tem = testCase[i]
     output_total_combined.write(str(tem))
     output_total_combined.write('\n') 

####  additional                                           ###
output_add_state = open('output_add_state.txt','w')
output_add_branch = open('output_add_branch.txt','w')
output_add_combined = open('output_add_combined.txt','w')

out_file.write('\n')
out_file.write('\n')
out_file.write('------------- additional prioritization --------')
out_file.write('\n')
additionalTestSet_line_number_statement = additionalTest(statementTestData,unreachable_Statement_line_number)
additionalTestSet_line_number_branch = additionalTest(branchTestData,unreachable_Branch_line_number)
additionalTestSet_line_number_combined = additionalTest(combinedTestData,unreachable_Combined_line_number)


out_file.write('test cases number (statement coverage):  ')
out_file.write(str(len(additionalTestSet_line_number_statement)))
out_file.write(' \nthese test cases are: \n')
for i in additionalTestSet_line_number_statement:
     tem = testCase[i]
     output_add_state.write(str(tem))
     output_add_state.write('\n')  

out_file.write('\n')
out_file.write('\n')
out_file.write('test cases number (branch coverage):  ')
out_file.write(str(len(additionalTestSet_line_number_branch)))
out_file.write(' \nthese test cases are: \n')
for i in additionalTestSet_line_number_branch:
     tem = testCase[i]
     output_add_branch.write(str(tem))
     output_add_branch.write('\n')  

out_file.write('\n')
out_file.write('\n')
out_file.write('test cases number (combined coverage):  ')
out_file.write(str(len(additionalTestSet_line_number_combined)))
out_file.write(' \nthese test cases are: \n')
for i in additionalTestSet_line_number_combined:
     tem = testCase[i]  
     output_add_combined.write(str(tem))
     output_add_combined.write('\n') 
