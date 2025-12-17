
import argparse
import os

from lpitPublisher.config import addConfigurationArgs, Config
from lpitPublisher.utils import die

def parseArgs() :
  parser = argparse.ArgumentParser(
    prog='lpitDeploy',
    description="""
      Deploy the recently generated website.
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
  config.checkDocumentDirs()

  if 'remoteDeployPath' not in config :
    die("No deploy path has been configured... nothing to do!")
  deployPath = config['remoteDeployPath']

  if 'preDeployCmds' in config :
    preDeployCmds = config['preDeployCmds']
    for aCmd in preDeployCmds :
      os.system(aCmd)

  os.system(f"rsync -av {config.webSiteCache}/ {deployPath}")

  if 'postDeployCmds' in config :
    postDeployCmds = config['postDeployCmds']
    for aCmd in postDeployCmds :
      os.system(aCmd)

