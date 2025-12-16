
import sys
import yaml

from jinja2 import Environment, PackageLoader, select_autoescape

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

def renderTemplate(aTemplate, varDict, verbose=False) :
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

