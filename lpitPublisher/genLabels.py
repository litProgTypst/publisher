
import yaml

from markdown import markdown

from lpitPublisher.jinjaUtils import getTemplate, renderTemplate, \
  compileKeyLevels

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

def createLabelRedirects(labels, config) :
  template = getTemplate('redirect.html')

  for labelKey, labelDef in labels.items() :
    for labelTarget in labelDef :
      theDoc = labelTarget[0]
      thePage = labelTarget[2]

      redirectHtml = renderTemplate(
        template,
        {
          'url'      : f"/pdfjs/web/viewer.html?file=/pdfs/{theDoc}.pdf#page={thePage}",  # noqa
          'target'   : f"lpit_{theDoc}",
          'pageName' : f"{theDoc}-{labelKey}-{thePage}"
        },
        verbose=config['verbose']
      )

      redirectPath = config.webSiteCache / 'labels' / theDoc / labelKey / (str(thePage) + '.html')  # noqa
      redirectPath.parent.mkdir(parents=True, exist_ok=True)
      redirectPath.write_text(redirectHtml)

def renderLabelIndex(metaData, config) :
  labels = collectLabels(metaData, config)
  labelLevels = compileKeyLevels(
    sorted(labels.keys()), config['indexLevels']['labels']
  )

  createLabelRedirects(labels, config)

  labelsDescPath = config.cacheDir / 'labelsDesc.yaml'
  labelsDesc = {}
  if labelsDescPath.exists() :
    labelsDesc = yaml.safe_load(labelsDescPath.read_text())

  for aLabel in labelsDesc.keys() :
    labelsDesc[aLabel] = markdown(labelsDesc[aLabel])

  template = getTemplate('labelIndex.html')

  labelIndexHtml = renderTemplate(
    template,
    {
      'labelsDesc'  : labelsDesc,
      'labels'      : labels,
      'labelLevels' : labelLevels,
    },
    verbose=config['verbose']
  )
  labelIndexPath = config.webSiteCache / 'labelIndex.html'
  labelIndexPath.write_text(labelIndexHtml)

