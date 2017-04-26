import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

# rename into pandas readable csv
'''comment'''
for i in range(6):
    for j in range(7):
        temp_xls_name = 'x' + str(i+1) + 'y' + str(j+1) + '.xls'
        temp_csv_name = 'x' + str(i+1) + 'y' + str(j+1) + '.csv'
        try:
            os.rename(temp_xls_name, temp_csv_name)
        except:
            pass

array_droplet_count = np.zeros((7,6),dtype=np.int)
array_droplet_diameter = np.zeros((7,6),dtype=np.float32)
df_total = pd.DataFrame(columns=['Area', 'Location', 'Diameter'])
'''comment'''
for i in range(6):
    for j in range(7):
        temp_csv_name = 'x' + str(i + 1) + 'y' + str(j + 1) + '.csv'
        df_xiyj = pd.read_table(temp_csv_name)
        df_xiyj['Location'] = 'x' + str(i + 1) + 'y' + str(j + 1)
        df_xiyj = df_xiyj[['Area','Location']]
        df_xiyj['Diameter'] = np.sqrt(df_xiyj['Area']/np.pi)*2
        mean_diameter = np.mean(df_xiyj['Diameter'])
        total_rows = len(df_xiyj.index)
        array_droplet_count[6-j,5-i] = total_rows
        array_droplet_diameter [6-j,5-i] = mean_diameter
        df_total = df_total.merge(df_xiyj,how="outer")

# save combined data
writer = pd.ExcelWriter('2017-04-13Data_water.xlsx', engine='xlsxwriter')
df_total.to_excel(writer,sheet_name='Sheet1')
writer.save()
# histogram of diameter
plt.figure()
plt.hist(df_total['Diameter'], bins=500, normed=True)
ax1 = plt.gca()
ax1.set_xlim([0,5])
plt.show()
# heat map
plt.subplot(1,2,1)
plt.imshow(array_droplet_count)
plt.title('Droplet Count Heat Map')
plt.subplot(1,2,2)
plt.imshow(array_droplet_diameter)
plt.title('Droplet Diameter Heat Map')
plt.show()
# print results
print (array_droplet_count)
print (array_droplet_diameter)
print (np.mean(df_total['Diameter']))

