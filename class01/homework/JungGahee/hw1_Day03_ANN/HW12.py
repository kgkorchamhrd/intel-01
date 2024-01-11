#!/usr/bin/env python
# coding: utf-8

# In[9]:


import numpy as np
import matplotlib.pylab as plt
A = np.matrix('\
              1,4,2,0;\
              9,5,0,0;\
              4,0,2,4;\
              6,1,8,3')
x = np.matrix('1;2;3;4').reshape(1,-1)
print(A)
print(x)


# In[10]:


b=A*x.T
print("A*x=",b)


# In[11]:


A = np.matrix('\
              4,5,2,1;\
              2,3,8,0;\
              1,0,7,2')
x = np.matrix('1;2;3;4')
b=A*x
print("A*x=",b)

