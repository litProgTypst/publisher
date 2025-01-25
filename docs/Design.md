# Design

This Publisher was originally inspired by the [Gerby
project](https://gerby-project.github.io/).

The key task of the publisher is to maintain a global glossary,
cross-reference, index and table of contents across a number of loosely
related documents written in [Typst](https://typst.app/).

We use:

1. `typst query` ([see](https://typst.app/docs/reference/introspection/))
   will extract cross-references from each individual document.

2. Cross references will consist of document-id, internal-reference-id,
   and version-number. The version-number will be the git tag and/or git
   version short code. Only git tags will be permanent on the website, git
   version short codes will be merely drafts.

   - these document-id/internal-reference-id/version-number combinations
     will provide *permanent* *external* links into the published documents.

3. Each document-id/internal-reference-id combination will have a short
   glossary description, and will have back links to all locations in the
   various documents. These descriptions and back-links will act as a
   global Glossary and Index.

4. `typst query` will extract document structure which will be used to
   maintain a global Table of Contents.

5. `typst` in HTML mode ([currently under active
   development](https://github.com/typst/typst/issues/5512) ([issue
   721](https://github.com/typst/typst/issues/721)) will be used to
   publish HTML versions of each document to be placed on the website
   (together with the pdf for download).

6. [Comentario](https://comentario.app/en/) will be used to provide
   moderated comments associated with each cross-reference and/or document
   section. We will consider using one or more of the associated
   extensions to help screen/moderate the comments.

   - we will try to use [OrcID OAuth sign
     in](https://info.orcid.org/documentation/integration-guide/orcid-oauth-sign-in-guidelines/)
     to provide authentication for commentors.

7. Cross references, glossary and table of contents will be extracted and
   built using a python script (which might include an internal website to
   maintain the glossary descriptions). The resulting glossary and table
   of contents will be auto-generated to provide a static website.

8. Non-Typst document pages will be maintained using the (python based)
   [Nikola](https://getnikola.com/) static website generator.

9. We may need to write a python script which modifies the HTML output of
   Typst to suit our needs. For example we may need to inject HTML code to
   be able to place the comments in the correct location in the documents.


## Resources

See:

- [Justin Pombrio - Typst as a
  Language](https://justinpombrio.net/2024/11/30/typst.html)

- [Typst Basics - Typst Examples
  Book](https://sitandr.github.io/typst-examples-book/book/basics/)

- [Myriad-Dreamin/tinymist: Tinymist [ˈtaɪni mɪst] is an integrated
  language service for Typst
  [taɪpst].](https://github.com/Myriad-Dreamin/tinymist)

