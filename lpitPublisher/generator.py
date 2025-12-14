
import argparse
import os
from pathlib import Path
import shutil
import sys
import yaml

from jinja2 import Environment, PackageLoader, select_autoescape
from markdown import markdown

from lpitPublisher.config import addConfigurationArgs, Config
from lpitPublisher.metaData import loadMetaData, sortDocuments, collectLabels

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

######################################################################

def renderTableOfContents(documentOrder, metaData, config) :
  template = getTemplate('tableOfContents.html')

  tocHtml = renderTemplate(
    template,
    {
      'documentOrder' : documentOrder,
      'metaData'      : metaData
    },
    verbose=config['verbose']
  )

  tocPath = config.webSiteCache / 'toc.html'
  tocPath.write_text(tocHtml)

def renderLabelIndex(metaData, config) :
  labels, labelLevels = collectLabels(metaData, config)

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

# def renderPdfs(metaData, config) :
  # template = getTemplate('pdf.html')
  # for

######################################################################
# Provide the command line interface

def parseArgs() :
  parser = argparse.ArgumentParser(
    prog='lpitGenerator',
    description="""
      Use the collected meta-data to generate a static website for the
      collection of LPiT documents
    """,
    # epilog="""something..."""
  )

  addConfigurationArgs(parser)

  parser.add_argument(
    '-r', '--removewebsite',
    help="Remove the cached website",
    default=False,
    action='store_true'
  )

  return vars(parser.parse_args())

def cli() :
  os.system("reset")

  config = Config()
  args = parseArgs()
  config.loadConfig(args)
  config.checkDocumentDirs()

  metaData = loadMetaData(config)
  # print(yaml.dump(metaData))

  documentOrder = sortDocuments(metaData)

  if 'removewebsite' in config and config['removewebsite'] :
    os.system(f"rm -rf {config.webSiteCache}")
  config.webSiteCache.mkdir(parents=True, exist_ok=True)

  renderTableOfContents(documentOrder, metaData, config)

  renderLabelIndex(metaData, config)

  if 'faviconDir' in config :
    faviconDir = Path(config['faviconDir']).expanduser()
    shutil.copytree(
      faviconDir, config.webSiteCache, dirs_exist_ok=True
    )

  shutil.copytree(
    config.pdfCache, config.webSiteCache / 'pdfs', dirs_exist_ok=True
  )

  pdfjsDir = Path(__file__).parent.parent / 'tmp' / 'pdfjs'
  if pdfjsDir.exists() :
    shutil.copytree(
      pdfjsDir, config.webSiteCache / 'pdfjs', dirs_exist_ok=True
    )

######################################################################
# Run the app if called as a main
if __name__ == "__main__":
  cli()
