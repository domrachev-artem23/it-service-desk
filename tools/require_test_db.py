import os, sys
name=os.getenv('TEST_DB_NAME','')
if not name.endswith('_test'):
    sys.exit('Set TEST_DB_NAME to a dedicated database ending in _test before integration tests.')
print('Test database selected:',name)
