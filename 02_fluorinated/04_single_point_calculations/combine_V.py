import numpy as np

file1 = open("_V_COMBINED.txt", "w")

for i in range(1000, 2000):
    data = np.loadtxt(f"_V_files_01/_V_{i}_re.txt")
    np.savetxt(file1, data, fmt='%f')  # Convert array to string and write to file
    print(f"Writing _V_{i}_re.txt to file")

file1.close()

