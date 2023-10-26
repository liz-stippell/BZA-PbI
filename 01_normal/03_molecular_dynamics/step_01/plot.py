import numpy as np
import matplotlib.pyplot as plt

file = open("OSZICAR")

file_new = file.read()

file.close()

# initializing string
test_str = file_new
 
# initializing substring
test_sub = "T="

 
# using list comprehension + startswith()
# All occurrences of substring in string
res = [i for i in range(len(test_str)) if test_str.startswith(test_sub, i)]

writeto_file = open("T.txt", "w")
#file = writeto_file.readlines()
for i in range(0, 2999):
    #print(file_new[res[i]+7:res[i]+10])
    #print(file_new[res[i]:res[i]+7])
#    test_1 = file_new[res[i]+7-12+7:res[i]+8].replace("E=", "")#.replace("    ", " ")
#    test_2 = file_new[res[i]+7-12+7-12+7-12:res[i]+7-12+7-12]

    test = file_new[res[i]+7-12:res[i]+8].replace("T=", "").replace("     ", " ")

    writeto_file.write(f"{test} \n")
    
writeto_file.close()

x = np.loadtxt("T.txt",usecols=(0,)) #[:,0]
y = np.loadtxt("T.txt", usecols=(1,)) #[:,1]

plt.plot(x, y)
plt.ylabel("Temperature / K" , fontsize=14)
plt.xlabel("Time / fs", fontsize=14)
plt.savefig("TempVTime.png")

# initializing string
test_str = file_new
 
# initializing substring
test_sub = "E="

 
# using list comprehension + startswith()
# All occurrences of substring in string
res = [i for i in range(len(test_str)) if test_str.startswith(test_sub, i)]

writeto_file = open("E.txt", "w")
#file = writeto_file.readlines()
for i in range(0, 2999):
    #print(file_new[res[i]+7:res[i]+10])
    #print(file_new[res[i]:res[i]+7])
    test_1 = file_new[res[i]+7-12+7:res[i]+8].replace("E=", "")#.replace("    ", " ")
    test_2 = file_new[res[i]+7-12+7-12+7-12:res[i]+7-12+7-12]

    #test = file_new[res[i]+7-12+7-12+7-12:res[i]+8]


    writeto_file.write(f"{test_2}  {test_1} \n")
    
writeto_file.close()

x = np.loadtxt("E.txt", usecols=(0, ))#[:,0]
y = np.loadtxt("E.txt", usecols=(1, ))#[:,1]

plt.plot(x, y)

plt.show()
plt.ylabel("Energy / eV", fontsize=14)
plt.xlabel("Time / fs", fontsize=14)
plt.savefig("EnergyVTime.png")
