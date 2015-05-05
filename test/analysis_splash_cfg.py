#------------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------------

import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

#------------------------------------------------------------------------------------
# Options
#------------------------------------------------------------------------------------

options = VarParsing.VarParsing()

options.register('skipEvents',
                 0, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Number of events to skip")

options.register('processEvents',
                 0, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Number of events to process")

options.register('inputFiles',
                 "file:inputFile.root", #default value
                 VarParsing.VarParsing.multiplicity.list,
                 VarParsing.VarParsing.varType.string,
                 "Input files")

options.register('outputFile',
                 "file:outputFile.root", #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Output file")

options.parseArguments()

print "Skip events =", options.skipEvents
print "Process events =", options.processEvents
print "inputFiles =", options.inputFiles
print "outputFile =", options.outputFile

#------------------------------------------------------------------------------------
# Declare the process
#------------------------------------------------------------------------------------

process = cms.Process('PFG')

#------------------------------------------------------------------------------------
# Set up the input source
#------------------------------------------------------------------------------------

process.source = cms.Source("PoolSource")

#------------------------------------------------------------------------------------
# What files should we run over?
#------------------------------------------------------------------------------------

process.source = cms.Source("PoolSource", 
   fileNames = cms.untracked.vstring(
       options.inputFiles
   ),
   skipEvents = cms.untracked.uint32(
       options.skipEvents
   )
)

#------------------------------------------------------------------------------------
# How many events should we run over?
#------------------------------------------------------------------------------------

process.maxEvents = cms.untracked.PSet(
   input = cms.untracked.int32(
       options.processEvents
   )
)

#------------------------------------------------------------------------------------
# Set up the output
#------------------------------------------------------------------------------------

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string( options.outputFile )
)

#------------------------------------------------------------------------------------
# Various python configuration files below
# 
# Used the following cmsDriver command:
# cmsDriver.py reco \
# -s RAW2DIGI,L1Reco,RECO \
# --conditions GR_P_V49 \
# --eventcontent RECO \
# --magField=38T_PostLS1 \
# --scenario=cosmics \
# --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 
# --filein=root://eoscms//eos/cms/store/data/Commissioning2014/Cosmics/RAW/v3/000/229/713/00000//0A23AFDB-5B6A-E411-A4D1-02163E010DDF.root \
# --no_exec
#------------------------------------------------------------------------------------

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContentCosmics_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.ReconstructionCosmics_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')

# Set up cosmic digis
process.load("HCALPFG.HcalTupleMaker.HcalCosmicDigisProducer_cfi")

# Set up L1 Jet digis
process.load("HCALPFG.HcalTupleMaker.HcalL1JetDigisProducer_cfi")

# Set up our analyzer
process.load("HCALPFG.HcalTupleMaker.HcalTupleMaker_cfi")

# Global tag
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'GR_P_V50', '')

# New HO emap
process.es_pool = cms.ESSource("PoolDBESSource",
    process.CondDBSetup,
    timetype = cms.string('runnumber'),
    toGet = cms.VPSet(
        cms.PSet(
            record = cms.string("HcalElectronicsMapRcd"),
            tag = cms.string("HcalElectronicsMap_v7.00_offline")
        )
    ),
    connect = cms.string('frontier://FrontierPrep/CMS_COND_HCAL'),
    authenticationMethod = cms.untracked.uint32(0)
)
process.es_prefer_es_pool = cms.ESPrefer( "PoolDBESSource", "es_pool" )

process.hcalTupleHBHEDigis.recHits = cms.untracked.InputTag("hbheprereco")

#------------------------------------------------------------------------------------
# Define the tuple-making sequence
#------------------------------------------------------------------------------------
    
process.tuple_step = cms.Sequence(
    # Make HCAL tuples: Event, run, ls number
    process.hcalTupleEvent*
    # Make HCAL tuples: FED info
    process.hcalTupleFEDs*
    # Make HCAL tuples: digi info
    process.hcalTupleHBHEDigis*
    process.hcalTupleHODigis*
    process.hcalTupleHFDigis*
    process.hcalTupleTriggerPrimitives*
    # Trigger info
    process.hcalTupleTrigger*
    process.hcalTupleTriggerObjects*
    # Package everything into a tree
    process.hcalTupleTree
)

#------------------------------------------------------------------------------------
# Define the path
#------------------------------------------------------------------------------------

# Path and EndPath definitions
process.preparation = cms.Path(
    process.RawToDigi *
    process.hcalLocalRecoSequence *
    process.tuple_step
)


#------------------------------------------------------------------------------------
# Customize for the post-LS1 environment
#------------------------------------------------------------------------------------

from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 
process = customisePostLS1(process)


