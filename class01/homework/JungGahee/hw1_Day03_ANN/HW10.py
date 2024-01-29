#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 과제10 : matplotlib를 통해 그래프 plot
import numpy as np
import matplotlib.pylab as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


x = np.linspace(-2, 2, 11)
f = lambda x: x**2
fx = f(x)


# In[3]:


print(x)
print(fx)


# In[4]:


plt.plot(x, fx, '-o')
plt.grid()
plt.xlabel('x')
plt.ylabel('y')
plt.title('This is an example for 1d graph')
plt.show()


# In[ ]:




