# Literate Programming in Typst Publisher Papers Style

This [Typst Package](https://github.com/typst/packages) provides the [(AMS
like) paper style](https://www.ams.org/arc/journals/index.html) for the
Literate Programming in Typst Publisher.

Generally we follow the [Chicago Manual of
Style](https://www.chicagomanualofstyle.org) and the
[AMS](https://www.ams.org) guidelines for
[Journals](https://www.ams.org/arc/journals/index.html).

To install locally, in the root of the Publisher project, type:

```
  ./scripts/installStyles
```

or

```
  ./scripts/installEditableStyles
```

To *use* you need to place the following line at the top of any of your
Typst (sub)documents:

```
  #import @local/lpit-publisher-paper:0.1.0" : *
```

