
from pathlib import Path

from lpitConfig.config import die, LpitConfig
import lpitConfig.config as lConfig

indices = [ 'labels', 'bibliography', 'theorems', 'figures' ]

def addConfigurationArgs(parser) :
  lConfig.addConfigurationArgs(parser)

  parser.add_argument(
    'project',
    help="Specify a project key to load the correct configuration",
  )

class Config(LpitConfig) :

  def checkDocumentDirs(self) :
    if 'documentDirs' not in self.config :
      die("No document directories specified... nothing to do!")
    docDirs = self.config['documentDirs']

    if len(docDirs) < 1 :
      die("No document directories specified... nothing to do!")

    for aDir in docDirs :
      # here be dragons!
      aDirPath = Path(aDir).expanduser()
      if not aDirPath.exists() :
        aDirPath.mkdir(parents=True, exist_ok=True)

  def addIndexLevels(self) :
    if 'indexLevels' not in self.config :
      self.config['indexLevels'] = {}
    indexLevels = self.config['indexLevels']
    for anIndex in indices :
      if anIndex not in indexLevels :
        indexLevels[anIndex] = 1

  def loadConfig(self, args, verbose=False) :
    self.initConfigFromArgs(args)
    self.mergeConfigFrom('config.yaml')
    self.mergeConfigFrom('publisher.yaml')

    if args['project'] :
      if args['project'] in self.config['projects'] :
        self.mergeConfigFrom(self.config['projects'][args['project']])

    if 'monitor' not in self.config :
      self.config['monitor'] = ['*.typ', '*.bib' ]

    if 'formats' not in self.config :
      self.config['formats'] = [ 'metadata', 'html', 'svg', 'pdf' ]

    if 'webSiteName' not in self.config :
      self.config['webSiteName'] = 'LPiT Documents'

    self.addIndexLevels()

    self.finishedLoading(args, verbose=verbose)

