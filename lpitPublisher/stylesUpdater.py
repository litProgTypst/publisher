
from pathlib import Path
import re
import sys
import yaml

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

  packages = lpitDef['packages']
  packages.insert(0, {
    'name' : styleInfo['name'],
    'version' : styleInfo['version']
  })

  print("Updating the following packages in this document")
  print(yaml.dump(packages))
  print("")

  docRoot = Path('.')
  for aDoc in docRoot.rglob('*.typ') :
    print(f"Updating packages in:\n  {aDoc}")
    newText = aDoc.read_text()
    for aPackage in packages :
      print(f"  - {aPackage['name']} ({aPackage['version']})")
      if 'regExp' not in aPackage :
        aPackage['regExp'] = re.compile(
          aPackage['name'] + '.*"'
        )
      for aMatch in aPackage['regExp'].findall(newText) :
        if aMatch :
          newText = newText.replace(
            str(aMatch),
            aPackage['name'] + ':' + aPackage['version'] + '"'
          )
    aDoc.write_text(newText)

