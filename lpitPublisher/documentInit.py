from pathlib import Path
import sys
import traceback
import yaml

from jinja2 import Template

from lpitPublisher.utils import loadLpitYaml, loadStyleInfo, getStyleDir

def usage() :
  print("""
    lpitDocumentInit [-h, --help] [<aNewDocumentPath>]

    where:
      -h, --help          prints this text

      <aNewDocumentPath>  is a (relative) path to a new document
                          to be created.

      If no `lpit.yaml` file is found an empty file is created.

      With no arguments, a new document named using the doc:id specified
      in the `lpit.yaml` file will be created (unless this file already
      exists).

      If <aNewDocumentPath> is provided, then a new document of that
      name/path will be created (unles this file already exists).
  """)
  sys.exit(0)

def createInitialDocument(lpitDef, importsOnly=False) :
  templatePath = getStyleDir(lpitDef) / 'typstTemplates'
  docPath      = Path(lpitDef['doc']['id'] + '.typ')
  if 1 < len(sys.argv) :
    # print(yaml.dump(sys.argv))
    docPath = sys.argv[1]
    if str(docPath).endswith('-h') or str(docPath).endswith('--help') :
      usage()
      
    if not str(docPath).endswith('.typ') :
      docPath = docPath + '.typ'
    docPath = Path(docPath).expanduser()
    docPath.parent.mkdir(parents=True, exist_ok=True)
    importsOnly = True
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

def cli() :
  lpitDef = loadLpitYaml()

  createInitialDocument(lpitDef)
