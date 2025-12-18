
# import yaml

from lpitPublisher.jinjaUtils import getTemplate, renderTemplate, \
  compileKeyLevels, createRedirects

keysToIgnore = [
  'docId',
  'inputs',
  'longTitle',
  'queries',
  'shortTitle',
]

def collectLabels(rawMD, config) :

  labels = {}

  for aDocKey, aDocDef in rawMD.items() :
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

def renderLabelIndex(metaData, config) :
  labels = collectLabels(metaData, config)
  labelLevels = compileKeyLevels(
    sorted(labels.keys()), config['indexLevels']['labels']
  )

  createRedirects(
    labels,
    config.webSiteCache / 'labels',
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
      'labelLevels' : labelLevels,
    },
    verbose=config['verbose']
  )
  labelIndexPath = config.webSiteCache / 'labelIndex.html'
  labelIndexPath.write_text(labelIndexHtml)

