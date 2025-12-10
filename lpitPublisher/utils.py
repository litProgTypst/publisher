
from pathlib import Path
import sys
import tomllib
import yaml

from markdown import markdown

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

def loadMetaData(config) :

  metaData = {}
  for aLpitPath in config.lpitCache.glob("*.yaml") :
    theDoc = aLpitPath.name.replace('.yaml','')
    if theDoc not in metaData : metaData[theDoc] = {}
    lpitDef = yaml.safe_load(aLpitPath.read_text())
    if 'docOrderPriority' not in lpitDef :
      lpitDef['docOrderPriority'] = 0
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

def metaDataSortKey(anItem) :
  # print(f" {anItem['lpit']['doc']['name']}: {anItem['lpit']['docOrderPriority']}")  # noqa
  return float(anItem['lpit']['docOrderPriority'])

def sortDocuments(metaData) :
  docItems = []
  for aKey in sorted(metaData.keys()) :
    anItem = metaData[aKey]
    anItem['key'] = aKey
    docItems.append(anItem)

  sortedDocNames = []
  for anItem in sorted(docItems, key=metaDataSortKey, reverse=True) :
    sortedDocNames.append(anItem['key'])

  return sortedDocNames

