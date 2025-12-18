
import yaml

from lpitPublisher.jinjaUtils import getTemplate, renderTemplate, \
  compileKeyLevels, createRedirects

keysToIgnore = [
  'docId',
  'inputs',
  'longTitle',
  'queries',
  'shortTitle',
]

def collectLabels(metaData) :

  labels = {}

  for aDocKey, aDocDef in metaData.items() :
    aDocMD = aDocDef['metaData'][0]['value']
    for aKey in aDocMD.keys() :
      if aKey in keysToIgnore : continue
      for anItem in aDocMD[aKey] :
        if 'label' not in anItem : continue
        itemLabel = anItem['label']
        if itemLabel == 'none' : continue

        # found a valid label record it
        itemLabel = itemLabel.strip('<>')
        if itemLabel not in labels :
          labels[itemLabel] = []
        labels[itemLabel].append(( aDocKey, anItem['label'], anItem['page']))

  return labels

def collectReferences(metaData, config) :
  references = {}

  collectionUrls = []
  for aProject, projDef in config['projects'].items() :
    if 'url' in projDef :
      collectionUrls.append(projDef['url'])

  for aDocKey, aDocDef in metaData.items() :
    aDocMD = aDocDef['metaData'][0]['value']
    for aRef in aDocMD['ref'] :
      label = aRef['target'].strip('<>')
      page  = aRef['page']
      if label not in references :
        references[label] = []
      references[label].append((aDocKey, label, page, 'ref'))
    for aLink in aDocMD['link'] :
      destBody = None
      for aUrl in collectionUrls :
        if aLink['dest'].startswith(aUrl) :
          destBody = aLink['dest'].removeprefix(aUrl)
          break
      if not destBody : continue
      destParts = destBody.split('/')
      label = destParts[3]
      page  = aLink['page']
      if label not in references :
        references[label] = []
      references[label].append((aDocKey, label, page, 'link'))

  print(yaml.dump(references))

  return references

def renderLabelIndex(metaData, config) :
  labels = collectLabels(metaData)
  labelLevels = compileKeyLevels(
    sorted(labels.keys()), config['indexLevels']['labels']
  )
  references = collectReferences(metaData, config)

  createRedirects(
    labels,
    config.webSiteCache / 'labels',
    config['verbose']
  )

  createRedirects(
    references,
    config.webSiteCache / 'references',
    config['verbose']
  )

  template = getTemplate('labelTargetIndex.html')

  for aLabel, someTargets in labels.items() :
    docPages = {}
    for aTarget in someTargets :
      docId, tLabel, page = aTarget
      if docId not in docPages :
        docPages[docId] = []
      docPages[docId].append(page)

    for aDoc, somePages in docPages.items() :
      labelTargetHtml = renderTemplate(
        template,
        {
          'docPages' : somePages,
          'docId'    : docId,
          'label'    : aLabel
        },
        verbose=config['verbose']
      )
      labelTargetPath = config.webSiteCache / 'labels' / aDoc / aLabel / 'index.html'  # noqa
      labelTargetPath.parent.mkdir(parents=True, exist_ok=True)
      labelTargetPath.write_text(labelTargetHtml)

  template = getTemplate('labelIndex.html')

  labelIndexHtml = renderTemplate(
    template,
    {
      'labelsDesc'  : config.labelsDesc,
      'labels'      : labels,
      'references'  : references,
      'labelLevels' : labelLevels,
    },
    verbose=config['verbose']
  )
  labelIndexPath = config.webSiteCache / 'labelIndex.html'
  labelIndexPath.write_text(labelIndexHtml)

