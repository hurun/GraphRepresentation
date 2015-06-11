'''
Created on my MAC Jun 10, 2015-4:09:47 PM
What I do:
extract obj-obj from original knowledge graph
What's my input:
obj obj
What's my output:
hFeature
@author: chenyanxiong
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

import os
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging
from EdgeFeatureExtraction.ObjObjEdgeFeatureExtractor import ObjObjEdgeFeatureExtractorC

class ObjObjEdgeFeatureKGExtractorC(ObjObjEdgeFeatureExtractorC):
    
    def Init(self):
        ObjObjEdgeFeatureExtractorC.Init(self)
        self.FeatureName += 'KG'
        
        
    def process(self, ObjA, ObjB):
        hFeature = {}
        
        hFeature.update(self.ExtractDirectConnectFeature(ObjA,ObjB))
        
        hFeature.update(self.ExtractTwoHopFeature(ObjA,ObjB))   #the longest path useful in literature is only two hop
        
        return hFeature
    
    
    def ExtractDirectConnectFeature(self,ObjA,ObjB):
        hFeature = {}
        
        lObjANeighbor = ObjA.GetField('Neighbor')
        
        hNeighborId = dict([item[1].GetId() for item in lObjANeighbor])
        
        FeatureName = self.FeatureName + 'Connected'
        score = 0
        if ObjB.GetId() in hNeighborId:
            score = 1
        hFeature[FeatureName] = score
        
        
        FeatureName = self.FeatureName + 'HopOneProb'
        score = 0
        if ObjB.GetId() in hNeighborId:
            score = 1.0 / float(len(hNeighborId))
        hFeature[FeatureName] = score
        
        return hFeature
    
    def ExtractTwoHopFeature(self,ObjA,ObjB):
        hFeature = {}
        
        lObjANeighbor = ObjA.GetNeighbor()
        hANeighborId = dict([item[1].GetId() for item in lObjANeighbor])
        lObjBNeighbor = ObjB.GetNeighbor()
        hBNeighborId = dict([item[1].GetId() for item in lObjBNeighbor])
        
        FeatureName = 'CommonNeighborFrac'
        score = 0
            
        
        for ObjId in hANeighborId.keys():
            if ObjId in hBNeighborId:
                score += 1
                break
        if len(hANeighborId) != 0:
            score /= len(hANeighborId)
            
        hFeature[FeatureName] = score
        return hFeature
        
                
        
        
        
        
        
        
        
        