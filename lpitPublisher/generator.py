
import argparse
import os

from lpitPublisher.config import addConfigurationArgs, Config
from lpitPublisher.utils import loadMetaData

######################################################################
# Provide the command line interface

def parseArgs() :
  parser = argparse.ArgumentParser(
    prog='lpitGenerator',
    description="""
      Use the collected meta-data to generate a static website for the
      collection of LPiT documents
    """,
    epilog="""something..."""
  )

  addConfigurationArgs(parser)

  return vars(parser.parse_args())

def cli() :
  os.system("reset")

  config = Config()
  args = parseArgs()
  config.loadConfig(args)

  loadMetaData(config)

