# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dfList = []
resultArr = []
fileName = 'daletou'

df = pd.read_csv(fileName + '.csv', names=['stage', 'r1', 'r2', 'r3', 'r4', 'r5', 'b1', 'b2'], encoding='utf-8')


def create(stage, r1, r2, r3, r4, r5, b1, b2):
    print stage, r1, r2, r3, r4, r5, b1, b2

i = 0
while i < len(df[['stage', 'r1', 'r2', 'r3', 'r4', 'r5', 'b1', 'b2']]):
    item = df.ix[i]
    i += 1
    create(item['stage'], item['r1'], item['r1'], item['r1'], item['r1'], item['r1'], item['b1'], item['b2'])
else:
    # fileBeforeStr = ''
    # file = open('../../self_alice/'+fileName+ '.aiml', 'wb')
    # file.write(fileBeforeStr)
    # file.close()
    print 'success'

plt.figure(1)
plt.plot(df[['r1']])
print df[['r1']]
plt.show()

plt.figure(2)
plt.plot(df[['r2']])
print df[['r2']]
plt.show()

# plt.figure(1)  # 创建图表1
# ax1 = plt.subplot(211)  # 在图表2中创建子图1
#
# x = np.linspace(0, 3, 100)
# for i in xrange(5):
#     plt.figure(1)  # ❶ # 选择图表1
#     plt.plot(x, np.exp(i * x / 3))
#     plt.sca(ax1)  # ❷ # 选择图表2的子图1
#     plt.plot(x, np.sin(i * x))
#     plt.plot(x, np.cos(i * x))
#
# plt.show()
