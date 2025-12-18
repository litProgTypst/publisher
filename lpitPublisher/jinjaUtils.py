
import sys
import yaml

from jinja2 import Environment, PackageLoader, select_autoescape

from lpitPublisher.config import Config

######################################################################
# Setup templates

jinjaEnv = Environment(
  loader=PackageLoader('lpitPublisher', 'templates'),
  autoescape=select_autoescape(
    enabled_extensions=('html', 'xml')
  )
)

def getTemplate(aTemplateName) :
  try :
    return jinjaEnv.get_template(aTemplateName)
  except Exception as err :
    print(f"Could not get template: {aTemplateName}")
    print(repr(err))
    sys.exit(1)

pages = {
  'list' : ['toc', 'labels', 'theorems', 'figures', 'bibliography'],
  'desc': {
    'toc' : {
      'url'   : '/toc.html',
      'short' : 'Contents',
      'long'  : 'Table of cotents'
    },
    'labels' : {
      'url'   : '/labelIndex.html',
      'short' : 'Labels',
      'long'  : 'Index of labels'
    },
    'theorems' : {
      'url'   : '/theoremIndex.html',
      'short' : 'Theorems',
      'long'  : 'Index of theorems'
    },
    'figures' : {
      'url'   : '/figureIndex.html',
      'short' : 'Figures',
      'long'  : 'Index of figures'
    },
    'bibliography' : {
      'url'   : '/bibliography.html',
      'short' : 'Bibliography',
      'long'  : 'Bibliography'
    }
  }
}

def renderTemplate(aTemplate, varDict, verbose=False) :
  varDict['webSiteName'] = Config()['webSiteName']
  varDict['pages'] = pages
  if verbose :
    print("----------------------------------------------")
    print(aTemplate.name)
    print(yaml.dump(varDict))

  try :
    return aTemplate.render(**varDict)
  except Exception as err :
    print(f"Could not render template: {aTemplate.name}")
    print(repr(err))
    sys.exit(1)

def compileKeyLevels(someKeys, keyIndexLevel) :
  keyLevels = {}

  for aKey in someKeys :
    # add a key to the key levels
    curLevel = keyLevels
    for aLevel in range(keyIndexLevel) :
      curTag = aKey[:aLevel + 1]
      if curTag not in curLevel : curLevel[curTag] = {}
      curLevel = curLevel[curTag]
    if aKey not in curLevel : curLevel[aKey] = {}

  return keyLevels

def createRedirects(theTargetDict, basePath, verbose) :
  template = getTemplate('redirect.html')

  for aKey, aDef in theTargetDict.items() :
    for aTarget in aDef :
      theDoc = aTarget[0]
      thePage = aTarget[2]

      redirectHtml = renderTemplate(
        template,
        {
          'url'      : f"/pdfjs/web/viewer.html?file=/pdfs/{theDoc}.pdf#page={thePage}",  # noqa
          'target'   : f"lpit_{theDoc}",
          'pageName' : f"{theDoc}-{aKey}-{thePage}"
        },
        verbose=verbose
      )

      redirectPath = basePath / theDoc / aKey / (str(thePage) + '.html')  # noqa
      redirectPath.parent.mkdir(parents=True, exist_ok=True)
      redirectPath.write_text(redirectHtml)
