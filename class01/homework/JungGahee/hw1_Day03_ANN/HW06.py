#!/usr/bin/env python
# coding: utf-8

# In[1]:


items = [[1,2], [3,4], [5,6]]
for item in items:
    print(item[0], item[1])


# In[2]:


for item1, item2 in items:
    print(item1, item2)


# In[3]:


items = [(1,2), (3,4), (5,6)]
for item1, item2 in items:
    print(item1, item2)


# In[4]:


info = {'A':1, 'B':2, 'C':3}
for key in info:
    print(key, info[key])


# In[5]:


for key, value in info.items():
    print(key, value)


# In[6]:


items1 = [[1,2], [3,4],[5,6]]
items2 = [['A','B'], ['C','D'],['E','F']]
print(items1)
print(items2)


# In[7]:


for digits, characters in zip(items1, items2):
    print(digits, characters)


# In[8]:


a=[]
for k in range(0,5):
    a.append(k)
print(a)


# In[9]:


a=[k for k in range(0,5)]
print(a)


# In[10]:


a=[k for k in range(0,5) if k % 2 == 0]
print(a)


# In[12]:


a={k : k*10 for k in range(0,5)}
print(a)


# In[ ]:




