
import argparse
import asyncio
import json
import os
from pathlib import Path
# import sys
import time
# import yaml

from lpitPublisher.config import addConfigurationArgs, Config
from lpitPublisher.utils import loadLpitYaml

######################################################################
# asynchronously check a single document

async def runShellCmdIn(aCmd, aDir) :
  aProc = await asyncio.create_subprocess_shell(
    aCmd,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
    cwd=str(aDir)
  )

  aProcStdout, aProcStderr = await aProc.communicate()
  return (
    aProcStdout.decode(encoding="utf-8"),
    aProcStderr.decode(encoding="utf-8"),
  )

async def getDocumentMetadata(workerId, docQueue, config, metadata) :
  while 0 < docQueue.qsize() :
    aDoc = await docQueue.get()
    try :

      # EVENTUALLY we want to read all (sub)typst documents looking for
      # `#import` or `#include` statements. This will allow us to cache
      # the metadata results based upon included file modification times.
      # If none of the included files have changed, then we do not need to
      # re-collect the metadata.

      rootDir     = aDoc.parent
      docFileName = aDoc.name
      print(f"({workerId})<{docQueue.qsize()}>  {rootDir} {docFileName}")

      typstStdout, typstStderr = await runShellCmdIn(
        f"typst query --input metadata=1 {docFileName} \"<lpitMetaData>\"",
        rootDir
      )

      # errorReport = None
      # if remoteFetchErrorARegExp.search(remoteUpdateStdout) :
      #   errorReport = remoteUpdateStdout.strip()
      # if remoteFetchErrorBRegExp.search(remoteUpdateStderr) :
      #   errorReport = remoteUpdateStderr.strip()
      # elif not gitStatusErrorARegExp.search(gitStatusStdout) :
      #   errorReport = gitStatusStdout.strip()
      # elif gitStatusErrorB1RegExp.search(gitStatusStdout) :
      #   if not gitStatusErrorB2RegExp.search(gitStatusStdout) :
      #     errorReport = gitStatusStdout.strip()

      typstResults = {
        'rootDir' : str(rootDir),
        'doc'     : str(docFileName),
        'stdout'  : typstStdout,
        'stderr'  : typstStderr
      }
      metadata[str(aDoc)] = typstResults
    except Exception as err :
      print(repr(err))

    docQueue.task_done()

######################################################################
# asynchronously check the listed documents

async def collectDocumentMetadata(documents, config, metadata) :
  docQueue   = asyncio.Queue()

  for aDoc in documents :
    await docQueue.put(aDoc)

  workers = []
  if 'numWorkers' not in config :
    config['numWorkers'] = 5
  for i in range(config['numWorkers']) :
    aWorker = asyncio.create_task(
      getDocumentMetadata(i, docQueue, config, metadata)
    )
    workers.append(aWorker)

  await asyncio.gather(*workers, return_exceptions=True)

######################################################################
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
  os.system("reset")

  config = Config()
  args = parseArgs()
  config.loadConfig(args)

  documents = []
  for aDir in config['documentDirs'] :
    aDir = Path(aDir).expanduser()
    print(f"Looking for LPiT documents in {aDir}")
    for aLpitYaml in aDir.rglob("lpit.yaml") :
      docDir = aLpitYaml.parent
      print(f"  found: {aLpitYaml}")
      lpitDef = loadLpitYaml(docDir=docDir)
      if not lpitDef : continue

      docName = lpitDef['doc']['name']
      if not docName.endswith('.typ') :
        docName = docName + '.typ'
      documents.append(docDir / docName)

  startTime = time.time()
  print(f"started: {time.ctime(startTime)}")

  print("")

  metadata = {}
  asyncio.run(collectDocumentMetadata(documents, config, metadata))

  print("")

  for someMetaData in metadata.keys() :
    print(json.dumps(metadata[someMetaData], indent=2))

  print("")

  endTime = time.time()
  print(f"finished: {time.ctime(endTime)}")
  print( "Total:    {} seconds".format(
    format(endTime - startTime, ".2f")
  ))
  print("")

######################################################################
# Run the app if called as a main
if __name__ == "__main__":
  cli()

