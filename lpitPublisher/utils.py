
from pathlib import Path
import sys
import tomllib
import yaml

from markdown import markdown

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

def loadMetaData(config) :

  metaData = {}
  for aLpitPath in config.lpitCache.glob("*.yaml") :
    theDoc = aLpitPath.name.replace('.yaml','')
    if theDoc not in metaData : metaData[theDoc] = {}
    lpitDef = yaml.safe_load(aLpitPath.read_text())
    if 'abstract' in lpitDef :
      lpitDef['abstract'] = markdown(lpitDef['abstract'])
    metaData[theDoc]['lpit'] = lpitDef

  for aPdfPath in config.pdfCache.glob("*.pdf") :
    theDoc = aPdfPath.name.replace('.pdf','')
    if theDoc not in metaData :
      die(f"Document: {theDoc} missing from LPiT definitions (addiing pdf)")
    metaData[theDoc]['pdf'] = aPdfPath.name

  for aMetaDataPath in config.metaDataCache.glob("*.yaml") :
    theDoc = aMetaDataPath.name.replace(".yaml", '')
    if theDoc not in metaData :
      die(f"Document: {theDoc} missing from LPiT definitions (loading metaData)")  # noqa
    docMetaData = yaml.safe_load(aMetaDataPath.read_text())
    metaData[theDoc]['metaData'] = docMetaData

  for aMarkdownPath in config.markdownCache.rglob("*.md") :
    theDoc = aMarkdownPath.parent.name
    theMarkdown = aMarkdownPath.name.replace('.md','')
    if theMarkdown.lower() == 'license' : continue
    if theDoc not in metaData :
      die(f"Document: {theDoc} missing from LPiT definitions (adding markdown)")  # noqa
    if 'markdown' not in metaData[theDoc] :
      metaData[theDoc]['markdown'] = {}
    mdHtml = markdown(aMarkdownPath.read_text())
    metaData[theDoc]['markdown'][theMarkdown] = mdHtml

  if config['verbose'] : print(yaml.dump(metaData))

  return metaData

