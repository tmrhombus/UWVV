from UWVV.AnalysisTools.AnalysisFlowBase import AnalysisFlowBase

from UWVV.Utilities.helpers import parseChannels

import FWCore.ParameterSet.Config as cms


class BJetCounters(AnalysisFlowBase):
    def __init__(self, *args, **kwargs):
        super(BJetCounters, self).__init__(*args, **kwargs)


    def makeAnalysisStep(self, stepName, **inputs):
        step = super(BJetCounters, self).makeAnalysisStep(stepName, **inputs)
        
        if stepName == 'initialStateEmbedding':
            jetCounters = {'JPL' : '? bDiscriminator("pfJetProbabilityBJetTags")>0.245 ? 1 : 0',
                "JPM" : '? bDiscriminator("pfJetProbabilityBJetTags")>0.515 ? 1 : 0',
                "JPT" : '? bDiscriminator("pfJetProbabilityBJetTags")>0.760 ? 1 : 0',
                "CSVv2L" : '? bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")>0.460 ? 1 : 0',
                "CSVv2M" : '? bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")>0.800 ? 1 : 0',
                "CSVv2T" : '? bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")>0.935 ? 1 : 0',
                "CMVAv2L" : '? bDiscriminator("pfCombinedMVAV2BJetTags")>-0.715 ? 1 : 0',
                "CMVAv2M" : '? bDiscriminator("pfCombinedMVAV2BJetTags")>0.185 ? 1 : 0',
                "CMVAv2T" : '? bDiscriminator("pfCombinedMVAV2BJetTags")>0.875 ? 1 : 0',
            }
            mod = cms.EDProducer(
                "PATJetCounter",
                src = step.getObjTag('j'),
                labels = cms.vstring(*['nJet'+label for label in jetCounters.keys()]),
                cuts = cms.vstring(*[jetCounters[key] for key in jetCounters.keys()])
                )
            step.addModule("jetCounter", mod)

            labels = ['nJet'+name for name in jetCounters.keys()]
            tags = [cms.InputTag("jetCounter:nJet"+name) for name in jetCounters.keys()]

            for chan in parseChannels('zl'):
                countEmbedding = cms.EDProducer(
                    'PATCompositeCandidateValueEmbedder',
                    src = step.getObjTag(chan),
                    intLabels = cms.vstring(*labels),
                    intSrc = cms.VInputTag(*tags),
                    )
                step.addModule(chan+'JetCountEmbedding', countEmbedding, chan)

        return step

