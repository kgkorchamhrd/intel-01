#!/usr/bin/env python
# coding: utf-8

# In[5]:


import numpy as np
a = np.array([1,2,3,4])
b = np.array([[1],[2],[3],[4]])


# In[6]:


print(a)
print(a.shape)
print(b)
print(b.shape)


# In[7]:


# transpose 함수의 사용방법을 실습.
# reshape 함수의 사용방법을 실습.
# reshape의 매개변수 중 -1의 의미 학습.
a = np.array([[1],[2],[3],[4]])
print(a)
print(a.T)
print(a.T.reshape(-1,4))
print(a.shape)
print(a.T.reshape(-1,4).T.shape)


# In[8]:


a = np.array([1,2,3,4])
b = a.reshape(4,-1)
print(a.reshape(4,-1))
print(a.shape, ',', b.shape)


# In[9]:


a = np.array([1,2,3,4,5,6])
print(a.reshape(3,2))
print(a.shape)
print(a.reshape(3,-1))
print(a.shape)
print(a.reshape(-1,2))
print(a.shape)


# In[14]:


a = np.array([k*10 for k in range(1,7)])
print(a)
b = a[[4,2,0]]
print(b)


# In[15]:


idx = np.arange(0, len(a))
print(idx)
np.random.shuffle(idx)
print(idx)
print(a[idx])


# In[ ]:




