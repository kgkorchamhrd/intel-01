#!/usr/bin/env python
# coding: utf-8

# In[9]:


import numpy as np
import matplotlib.pylab as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[10]:


x = np.linspace(-2, 2, 11)
y = np.linspace(-2, 2, 11)
print(x,'\n',y)


# In[11]:


x,y = np.meshgrid(x,y)
print(x,'\n',y)


# In[12]:


f = lambda x,y : (x-1)**2 + (y-1)**2


# In[14]:


z = f(x, y)
print(z)


# In[15]:


from mpl_toolkits.mplot3d import Axes3D

ax = plt.axes(projection='3d', elev=50, azim=-50)
ax.plot_surface(x,y,z, cmap=plt.cm.jet)

ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_zlabel('$z$')

plt.show()


# In[16]:


ax = plt.axes()
ax.contour(x, y, z, levels=np.linspace(0, 20, 20), cmap=plt.cm.jet)
ax.grid()
ax.axis('equal')
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
plt.show()


# In[ ]:




