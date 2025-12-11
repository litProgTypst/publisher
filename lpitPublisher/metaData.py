
import copy
import yaml

from markdown import markdown

from lpitPublisher.utils import die

def filterQueryData(rawMD) :
  # setup
  metaData = rawMD[0]['value']
  if 'heading'      not in metaData : metaData['heading']      = []
  if 'ref'          not in metaData : metaData['ref']          = []
  if 'cite'         not in metaData : metaData['cite']         = []
  if 'figure'       not in metaData : metaData['figure']       = []
  if 'table'        not in metaData : metaData['table']        = []
  if 'link'         not in metaData : metaData['link']         = []
  if 'footnote'     not in metaData : metaData['footnote']     = []
  if 'bibliography' not in metaData : metaData['bibliography'] = []
  if 'outline'      not in metaData : metaData['outline']      = []

  # do the work
  queryData = metaData['queries']
  for aQData in queryData :
    metaData[aQData['data']['func']].append(copy.deepcopy(aQData))
  return rawMD

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
    metaData[theDoc]['metaData'] = filterQueryData(docMetaData)

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

