import site
site.addsitedir('/home/zzy/xgkxflask/venv/lib/python3.6/site-packages')
import sys       
sys.path.insert(0, '/home/zzy/xgkxflask')
from flasky import app as application