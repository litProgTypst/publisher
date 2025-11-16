
import os
from pathlib import Path
import sys
import yaml

def die(msg) :
  print(msg)
  sys.exit(1)

def addConfigurationArgs(parser) :
  parser.add_argument(
    '-c', '--config',
    help="The path to the user configuration file",
    default=os.path.expanduser('~/.config/lpitPublisher/config.yaml')
  )
  parser.add_argument(
    '-v', '--verbose',
    help="Be verbose",
    default=False,
    action='store_true'
  )

class Config(object) :
  def __new__(cls) :
    if not hasattr(cls, 'instance') :
      cls.instance = super(Config, cls).__new__(cls)
    return cls.instance

  def __getitem__(self, key) :
    return self.config[key]

  def __contains__(self, key) :
    return key in self.config

  def __setitem__(self, key, value) :
    self.config[key] = value

  def print(self) :
    print("-------------------------------------------------")
    print(yaml.dump(self.config))
    print("-------------------------------------------------")

  def checkDirs(self) :
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

    cachePath = Path('~/.var/cache/lpitPublisher')
    if 'cacheDir' in self.config :
      cachePath = Path(self.config['cacheDir'])
    cachePath = cachePath.expanduser()
    if not cachePath.exists() :
      cachePath.mkdir(parents=True, exist_ok=True)
    self.config['cacheDir'] = str(cachePath)
    self.htmlCache     = cachePath / 'html'
    if not self.htmlCache.exists() :
      self.htmlCache.mkdir(parents=True, exist_ok=True)
    self.metaDataCache = cachePath / 'metaData'
    if not self.metaDataCache.exists() :
      self.metaDataCache.mkdir(parents=True, exist_ok=True)

  def loadConfig(self, args, verbose=False) :
    configPath = Path(args['config']).expanduser()

    if not configPath.parent.exists() :
      configPath.parent.mkdir(parents=True, exist_ok=True)

    self.config = yaml.safe_load(configPath.read_text())
    if not self.config :
      self.config = {}

    for aKey, aValue in args.items() :
      if aValue : self.config[aKey] = aValue

    if 'verbose' not in self.config :
      self.config['verbose'] = verbose

    self.checkDirs()

    if self.config['verbose'] : self.print()

