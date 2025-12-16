# import yaml

from lpitPublisher.jinjaUtils import getTemplate, renderTemplate, \
  compileKeyLevels, createRedirects

def collectTheorems(metaData) :
  theorems = {}

  for aDocKey, aDocDef in metaData.items() :
    aDocMD = aDocDef['metaData'][0]['value']['figure']
    for aFigure in aDocMD :
      if aFigure['kind'] != 'thmenv' : continue
      theType = "unknown"
      if 'text' in aFigure['supplement'] :
        theType = aFigure['supplement']['text']
      if aFigure['label'] == 'none' :
        print(f"WARNING: no label found for the {theType} on page {aFigure['page']} in the {aDocKey} document")  # noqa
        continue

      # found a valid theorem environment record it
      theoremLabel = aFigure['label'].strip('<>')
      if theoremLabel not in theorems :
        theorems[theoremLabel] = []
      theorems[theoremLabel].append((
        aDocKey, theoremLabel, aFigure['page'], theType
      ))

  return theorems

def renderTheoremIndex(metaData, config) :
  theorems = collectTheorems(metaData)
  theoremLevels = compileKeyLevels(
    sorted(theorems.keys()), config['indexLevels']['theorems']
  )

  createRedirects(
    theorems,
    config.webSiteCache / 'theorems',
    config['verbose']
  )

  template = getTemplate('theoremIndex.html')

  theoremIndexHtml = renderTemplate(
    template,
    {
      'labelsDesc'    : config.labelsDesc,
      'theorems'      : theorems,
      'theoremLevels' : theoremLevels,
    },
    verbose=config['verbose']
  )
  theoremIndexPath = config.webSiteCache / 'theoremIndex.html'
  theoremIndexPath.write_text(theoremIndexHtml)

