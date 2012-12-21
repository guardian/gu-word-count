import os

from google.appengine.api import apiproxy_stub_map
# from google.appengine.api import datastore_file_stub
from google.appengine.datastore import datastore_sqlite_stub
from google.appengine.api import memcache
from google.appengine.api.memcache import memcache_stub
from google.appengine.api import taskqueue
from google.appengine.api.taskqueue import taskqueue_stub
from google.appengine.api import urlfetch_stub

from google.appengine.api import appinfo

app_root = os.path.dirname(__file__)
dbpath = "%s/tmp/dev.sqlite3" % app_root
# load app.yaml config
app_ext_info = appinfo.LoadSingleAppInfo(file('%s/app.yaml' % app_root, 'r'))
app_id = 'dev~%s' % app_ext_info.application

# set the app ID to make stubs happy, esp. datastore
os.environ['APPLICATION_ID'] = app_id


# Init the proxy map and stubs
apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()

# sqlite Datastore
opts_for_ds = {
  'require_indexes': True, 
  'verbose': True
}
ds_stub = datastore_sqlite_stub.DatastoreSqliteStub(app_id, dbpath, **opts_for_ds)
apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', ds_stub)
# Memcache
mc_stub = memcache_stub.MemcacheServiceStub()
apiproxy_stub_map.apiproxy.RegisterStub('memcache', mc_stub)
# Task queues
tq_stub = taskqueue_stub.TaskQueueServiceStub()
apiproxy_stub_map.apiproxy.RegisterStub('taskqueue', tq_stub)
# URLfetch service
uf_stub = urlfetch_stub.URLFetchServiceStub()
apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', uf_stub)


# pretty printing
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

# load the app stuff, like models
from models import *
