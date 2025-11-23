
import argparse
import asyncio
import json
import os
from pathlib import Path
import shutil
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

      typstResults = {
        'rootDir' : str(rootDir),
        'doc'     : str(docFileName),
      }

      if 'metadata' in config['formats'] :
        queryStdout, queryStderr = await runShellCmdIn(
          f"typst query --format yaml --input metadata=1 {docFileName} \"<lpitMetaData>\"",  # noqa
          rootDir
        )

        if queryStdout :
          queryPath = config.metaDataCache / docFileName.replace('.typ', '.yaml')  # noqa
          queryPath.write_text(queryStdout)

        typstResults['query'] = {
          'stdout'  : queryStdout,
          'stderr'  : queryStderr
        }

      if 'pdf' in config['formats'] :
        pdfStdout, pdfStderr = await runShellCmdIn(
          f"typst compile --format pdf {docFileName} {config.pdfCache}/{docFileName.replace('.typ','.pdf')}",  # noqa
          rootDir
        )

        typstResults['pdf'] = {
          'stdout'  : pdfStdout,
          'stderr'  : pdfStderr
        }

      if 'svg' in config['formats'] :
        svgDocDir = config.svgCache / docFileName.replace('.typ','')
        svgDocDir.mkdir(parents=True, exist_ok=True)
        svgStdout, svgStderr = await runShellCmdIn(
          f"typst compile --format svg {docFileName} {svgDocDir}/page{{0p}}.svg",  # noqa
          rootDir
        )

        typstResults['svg'] = {
          'stdout'  : svgStdout,
          'stderr'  : svgStderr
        }

      if 'html' in config['formats'] :
        htmlStdout, htmlStderr = await runShellCmdIn(
          f"typst compile --format html --features html {docFileName} {config.htmlCache}/{docFileName.replace('.typ','.html')}",  # noqa
          rootDir
        )

        typstResults['html'] = {
          'stdout'  : htmlStdout,
          'stderr'  : htmlStderr
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
# check to see if a LPiT document has changed.
#
# We use a fairly crude but fast diff of
# past and present sha256sum files.

def documentFilesChanged(docPath, docName, config) :
  filesToCheck = []

  if not config['monitor'] : return True

  for aFileType in config['monitor'] :
    for aFile in docPath.rglob(aFileType) :
      filesToCheck.append(str(aFile))

  if not filesToCheck : return True

  filesToCheck = sorted(filesToCheck)

  newPath = Path('/tmp') / docName
  newFilesPath = newPath.with_suffix('.files')
  newSumsPath  = newPath.with_suffix('.sums')

  cachedPath     = config.shaSumsCache / docName
  cachedSumsPath = cachedPath.with_suffix('.sums')

  newFilesPath.write_text('\n'.join(filesToCheck))
  os.system(f"xargs -a {newFilesPath} sha256sum > {newSumsPath}")

  result = 1
  if cachedSumsPath.exists() :
    result = os.system(f"diff {cachedSumsPath} {newSumsPath}")

  shutil.move(newSumsPath, cachedSumsPath)

  if result != 0 : return True
  return False

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
  config.print()

  documents = []
  for aDir in config['documentDirs'] :
    aDir = Path(aDir).expanduser()
    print(f"Looking for LPiT documents in {aDir}")
    for aLpitYaml in aDir.rglob("lpit.yaml") :
      print(f"  found: {aLpitYaml}")

      docDir = aLpitYaml.parent

      lpitDef = loadLpitYaml(docDir=docDir)
      if not lpitDef : continue

      docName = lpitDef['doc']['name']
      if not docName.endswith('.typ') :
        docName = docName + '.typ'

      if not documentFilesChanged(docDir, docName, config) : continue

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

