from knn import KnnIndex

import numpy as np

testFile='testindex.pk'
data=np.random.normal(3,3,(1000,100))
I=KnnIndex()
print 'TEST::init'
I.train(data)
print 'TEST::train'
out_I = I.query(data[0:50])
print 'TEST::query'
I.save(testFile)
print 'TEST::save'

J=KnnIndex()
J.load(testFile)
print 'TEST::load'
out_J = J.query(data[0:50])
print 'TEST::query'
assert(sum(sum(out_I-out_J))==0)
print 'TEST::FLOAT OK'

data=np.random.randint(256,size=(1000,32)).astype(np.uint8)
I=KnnIndex()
print 'TEST::init'
I.train(data)
print 'TEST::train'
out_I = I.query(data[0:50])
print 'TEST::query'
I.save(testFile)
print 'TEST::save'

J=KnnIndex()
J.load(testFile)
print 'TEST::load'
out_J = J.query(data[0:50])
print 'TEST::query'
assert(sum(sum(out_I-out_J))==0)
print 'TEST::BIN OK'


