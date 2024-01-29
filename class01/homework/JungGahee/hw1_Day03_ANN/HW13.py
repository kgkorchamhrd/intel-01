#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# In[3]:


x = [5,7,8,7,2,17,2,9,4,11,12,9,6]
y = [99,86,87,88,111,86,103,87,94,78,77,85,86]


# In[4]:


slope, intercept, r, p, std_err = stats.linregress(x, y)


# In[5]:


def myfunc(x):
    return slope*x + intercept


# In[7]:


xx=np.linspace(0,18,180)
yy=slope*xx + intercept

plt.scatter(x,y)
plt.plot(xx,yy)
plt.show()


# In[ ]:




