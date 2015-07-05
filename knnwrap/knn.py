from pykgraph import KGraph
import numpy as np
import pickle


class KnnIndex:
    def __init__(self):
        self.Index=KGraph()
        self.iterations=20
        self.L=64
        self.K=8
        self.S=30
        self.controls=100
        self.delta=0.005
        self.recall=0.95
        self.prune=2
    def set_dataset_key_map(self,map_vector):
        assert(len(self.dataset)==len(map_vector))
        self.key_map=map_vector
    def train(self,dataset):
        self.dataset=dataset
        self.dtype=dataset.dtype
        assert(self.dtype in [np.uint8,np.float])
        self.Index.build(
                self.dataset,
                self.iterations, 
                self.L, 
                self.K, 
                self.S, 
                self.controls, 
                self.delta, 
                self.recall, 
                self.prune)
    def save(self,filename):
        indexName=filename.split('.')[0]+'.kgi'
        self.indexName=indexName
        self.Index.save(indexName)
        d = dict(self.__dict__)
        del d['Index']
        with open(filename, 'wb') as fp:
            pickle.dump(d,fp)
        return filename
    def load(self,filename):
        with open(filename, 'rb') as pkl_file:
            this_d=pickle.load(pkl_file)
            self.__dict__.update(this_d)
            if 'indexName' in this_d:
                I=KGraph()
                I.load(self.indexName)
                self.Index=I
    def query(self,queryset,K=8,probe=100,mapped=False):
        assert(self.dtype==queryset.dtype)
        ans=self.Index.search(self.dataset,queryset,K=K, P=probe)
        if mapped :
            return np.array([
                    [self.key_map[i] for i in line]
                   for line in ans])
        return np.array(ans)

