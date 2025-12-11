# Bibliography in Typst

## CSL

Typst uses the [CSL
collection](https://github.com/citation-style-language/styles) of
bibliographic descriptions.

The main drawback of this is that a CSL file can NOT include any "dynamic
behaviours". In particular it is the responsibility of the CSL-Processor
to compute citation-labels. 

For Typst the CSL-Processor is part of the [`hayagriva`
project](https://github.com/typst/hayagriva).

At the moment this CSL-Project's label creation is rather limited. In
particular alphanumeric labels with more the three authors, uses the first
author and a `+`, which is not LaTeX's alpha BST's default. Alas this is
unlikely to change in the near future. There is however a [patch that can
be
applied](https://forum.typst.app/t/impossible-to-mimic-bibliographystyle-alpha-in-typst/4767/10).

Again, at the moment the simplistic `alphanumeric` seems good enough...

As an alternative, we could use the CSL's [`citation-key`
variable](https://docs.citationstyles.org/en/stable/specification.html#standard-variables)
by copying and modifying the `alphanumeric.csl` file in the `hayagriva`
project and changing:

```
  <citation after-collapse-delimiter="; " disambiguate-add-year-suffix="true">
    <sort>
      <key variable="author" />
      <key variable="issued" />
    </sort>
    <layout prefix="[" suffix="]" delimiter=", ">
      <group delimiter=", ">
        <group>
            <text variable="citation-label" />
            <text variable="year-suffix" />
        </group>
        <text variable="locator" />
      </group>
    </layout>
  </citation>

```

to 

```
  <citation after-collapse-delimiter="; " disambiguate-add-year-suffix="true">
    <sort>
      <key variable="author" />
      <key variable="issued" />
    </sort>
    <layout prefix="[" suffix="]" delimiter=", ">
      <group delimiter=", ">
        <group>
            <text variable="citation-key" />
        </group>
        <text variable="locator" />
      </group>
    </layout>
  </citation>

```

AND then providing our own bibliographic citation keys in the bibtex "key"
entry, using our existing `cmAddBib` or `cmBibRefresh` tools.


## Resources

- [Citation Style Language
  Documentation](https://docs.citationstyles.org/_/downloads/en/stable/pdf/)
  **HAS an excellent description of how the CSL works**

- [Named destinations by Heinenen · Pull Request #2954 ·
  typst/typst](https://github.com/typst/typst/pull/2954)

- [External reference to PDF #subsection · Issue #1352 ·
  typst/typst](https://github.com/typst/typst/issues/1352)

- [Juris-M/citeproc-js: A JavaScript implementation of the Citation Style
  Language (CSL)
  https://citeproc-js.readthedocs.io](https://github.com/Juris-M/citeproc-js)

- [citeproc-py · PyPI](https://pypi.org/project/citeproc-py/)

- [`alphanumeric` style: How to get disambiguation letters (e.g., [ASS96a]
  and [ASS96b]) in bibliography labels? - Questions - Typst
  Forum](https://forum.typst.app/t/alphanumeric-style-how-to-get-disambiguation-letters-e-g-ass96a-and-ass96b-in-bibliography-labels/3871)

- [Force `CitationLabel` in bibliography when using `alphanumeric`
  citation labels · Issue #2707 ·
  typst/typst](https://github.com/typst/typst/issues/2707)

- [Impossible to mimic `\bibliographystyle{alpha}` in Typst? - Questions -
  Typst
  Forum](https://forum.typst.app/t/impossible-to-mimic-bibliographystyle-alpha-in-typst/4767/10)

- [Authors - Citation Style
  Language](https://citationstyles.org/authors/#/csl-limitations)

