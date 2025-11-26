# Using PDFjs


We simply reuse the viewer.

We ***should*** change the livery/theme slightly, ***but*** we would like to use
most of the existing functionality.

--------------------------

## Viewer URL options

The following has been adapted from: [Viewer options · mozilla/pdf.js
Wiki](https://github.com/mozilla/pdf.js/wiki/Viewer-options)

Below are the options for the PDF.js viewer that can be given at URL
level. Multiple values of either type can be combined by separating with
an ampersand (`&`) after the hash (for example: `#page=2&zoom=200`).

### Options after the `#`

Example: `https://mozilla.github.io/pdf.js/web/viewer.html#page=2`

- **page**: page number. Example: `page=2`

- **zoom**: zoom level. Example: `zoom=200` (accepted formats: `[zoom],[left
  offset],[top offset]`, `page-width`, `page-height`, `page-fit`, `auto`)

- **nameddest**: go to a named destination

- **pagemode**: sidebar state. Example: `pagemode=none` (accepted values:
  `none`, `thumbs`, `bookmarks`, `attachments`)

### Options after the `?`

Example: `https://mozilla.github.io/pdf.js/web/viewer.html?file=compressed.tracemonkey-pldi-09.pdf`

- **file**: the path of the PDF file to use (must be on the same server
  due to JavaScript limitations). Please notice that the path/URL must be
  encoded using encodeURIComponent, e.g.
  `/viewer.html?file=%2Fpdf.js%2Fweb%2Fcompressed.tracemonkey-pldi-09.pdf`


## Additional resources

- [firefox - What does the mozdisallowselectionprint attribute in PDF.js
  do? - Stack
  Overflow](https://stackoverflow.com/questions/30097055/what-does-the-mozdisallowselectionprint-attribute-in-pdf-js-do)

- [init — Alpine.js](https://alpinejs.dev/directives/init) used to
  insert the document name in the viewer's toolbar (as part of our livery
  changes). See the second example for some javascript setting a data value.

- [text — Alpine.js](https://alpinejs.dev/directives/text) used to
  actually do the text insertion.

- [mozilla/pdf.js: PDF Reader in
  JavaScript](https://github.com/mozilla/pdf.js)

- [PDF.js - Home](https://mozilla.github.io/pdf.js/)

- [Window: location property - Web APIs |
  MDN](https://developer.mozilla.org/en-US/docs/Web/API/Window/location)

