from . models import Post
import logging

logger=logging.getLogger(__name__)

def my_scheduled_job():
  print("Hello User Good Morning")
#   f=open('/home/agilecpu93/Desktop/Docker/miniblog/debug.txt','w+')
#   f.write('Hello User Good Morning')
#   f.close()  