
import yaml

from pybtex import format_from_string  # type: ignore

# from markdown import markdown

# from lpitPublisher.jinjaUtils import getTemplate, renderTemplate

def addBibEntry(aBibEntry, bibEntries) :
  aKey = aBibEntry[0].split('{')[1].strip(',')
  if aKey not in bibEntries :
    print("FOUND NEW KEY")
    theBibEntry = "\n".join(aBibEntry)
    bibEntries[aKey] = theBibEntry.strip()

def collectBibliographyHtml(config) :
  bibEntries = {}

  for aBibFile in config.bibCache.rglob('*.bib') :
    bibLines = aBibFile.read_text().splitlines()
    aBibEntry = []
    for aLine in bibLines :
      if aLine.startswith('%') : continue
      if not aLine : continue
      if aLine.startswith('@') :
        print(aLine)
        if aBibEntry :
          addBibEntry(aBibEntry, bibEntries)
        aBibEntry = [aLine]
      else :
        aBibEntry.append(aLine)
    if aBibEntry : addBibEntry(aBibEntry, bibEntries)

  for aBibKey in sorted(bibEntries.keys()) :
    bibStr.append(bibEntries[aBibKey])

  return format_from_string(
    "\n\n".join(bibStr),
    'plain',
    output_backend='html'
  )

def collectBibEntries(metaData, config) :
  # bibEntriesIndexLevel = config['bibEntriesIndexLevel']

  bibEntries = {}
  bibEntriesLevels = {}

  for aDocKey, aDocDef in metaData.items() :
    print("-------------------------------_")
    print(aDocKey)
    aDocCites = aDocDef['metaData'][0]['value']['cite']
    for aCite in aDocCites :
      print(yaml.dump(aCite))

  return (bibEntries, bibEntriesLevels)

def createLabelRedirects(bibEntries, config) :
  pass

def renderBibliography(metaData, config) :
  bibHtml = collectBibliographyHtml(config)
  print("-----------------------------------")
  print(bibHtml)
  print("-----------------------------------")
  bibEntries, bibEntriesLevels = collectBibEntries(
    metaData, config
  )
