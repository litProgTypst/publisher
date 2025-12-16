
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

