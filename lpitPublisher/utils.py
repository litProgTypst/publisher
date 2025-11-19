
from pathlib import Path
import sys
import tomllib
import yaml

from jinja2 import Template

lpitYamlPath = Path('lpit.yaml')
stylesDir = Path(__file__).parent.parent / 'styles'
lpitYamlTemplate = stylesDir / 'lpitYaml.jinja2'

def createLpitYamlFile(lpitYamlPath) :
  try :
    print("Creating a new LPiT.yaml file")
    templateStr = lpitYamlTemplate.read_text()
    template    = Template(templateStr)
    lpitYamlStr = template.render()
    lpitYamlPath.write_text(lpitYamlStr)
    print("""

      Now PLEASE update the values in this new `lpit.yaml` file to
      represent your new document.

    """)
  except Exception as err :
    print("Could not create the document's lpit.yaml file")
    print(repr(err))

def loadLpitYaml() :
  lpitDef = {}
  try :
    lpitDef = yaml.safe_load(lpitYamlPath.read_text())
    # if lpitDef :
    #   print(yaml.dump(lpitDef))
  except FileNotFoundError :
    createLpitYamlFile(lpitYamlPath)
    sys.exit(0)
  except Exception as err :
    print("Could not load the document's lpit.yaml file")
    print(repr(err))
    sys.exit(1)
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

