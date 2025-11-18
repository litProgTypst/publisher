# LPiT document structure

All LPiT documents will have:

1. `lpit.yaml` file which contains:

   1. Document identifier
   2. Document type
   3. Short title
   4. Long title
   5. Authors (given, family, prefix, suffix)
   6. Abstract (in Markdown/KaTeX format; this *may* diverge from the
      abstract in the document)
   
2. A main typst file named using the document identifier with the `.typ`
   extension. This typst file **WILL** import one of the current LPiT
   typst style templates.

The `lpit.yaml` file **WILL** be loaded by the chosen LPiT style template
to supply those values to the style.

