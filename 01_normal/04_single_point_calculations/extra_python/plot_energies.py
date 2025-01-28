import numpy as np
import matplotlib.pyplot as plt

layer_1 = []
layer_2 = []

#for i in range(1000, 2000):
#    layer_2.append(np.loadtxt(f"E_files_NEW/_E2_{i}_.txt")[280])
#    layer_1.append(np.loadtxt(f"E_files_NEW/_E1_{i}_.txt")[280])

#    print(np.loadtxt(f"E_files_NEW/_E1_{i}_.txt")[280])

for i in range(1000, 2000):
    file_name = f"E_files_NEW/_E1_{i}_.txt"
    value_at_index_280 = np.loadtxt(file_name)[280]
    
    print(f"File: {file_name}, Value at index 280: {value_at_index_280}")
    
    layer_1.append(value_at_index_280)


x = range(1000, 2000)

plt.plot(x, layer_1, "r-")
plt.plot(x, layer_2, "b-")

plt.savefig("E_TEST.png") 
