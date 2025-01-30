# Phasing the Publisher's abilities

Since the [Typst HTML output
mode](https://github.com/typst/typst/issues/5512) is currently unstable,
incomplete and in very active development, we need to provide a initial
(incomplete) solution based on existing tools.

We will do this by serving the PDFs as they are and assume that the user's
browser works essentially like the PDF.js viewer (which is automatically
built into FireFox and Chrome). In this iteration we can (easily) "jump"
to individual pages in the PDF, so our tables of contents, etc will have
url's directly to a given page:

```
  https://<server>/<pdfPath>#page=<pageNumber>
```




