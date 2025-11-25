# The structure of the LPiT.yaml file

This YAML file is a dictionary containing the keys:

 - **doc** contains the subkeys:
   - **id** provides the unique document id.
   - **name** provides the name of the base document file.
   - **type** declares the *type* of document.

 - **title** contains the subkeys:
   - **short** is a short title to be displayed 
     is the top of each page
   - **long** is a longer title to be used
     on the title page

 - **gitHub** is the (external) https link to the gitHub repository
   associated with this document.

 - **authors** is a list of dictionaries one for each author.
   Each author's dictionary contains the keys:
   - **given** is the given name of the author
   - **family** is the family name of the author
   - **prefix** is one or more prefixes of the family name (eg: 'Von'). (optional)
   - **suffix** is one or more suffixes of the family name (eg: 'Jr'). (optional)
   - **order** indicates the order in which the name should be constructed. (optional)
   - **email** is the author's contact email address. (optional)

- **packages** is a list of dictionaries one for each `#import'ed` Typst
  package (explicitly) used in the document. This information is used by
  the `lpitStylesUpdater` to find and update the versions of each package
  used in the document.
  
  Each package's dictionary contains the keys:
  
  - **location** is the package's location. This key is optional; its
    default is `@local`.
  - **name** is the name of the pacakge
  - **version** is the (current) version of the package

- **abstract** is the document's (external) abstract as used by the LPiT
  publisher. This abstract will tend to use either MathJaX or KaTeX
  notation for Mathematics, instead of the Typst notaion. This means that
  this abstract and the one included in the document *may* differ.

## Local version

If a file `lpitYaml.jinja2` is found in the config directory (by default
`~/.config/lpitPublisher`) then it will be used as the Jinja2 template for
the new `lpit.yaml` file.

