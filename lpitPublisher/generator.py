
import argparse
import os
from pathlib import Path
import shutil
# import yaml

from lpitPublisher.config import addConfigurationArgs, Config
from lpitPublisher.metaData import loadMetaData, sortDocuments
from lpitPublisher.jinjaUtils import getTemplate, renderTemplate

from lpitPublisher.genLabels import renderLabelIndex
from lpitPublisher.genBibliography import renderBibliography
from lpitPublisher.genTheorems import renderTheoremIndex
from lpitPublisher.genFigures import renderFigureIndex

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

def renderWebsiteIndex(config) :
  template = getTemplate('websiteIndex.html')

  indexHtml = renderTemplate(
    template,
    {
      'websiteTitle' : config['webSiteName']
    },
    verbose=config['verbose']
  )

  indexPath = config.webSiteCache / 'index.html'
  indexPath.write_text(indexHtml)

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
  renderBibliography(metaData, config)
  renderTheoremIndex(metaData, config)
  renderFigureIndex(metaData, config)

  renderWebsiteIndex(config)

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

  os.system(
    "tailwindcss --cwd lpitPublisher --input css/main.css --output ~/.cache/lpit/webSite/css/main.css"  # noqa
  )

######################################################################
# Run the app if called as a main
if __name__ == "__main__":
  cli()
