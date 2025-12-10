# Overall Design

The publisher has a number of phases:

1. Identification of all documents.
2. Collection of meta-data (Typst-Query) from each document.
3. Creation of the static website using the collected meta-data.

Since most documents will not have changed from one run of the publisher
to another, to help ensure we do only the work required, we keep a cache
of the meta-data, as well as a hash of each `*.typ` document and its last
modification time.

We can then check if a given document requires re-collection of the
meta-data before re-running the compute intensive typst-query, typst-html,
typst-pdf commands.

We can also use the accumulated cache of meta-data to generate the static
website.

## Configuration and cache

The **configuration** will be contained in a `~/.config/lpit`
directory. This configuration *should* be version controlled.

The **cache** will be contained in a `~/.cache/lpit`
directory. This cache need not be version controlled, as it can and
probably will be periodically recreated from the existing documents.

The cache will contain:

1. A YAML file containing all collected file names, hashes and last
   modification times.

2. A meta-data directory containing the typst-query meta-data for each
   *document* as a JSON file. (We use JSON as it is the output of the
   typst-query command).

3. An html directory containing a sub-directory of the html for each
   identified document.

4. A PDF directory containing the PDF for each identified document.

In order to keep all of this data separate, each identified document
**MUST** be given a **UNIQUE** identifier.

## Identification phase

The configuration **will** contain a list of directories which will be
checked for LPiT documents.

Each sub-directory of these listed directories which (recursively) contain
`*.typ` documents, will be considered LPiT documents to be *included* in
the publisher's cache and (eventual) output.

## Collection phase

For each identified LPiT document, which requires re-collection, the
publisher will run typst-query, typst-html and/or typst-pdf as required.

The output of the typst-query will be added to the meta-data cache.

The output of the typst-html will be added to an html directory dedicated
to the given document.

The output of the typst-pdf will be added to the collection of PDF documents.

## Generation phase

The cached meta-data, collected during repeated collection phases, will be
used to stitch together a coherent website combining all of the identified
LPiT documents in *one* (static) website.

The configuration **will** contain an ordered list of the document
identifiers, in order to provide an order to the website's contents. Any
document which is not listed in this order, will be appended in
*alphabetical* order by identifier.

