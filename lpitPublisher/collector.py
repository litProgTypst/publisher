
import argparse
import sys
import yaml

from lpitPublisher.config import addConfigurationArgs, Config

#######################################################
# Provide the command line interface

def parseArgs() :
  parser = argparse.ArgumentParser(
    prog='lpitCollector',
    description="""
      Collect the meta-data for all configured LPiT documents
    """,
    epilog="""something..."""
  )

  addConfigurationArgs(parser)

  return vars(parser.parse_args())

def cli() :
  print(yaml.dump(sys.argv))
  config = Config()
  args = parseArgs()
  print(yaml.dump(args))
  config.loadConfig(args)
  config.print()

#######################################################
# Run the app if called as a main
if __name__ == "__main__":
  cli()

