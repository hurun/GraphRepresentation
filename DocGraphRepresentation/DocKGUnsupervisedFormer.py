'''
Created on my MAC Aug 31, 2015-9:59:01 PM
What I do:
    I form doc's kg in various unsupervised ways
What's my input:
    a root class about API's
    several independent class for each different ways of filling the doc graph
What's my output:
    DocKG
@author: chenyanxiong
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
import numpy as np
import scipy
import pickle
import json

from DocKnowledgeGraph import DocKnowledgeGraphC
import logging

class DocKGUnsupervisedFormerC(cxBaseC):
    
    def FillDocGraph(self,DocNo):
        raise NotImplementedError
    
    

class DocKGAnaFormerC(DocKGUnsupervisedFormerC):
    def Init(self):
        DocKGUnsupervisedFormerC.Init(self)
        self.hDocAna = {}   # preloaded from QueryFaccDir I would say for now.
        self.MaxNodePerGraph = 500
        
    def SetConf(self, ConfIn):
        DocKGUnsupervisedFormerC.SetConf(self, ConfIn)
        self.MaxNodePerGraph = self.conf.GetConf('maxnodepergraph', self.MaxNodePerGraph)
    
    @staticmethod
    def ShowConf():
        DocKGUnsupervisedFormerC.ShowConf()
        print 'maxnodepergraph'
    
    def FillDocGraph(self, DocNo):
        DocKg = DocKnowledgeGraphC()
        DocKg.DocNo = DocNo
        
        if not DocNo in self.hDocAna:
            logging.warn('[%s] doc ana not found',DocNo)
            return DocKg
        
        lAna = self.hDocAna[DocNo]
        
        '''
        keep top self.MaxNodePerGraph node, via sum ana score as weights
        '''
        
        hObjScore = {}
        for ObjId,name,score in lAna:
            if not ObjId in hObjScore:
                hObjScore[ObjId] = score
            else:
                hObjScore[ObjId] += score
                
        lObjScore = hObjScore.items()
        lObjScore.sort(key=lambda item:item[1],reverse = True)
        lObjScore = lObjScore[:self.MaxNodePerGraph]
        
        
#         sObjId = set([item[0] for item in lAna])
        DocKg.hNodeId = dict(zip([item[0] for item in lObjScore],range(len(lObjScore))))
        DocKg.vNodeWeight = np.array([item[1] for item in lObjScore])
        
#         Z = np.sum(DocKg.vNodeWeight)
#         if Z != 0:
#             DocKg.vNodeWeight /= Z 
            
        DocKg.mEdgeMatrix = np.zeros([len(lObjScore),len(lObjScore)])
        
        return DocKg
    
    
class DocKGFaccFormerC(DocKGAnaFormerC):
    '''
    I fill doc's kg using FACC1 annotation
        node score = \sum_mention confidence score
    using the prepared facc doc annotation dict
    '''
        
    def SetConf(self, ConfIn):
        DocKGAnaFormerC.SetConf(self, ConfIn)
        FaccDictInName = self.conf.GetConf('faccdictin')
        self.hDocAna = pickle.load(open(FaccDictInName))
        
    @staticmethod
    def ShowConf():
        DocKGUnsupervisedFormerC.ShowConf()
        print 'faccdictin'
        
 
    
    
    
class DocKGTagMeFormerC(DocKGAnaFormerC):
    '''
    I fill doc's kg using TagMe annotation
        node score = \sum_mention confidence score
    '''
    def Init(self):
        DocKGAnaFormerC.Init(self)
        self.TagMeResIn = ""
    
    @staticmethod
    def ShowConf():
        DocKGAnaFormerC.ShowConf()
        print 'taggeddoc'
        
    def SetConf(self, ConfIn):
        DocKGAnaFormerC.SetConf(self, ConfIn)
        
        self.TagMeResIn = self.conf.GetConf('taggeddoc')
        self.FormTagMeDict()
        return
    
    def FormTagMeDict(self):
        '''
        form the doc no -> [[fb id,name,score],] dict
        '''
        
        for line in open(self.TagMeResIn):
            vCol = line.strip().split('\t')
            DocNo = vCol[0]
            vCol = vCol[1:]
            lAna = []
            for i in range((len(vCol)) / 8):
                FbObjId = vCol[i * 8 + 6]
                FbName = vCol[i * 8 + 7]
                score = float(vCol[i * 8 + 4])
                lAna.append([FbObjId,FbName,score])
#                 logging.debug('[%s][%s][%f] in %s',FbObjId,FbName,score,json.dumps(vCol))
            self.hDocAna[DocNo] = lAna
        
        return
    

        
        
        
        
        
        
    
        
    
    
    
    
    
        
