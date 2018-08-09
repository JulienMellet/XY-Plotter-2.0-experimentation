import matplotlib.pyplot as plt
import numpy as np


# Processing of data
file = open("C:/Users/JulienM/Documents/GitHub/XY-Plotter-2.0-experimentation/data_1.txt","r")

# Standard deviation of values on the measurement
s_measurements = np.zeros((9,30))
means = np.zeros((9,30))
I_pdiode = np.zeros(3)
I_acc = np.zeros(3)
I_filter = np.zeros(3)

# l stand for length
for l in range(30):
    # i stand for indice
    for i in range(100):
        line = file.readline()
        duration, I_pdiode[0], I_pdiode[1], I_pdiode[2], I_acc[0], I_acc[1], I_acc[2], I_filter[0], I_filter[1], I_filter[2] = line.split(",")
        #print(duration)
        #print(I_filter[2])
        for k in range(3):
            means[k][l] += I_pdiode[k]/100
            means[3+k][l] += I_acc[k]/100
            means[6+k][l] += I_filter[k]/100

file.close()
print(means)

# Redefine 30 points that are means of each 100 measurement
I_pdiode = np.zeros((3,30))
I_acc = np.zeros((3,30))
I_filter = np.zeros((3,30))

Y = np.zeros(30)

for i in range(3):
    for j in range(30):
        I_pdiode[i][j] = means[i][j]
        I_acc[i][j] = means[3+i][j]
        I_filter[i][j] = means[6+i][j]

print("========================")
print(I_pdiode)
print(I_acc)

plt.plot(I_pdiode[0], I_pdiode[1], 'bx')
plt.plot(I_acc[0], I_acc[1], 'rx')
#plt.plot(I_filter[0], I_filter[1], 'gx')
plt.xlabel('x axis (m)')
plt.ylabel('y axis (m)')
plt.show()
