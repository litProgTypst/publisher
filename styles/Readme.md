# Typst Publisher Styles

The Typst Publisher is used to "publish" a collection of Typst documents
to the web.

This "styles" directory provides a number of styles for publishing such
Typst documents using the Publisher.

At the moment we have two styles:

  - **papers** : each part of the published collection is a paper in a
    (collective) "Journal". 

  - **chapters** : each part of the published collection is a chapter in a
    (collective) "Book".

In fact each part of the collection can be chosen individually to be
either a "paper" or a "chapter". As far as the published collection is
concerned, all such parts will be indexed, cross-referenced, and provided
with a bibliography and table of contents *as a whole*.

All Typst documents published by the publisher **must** contain:

  - An abstract
  - A bibliography
  - Headings (at various levels)

These styles actively generate the information about each document which
is required by the Publisher to provide its global overviews.

Generally we follow the [Chicago Manual of
Style](https://www.chicagomanualofstyle.org) and the
[AMS](https://www.ams.org) guidelines for
[Journals](https://www.ams.org/arc/journals/index.html) and
[Books](https://www.ams.org/arc/books/index.html).

The journal style has been based upon the style packages below. However,
since we required such extensive changes, we have created our own styles
rather than simply adapting one of these existing pacakges.

## Notes

### Package structure

- [typst-community/typst-package-template](https://github.com/typst-community/typst-package-template)

- [typst/packages: Packages for
  Typst.](https://github.com/typst/packages/?tab=readme-ov-file#package-format)

### Managing large documents

- [Best practices for working with longer documents - General - Typst
  Forum](https://forum.typst.app/t/best-practices-for-working-with-longer-documents/1228/4)

### Example style packages

- [templates/unequivocal-ams at main ·
  typst/templates](https://github.com/typst/templates/tree/main/unequivocal-ams)

- [HPDell/typst-starter-journal-article](https://github.com/HPDell/typst-starter-journal-article)

- [gdahia/typst-ams-fullpage-template: Typst AMS template customized to
  look like TeX amsart with
  fullpage](https://github.com/gdahia/typst-ams-fullpage-template)

- [npikall/rubber-article: A simple template recreating the look of the
  classic LaTeX article.](https://github.com/npikall/rubber-article)

