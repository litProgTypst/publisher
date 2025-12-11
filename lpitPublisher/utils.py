
from pathlib import Path
import sys
import tomllib

def die(mesg) :
  print(mesg)
  sys.exit(1)

stylesDir = Path(__file__).parent.parent / 'styles'

def getStyleDir(lpitDef) :
  return stylesDir / lpitDef['doc']['type']

def loadStyleInfo(lpitDef) :
  styleInfoPath = getStyleDir(lpitDef) / 'typst.toml'

  try :
    styleInfo = tomllib.loads(styleInfoPath.read_text())
    styleInfo = styleInfo['package']
  except Exception as err :
    print(f"Could not load the {getStyleDir(lpitDef).name} style's typst.toml file")  # noqa
    print(repr(err))
    sys.exit(1)
  return styleInfo


