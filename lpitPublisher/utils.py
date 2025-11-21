
from pathlib import Path
import sys
import tomllib
import yaml

def die(mesg) :
  print(mesg)
  sys.exit(1)

localLpitYamlPath = Path('lpit.yaml')
stylesDir = Path(__file__).parent.parent / 'styles'

def loadLpitYaml(docDir=None) :
  lpitYamlPath = Path(str(localLpitYamlPath))
  if docDir :
    lpitYamlPath = docDir / str(localLpitYamlPath)
  lpitYamlPath = lpitYamlPath.expanduser()

  lpitDef = {}
  try :
    lpitDef = yaml.safe_load(lpitYamlPath.read_text())

    if 'packages' not in lpitDef : lpitDef['packages'] = []

    # if lpitDef :
    #   print(yaml.dump(lpitDef))
  except FileNotFoundError :
    return {}
  except Exception as err :
    print("Could not load the document's lpit.yaml file")
    print(repr(err))
    sys.exit(1)

  if 'doc' not in lpitDef :
    return lpitDef

  lpitDoc = lpitDef['doc']
  if 'name' not in lpitDoc :
    if 'id' not in lpitDoc :
      die("No doc:id specified in the `lpit.yaml` file")
    lpitDoc['name'] = lpitDoc['id']
    if '-' in lpitDoc['name'] :
      lpitDoc['name'] = lpitDoc['name'].split('-')[1]

  return lpitDef

def getStyleDir(lpitDef) :
  return stylesDir / lpitDef['doc']['type']

def loadStyleInfo(lpitDef) :
  styleInfoPath = getStyleDir(lpitDef) / 'typst.toml'

  try :
    styleInfo = tomllib.loads(styleInfoPath.read_text())
    styleInfo = styleInfo['package']
  except Exception as err :
    print("Could not load this style's typst.toml file")
    print(repr(err))
    sys.exit(1)
  return styleInfo

