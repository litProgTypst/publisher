#!/usr/bin/env python

# for configuration we will use TOML
# we will read the Typst MetaData as JSON strings.

# This python script walks through (sub)directories looking for git
# managed directories. Once a directory is found which is managed by git,
# it reports the current status of the directory and whether or not the
# default "remote" is up to date

# The asyncio worker pattern is based on:
# https://stackoverflow.com/a/63977974
# and/or Python Asyncio Queue example:
# https://docs.python.org/3/library/asyncio-queue.html#asyncio-queues

import asyncio
import os
from pathlib import Path
import re
import time

######################################################################
# regular expressions

remoteFetchErrorARegExp = re.compile(r"error: Could not fetch origin")
remoteFetchErrorBRegExp = re.compile(r"ERROR: Repository not found")
gitStatusErrorARegExp   = re.compile(r"nothing to commit\, working .* clean")
gitStatusErrorB1RegExp  = re.compile(r"Your branch")
gitStatusErrorB2RegExp  = re.compile(r"is up.to.date")

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

async def checkARepo(workerId, repoQueue, repoResults) :
  while 0 < repoQueue.qsize() :
    aRepo = await repoQueue.get()
    try :
      headFile = aRepo / 'HEAD'
      head = headFile.read_text(encoding='utf-8').split()
      if 1 < len(head) :
        head = head[1].split('/').pop()
      else :
        head = head[0]

      aRepo = aRepo.parent
      print(f"({workerId})<{repoQueue.qsize()}>[{head}]  {aRepo}")

      fetchUrlStdout, fetchUrlStderr = await runShellCmdIn(
        "git remote show origin | grep Fetch",
        aRepo
      )

      remoteUpdateStdout, remoteUpdateStderr = await runShellCmdIn(
        "git remote update",
        aRepo
      )

      gitStatusStdout, gitStatusStderr = await runShellCmdIn(
        "git status",
        aRepo
      )

      errorReport = None
      if remoteFetchErrorARegExp.search(remoteUpdateStdout) :
        errorReport = remoteUpdateStdout.strip()
      if remoteFetchErrorBRegExp.search(remoteUpdateStderr) :
        errorReport = remoteUpdateStderr.strip()
      elif not gitStatusErrorARegExp.search(gitStatusStdout) :
        errorReport = gitStatusStdout.strip()
      elif gitStatusErrorB1RegExp.search(gitStatusStdout) :
        if not gitStatusErrorB2RegExp.search(gitStatusStdout) :
          errorReport = gitStatusStdout.strip()

      aRepoResults = {
        'repo'           : str(aRepo),
        'head'           : head,
        'errorReport'    : errorReport,
        'fetchUrlStdout' : fetchUrlStdout.strip(),
      }
      repoResults[str(aRepo)] = aRepoResults
    except Exception as err :
      print(repr(err))

    repoQueue.task_done()

async def checkRepoList(someRepos, repoResults) :
  repoQueue   = asyncio.Queue()

  for aRepo in someRepos :
    await repoQueue.put(aRepo)

  workers = []
  for i in range(50) :
    aWorker = asyncio.create_task(
      checkARepo(i, repoQueue, repoResults)
    )
    workers.append(aWorker)

  await asyncio.gather(*workers, return_exceptions=True)

######################################################################
# load the configuration

os.system("clear")

print("Checking git repositories")

# os.system("useKeyStandard")
os.system("useKeyGit")

gitCheckerDir = Path.home() / '.gitChecker'
gitCheckerConfig = gitCheckerDir / 'config.yaml'
if not gitCheckerDir.exists() :
  gitCheckerDir.mkdir()
  gitCheckerConfig.write_text("""dirs:
  -  '.'
""", encoding='utf-8')

config = yaml.safe_load(gitCheckerConfig.read_text(encoding='utf-8'))
print("")
print("------------------------------------------------------------")
print("Configuration:")
print("-------")
print(yaml.dump(config))
print("------------------------------------------------------------")
print("")

######################################################################
# find repositories

startTime = time.time()
print("started: {}".format(time.ctime(startTime)))
print("")
gitDirs = list(config['dirs'])
gitDirs.sort()
repos = []
for aGitDir in gitDirs :
  aGitDir = Path(aGitDir)
  print(f"collecting git repositories in: {aGitDir}")
  repos.extend(list(aGitDir.glob("**/.git")))

print("")

repos.sort()
repoResults = { }
asyncio.run(checkRepoList(repos, repoResults))

reposList = list(repoResults.keys())
reposList.sort()
for theRepo in reposList :
  theRepoResults = repoResults[theRepo]
  if theRepoResults['errorReport'] :
    print("\n------------------------------------------------------------")
    print("[{}] {}".format(
      theRepoResults['head'],
      theRepoResults['repo'],
    ))
    print(repoResults[theRepo]['errorReport'])

print("")
endTime = time.time()
print("finished: {}".format(time.ctime(endTime)))
print("Total:    {} seconds".format(
  format(endTime - startTime, ".2f")
))
print("")
