

#import "@preview/cetz:0.4.2" as cetz 
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge

#import "@preview/codly:1.3.0" : *
#import "@preview/codly-languages:0.1.10": *
#show: codly-init.with()
#codly(languages: codly-languages)

#import fletcher.shapes: *

#import "@preview/theoretic:0.2.0" as theoretic: theorem, proof, qed
#show ref: theoretic.show-ref
// set up your needed presets
#let corollary = theorem.with(kind: "corollary", supplement: "Corollary")
#let example = theorem.with(kind: "example", supplement: "Example", number: none)

// Our goal is to adapt one or more of the AMS like journal styles for our
// specific use. However, at the moment, we will settle for less...

// 1. Table of Contents complete with abstracts

// This requires (a) a delcaration of the document id, (b) an abstract
// function whose text can be captured by the query, (c) some "query" code
// to capture the headings and their associated page numbers as well as
// the abstract.

// see: https://github.com/typst/typst/issues/2196#issuecomment-1728135476
#let lpit-to-string(content) = {
  if content.has("text") {
    content.text
  } else if content.has("children") {
    content.children.map(to-string).join("")
  } else if content.has("body") {
    to-string(content.body)
  } else if content == [ ] {
    " "
  }
}

#let lpitDocument(
  docId,
  shortTitle: [],
  longTitle: []
) = {
  context {
    let theData = (:)

    let queryData = ()
    for aQuery in query(heading) {
      let loc = aQuery.location()
      let aPageNum = loc.page()
      queryData.push(("data": aQuery, "page": aPageNum))
    }

    for aQuery in query(ref) {
      let loc = aQuery.location()
      let aPageNum = loc.page()
      queryData.push(("data": aQuery, "page": aPageNum))
    }

    for aQuery in query(cite) {
      let loc = aQuery.location()
      let aPageNum = loc.page()
      queryData.push(("data": aQuery, "page": aPageNum))
    }

    for aQuery in query(figure) {
      let loc = aQuery.location()
      let aPageNum = loc.page()
      queryData.push(("data": aQuery, "page": aPageNum))
    }

    for aQuery in query(table) {
      let loc = aQuery.location()
      let aPageNum = loc.page()
      queryData.push(("data": aQuery, "page": aPageNum))
    }

    for aQuery in query(link) {
      let loc = aQuery.location()
      let aPageNum = loc.page()
      queryData.push(("data": aQuery, "page": aPageNum))
    }

    for aQuery in query(footnote) {
      let loc = aQuery.location()
      let aPageNum = loc.page()
      queryData.push(("data": aQuery, "page": aPageNum))
    }

    for aQuery in query(bibliography) {
      let loc = aQuery.location()
      let aPageNum = loc.page()
      queryData.push(("data": aQuery, "page": aPageNum))
    }

    for aQuery in query(outline) {
      let loc = aQuery.location()
      let aPageNum = loc.page()
      queryData.push(("data": aQuery, "page": aPageNum))
    }

    theData.queries = queryData

    theData.docId = docId
    theData.shortTitle = shortTitle
    theData.longTitle = longTitle
    theData.abstract = query(<abstract>)
    theData.inputs   = sys.inputs
    [ #metadata(theData) <lpitMetaData> ]
  }
  [ #longTitle #label("title") ]
}

#let abstract(body) = [
  #align(center, body) #label("abstract")
]

#let setupDoc(lpitDef, doc) = {
  // document set and show rules
  set cite(style: "alphanumeric")

  // function which adds content
  lpitDocument(lpitDef.doc.id,
    shortTitle: lpitDef.title.short,
    longTitle: lpitDef.title.long
  )
  doc
}


