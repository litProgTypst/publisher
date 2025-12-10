

#import "@preview/cetz:0.4.2" as cetz 
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge
#import "@preview/codly:1.3.0" : *
#import "@preview/codly-languages:0.1.10": *

#show: codly-init.with()
#codly(languages: codly-languages)

#import fletcher.shapes: *

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

    let headingData = ()
    for aHeading in query(heading) {
      let loc = aHeading.location()
      let aPageNum = loc.page()
      headingData.push(("theHeading": aHeading, "thePage": aPageNum))

    theData.headings = headingData

    theData.docId = docId
    theData.shortTitle = shortTitle
    theData.longTitle = longTitle
    theData.abstract = query(<abstract>)
    theData.inputs   = sys.inputs
    }
    [ #metadata(theData) <lpitMetaData> ]
  }
  [ #longTitle #label("title") ]
}

#let abstract(body) = [
  #align(center, body) #label("abstract")
]

#let setupDoc(lpitDef) = {
  lpitDocument(lpitDef.doc.id,
    shortTitle: lpitDef.title.short,
    longTitle: lpitDef.title.long
  )
  // [ #yaml.encode(lpitDef) ]
}

// see: https://forum.typst.app/t/alphanumeric-style-how-to-get-disambiguation-letters-e-g-ass96a-and-ass96b-in-bibliography-labels/3871
#show bibliography: set cite(style: "alphanumeric")

