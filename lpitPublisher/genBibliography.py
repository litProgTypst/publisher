
import re
# import yaml

from pybtex import format_from_string  # type: ignore

# from markdown import markdown

from lpitPublisher.jinjaUtils import getTemplate, renderTemplate, \
  compileKeyLevels, createRedirects

def addBibEntry(aBibEntry, bibEntries) :
  aKey = aBibEntry[0].split('{')[1].strip(',')
  if aKey not in bibEntries :
    theBibEntry = "\n".join(aBibEntry)
    bibEntries[aKey] = theBibEntry.strip()

def getBibEntryHtml(someHtml) :
  foundEntry = False
  entry = []
  for aLine in someHtml.splitlines() :
    if aLine.startswith('<dd>') :
      foundEntry = True
      entry.append(aLine.removeprefix('<dd>'))
      continue
    if aLine.endswith('</dd>') :
      foundEntry = False
      entry.append(aLine.removesuffix('</dd>'))
      continue
    if not foundEntry : continue
    entry.append(aLine)

  return "\n".join(entry)

removeBibCommentRegExp = re.compile(r'%.*$')

def collectBibliographyHtml(config) :
  bibEntries = {}

  for aBibFile in config.bibCache.rglob('*.bib') :
    bibLines = aBibFile.read_text().splitlines()
    aBibEntry = []
    for aLine in bibLines :
      aLine = removeBibCommentRegExp.sub('', aLine)
      if not aLine.strip() : continue
      if aLine.startswith('@') :
        if aBibEntry :
          addBibEntry(aBibEntry, bibEntries)
        aBibEntry = [aLine]
      else :
        aBibEntry.append(aLine)
    if aBibEntry : addBibEntry(aBibEntry, bibEntries)

  bibHtml = {}
  for aBibKey in sorted(bibEntries.keys()) :
    bibHtml[aBibKey] = getBibEntryHtml(
      format_from_string(
        bibEntries[aBibKey],
        'plain',
        output_backend='html'
      )
    )

  return bibHtml

def collectBibEntryTargets(metaData) :

  bibEntryTargets = {}

  for aDocKey, aDocDef in metaData.items() :
    aDocCites = aDocDef['metaData'][0]['value']['cite']
    for aCite in aDocCites :
      aKey = aCite['cite']['key'].strip('<>')
      aPage = aCite['page']
      if aKey not in bibEntryTargets :
        bibEntryTargets[aKey] = []
      bibEntryTargets[aKey].append((aDocKey, aKey, aPage))

  return bibEntryTargets

def renderBibliography(metaData, config) :
  bibHtml = collectBibliographyHtml(config)
  bibEntryTargets = collectBibEntryTargets(metaData)
  bibEntryLevels = compileKeyLevels(
    sorted(bibHtml.keys()), config['indexLevels']['bibliography']
  )

  createRedirects(
    bibEntryTargets,
    config.webSiteCache / 'citations',
    config['verbose']
  )

  template = getTemplate('bibliography.html')

  bibliographyHtml = renderTemplate(
    template,
    {
      'bibHtml'         : bibHtml,
      'bibEntryTragets' : bibEntryTargets,
      'bibEntryLevels'  : bibEntryLevels,
    },
    verbose=config['verbose']
  )
  bibliographyPath = config.webSiteCache / 'bibliography.html'
  bibliographyPath.write_text(bibliographyHtml)

