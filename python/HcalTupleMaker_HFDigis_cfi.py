import FWCore.ParameterSet.Config as cms

hcalTupleHFDigis = cms.EDProducer("HcalTupleMaker_HFDigis",
  source  = cms.untracked.InputTag("hcalDigis"),
  recHits = cms.untracked.InputTag("hfreco"),
  Prefix  = cms.untracked.string ( "HFDigi"),
  Suffix  = cms.untracked.string ( ""),
  DoChargeReco = cms.untracked.bool ( True ) ,
  DoEnergyReco = cms.untracked.bool ( True ) 
)

hcalTupleHFUTCADigis = cms.EDProducer("HcalTupleMaker_HFDigis",
  source  = cms.untracked.InputTag("utcaDigis"),
  recHits = cms.untracked.InputTag("hfreco"),
  Prefix  = cms.untracked.string ( "HFUTCADigi"),
  Suffix  = cms.untracked.string ( ""),
  DoChargeReco = cms.untracked.bool ( True ) ,
  DoEnergyReco = cms.untracked.bool ( True ) 
)

hcalTupleHFL1JetsDigis = cms.EDProducer("HcalTupleMaker_HFDigis",
  source  = cms.untracked.InputTag("hcalL1JetDigis"),
  recHits = cms.untracked.InputTag("hfreco"),
  Prefix  = cms.untracked.string ( "HFL1JetDigi"),
  Suffix  = cms.untracked.string ( ""),
  DoChargeReco = cms.untracked.bool ( True ) ,
  DoEnergyReco = cms.untracked.bool ( True ) 
)
