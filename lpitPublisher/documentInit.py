
import argparse
from pathlib import Path
import traceback
import yaml

from jinja2 import Template

from lpitConfig.config import localLpitYamlPath, loadLpitYaml
from lpitPublisher.config import Config, addConfigurationArgs
from lpitPublisher.utils import stylesDir, loadStyleInfo, getStyleDir

def createLpitYamlFile(lpitYamlPath, config) :

  lpitYamlTemplate = Path(
    config['config']
  ).expanduser().parent / 'lpitYaml.jinja2'
  if not lpitYamlTemplate.exists() :
    lpitYamlTemplate = stylesDir / 'lpitYaml.jinja2'

  try :
    print("Creating a new LPiT.yaml file")
    templateStr = lpitYamlTemplate.read_text()
    template    = Template(templateStr)
    lpitYamlStr = template.render()
    localLpitYamlPath.write_text(lpitYamlStr)
    print("""

      Now PLEASE update the values in this new `lpit.yaml` file to
      represent your new document.

    """)
  except Exception as err :
    print("Could not create the document's lpit.yaml file")
    print(repr(err))

def createInitialDocument(lpitDef, config, importsOnly=False) :
  templatePath = getStyleDir(lpitDef) / 'typstTemplates'
  docPath      = lpitDef['doc']['name'] + '.typ'
  if 'docPath' in config :
    docPath = config['docPath']

    if not str(docPath).endswith('.typ') :
      docPath = docPath + '.typ'
      importsOnly = True

  docPath = Path(docPath).expanduser()
  docPath.parent.mkdir(parents=True, exist_ok=True)
  if docPath.exists() : return

  documentParts = ['imports', 'frontMatter', 'body', 'endMatter']
  if importsOnly : documentParts = [ 'imports' ]

  styleInfo = loadStyleInfo(lpitDef)

  try :
    print(f"Creating a new typst document file:\n  {docPath}")
    templateParts = []
    for aPart in documentParts :
      aTemplatePart = templatePath / (aPart + '.jinja2')
      templateParts.append(aTemplatePart.read_text())
    templateStr = '\n'.join(templateParts)
    template    = Template(templateStr)
    docStr      = template.render(
      version=styleInfo['version'],
      docId=lpitDef['doc']['id'],
      shortTitle=lpitDef['title']['short'],
      longTitle=lpitDef['title']['long'],
      abstract=lpitDef['abstract']
    )
    docPath.write_text(docStr)
  except Exception as err :
    print("Could not create the initial LPiT base document")
    print("----------------------------------")
    print(yaml.dump(styleInfo))
    print("----------------------------------")
    traceback.print_exception(err)

######################################################################
# Provide the command line interface

def parseArgs() :
  parser = argparse.ArgumentParser(
    prog='lpitDocumentInit',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""
Initialize a LPiT document directory
    """,
    epilog="""
If no `lpit.yaml` file is found an empty file is created.\n

With no arguments, a new document named using the doc:name specified
in the `lpit.yaml` file will be created (unless this file already
exists).\n

If `docPath` is provided, then a new document of that
name/path will be created (unless this file already exists).
    """
  )

  parser.add_argument(
    "docPath",
    nargs='?',
    help="a (relative) path to a new document (part) to initialize"
  )

  addConfigurationArgs(parser)

  return vars(parser.parse_args())

def cli() :
  config = Config()
  args = parseArgs()
  config.loadConfig(args)

  lpitDef = loadLpitYaml()
  if not lpitDef :
    createLpitYamlFile(localLpitYamlPath, config)
    return

  createInitialDocument(lpitDef, config)

