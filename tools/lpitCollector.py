#!/usr/bin/env python

# for configuration we will use TOML
# we will read the Typst MetaData as JSON strings.

# This python script walks through a list of Typst Publisher documents
# collecting metadata for the publisher. The resulting metadata is stored
# in the `base` directory in the `metadata` subdirectory. This metadata
# can then be used by the publisher to maintain various tables.

# The asyncio worker pattern is based on:
# https://stackoverflow.com/a/63977974
# and/or Python Asyncio Queue example:
# https://docs.python.org/3/library/asyncio-queue.html#asyncio-queues

import asyncio
import json
import os
from pathlib import Path
# import re
import sys
import time
import tomllib

######################################################################
# check a single repo

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

async def getDocumentMetadata(workerId, docQueue, metadata) :
  while 0 < docQueue.qsize() :
    aDoc = await docQueue.get()
    try :

      # EVENTUALLY we want to read all (sub)typst documents looking for
      # `#import` or `#include` statements. This will allow us to cache
      # the metadata results based upon included file modification times.
      # If none of the included files have changed, then we do not need to
      # re-collect the metadata.

      rootDir      = aDoc.parent
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

async def collectDocumentMetadata(documents, metadata) :
  docQueue   = asyncio.Queue()

  for aDoc in documents :
    await docQueue.put(aDoc)

  workers = []
  for i in range(5) :
    aWorker = asyncio.create_task(
      getDocumentMetadata(i, docQueue, metadata)
    )
    workers.append(aWorker)

  await asyncio.gather(*workers, return_exceptions=True)

def usage() :
  print(f"""
  usage: {sys.argv[0]} [options] <collectionToml>

  where <collectionToml> is the TOML file describing the ordered
  collection of documents to be published.

  Options:
    -h, --help     Print this help text
    -v, --verbose  Be verbose

""")
  sys.exit(1)

######################################################################
# load the configuration

os.system("clear")

if len(sys.argv) < 2 :
  usage()

tomlPath = Path(sys.argv[-1], 'lpitPublisher.toml')

print(f"Collecting lpit published parts from {tomlPath}")

config = tomllib.loads(tomlPath.read_text(encoding='utf-8'))
print("")
print("------------------------------------------------------------")
print("Configuration:")
print("-------")
print(json.dumps(config, sort_keys=True, indent=2))
print("------------------------------------------------------------")
print("")

######################################################################
# find typst documents

startTime = time.time()
print(f"started: {time.ctime(startTime)}")
print("")
collections = list(config['collection'])
documents = []
for docInfo in collections :
  aDocPath = Path(docInfo['path'], docInfo['doc'])
  print(f"collecting Publisher metadata from: {aDocPath}")
  documents.append(aDocPath)
print("")

metadata = {}
asyncio.run(collectDocumentMetadata(documents, metadata))

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
