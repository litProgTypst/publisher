
# import yaml

from lpitPublisher.jinjaUtils import getTemplate, renderTemplate, \
  compileKeyLevels, createRedirects

def collectFigures(metaData) :
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

def renderFigureIndex(metaData, config) :
  figures = collectFigures(metaData)
  figureLevels = compileKeyLevels(
    sorted(figures.keys()), config['indexLevels']['figures']
  )

  createRedirects(
    figures,
    config.webSiteCache / 'figures',
    config['verbose']
  )

  template = getTemplate('figureIndex.html')

  figureIndexHtml = renderTemplate(
    template,
    {
      'labelsDesc'   : {},
      'figures'      : figures,
      'figureLevels' : figureLevels,
    },
    verbose=config['verbose']
  )
  theoremIndexPath = config.webSiteCache / 'figureIndex.html'
  theoremIndexPath.write_text(figureIndexHtml)

