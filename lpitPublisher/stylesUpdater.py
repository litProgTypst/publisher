
from pathlib import Path
import re
import sys
# import yaml

from lpitPublisher.utils import loadLpitYaml, loadStyleInfo

def usage() :
  print("""
    lpitStyleUpdate [-h, --help]

    where:
      -h, --help          prints this text

    All typst documents found (recursively) will have the appropriate LPiT
    style updated to the most recent verion.

  """)
  sys.exit(0)

def cli() :
  if 1 < len(sys.argv) :
    usage()

  lpitDef = loadLpitYaml()

  styleInfo = loadStyleInfo(lpitDef)
  versionRegExp = re.compile(styleInfo['name'] + '.*"')

  print(f"Updating documents to use {styleInfo['name']} version {styleInfo['version']}\n")  # noqa
  docRoot = Path('.')
  for aDoc in docRoot.rglob('*.typ') :
    print(f"Updating the version in:\n  {aDoc}")
    origText = aDoc.read_text()
    for aMatch in versionRegExp.findall(origText) :
      if aMatch :
        newText = origText.replace(
          str(aMatch),
          styleInfo['name'] + ':' + styleInfo['version'] + '"'
        )
        aDoc.write_text(newText)

