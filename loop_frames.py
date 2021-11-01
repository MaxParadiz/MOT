import os
import shutil


for i in range(0,249):
 inp = ('%s.png' % i)
 out = ('%s.png' % (498-i))
 shutil.copyfile(inp,out)
