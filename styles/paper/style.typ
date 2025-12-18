
#import "metadata.typ": gatherMetaData

#import "@preview/cetz:0.4.2" as cetz 
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge

#import "@preview/codly:1.3.0" : *
#import "@preview/codly-languages:0.1.10": *
#show: codly-init.with()
#codly(languages: codly-languages)

#import fletcher.shapes: *

#import "@preview/ctheorems:1.1.3": *
#show: thmrules

/////////////////////////////////////////////////////////////////////////
// set up the Theorem Environments that we use:
//
#let definition = thmbox("definition", "Definition")
#let lemma = thmbox("lemma", "Lemma")
#let corollary = thmbox("corollary", "Corollary")
#let example = thmbox("example", "Example").with(number: none)

// Our goal is to adapt one or more of the AMS like journal styles for our
// specific use. However, at the moment, we will settle for less...

// 1. Table of Contents complete with abstracts

// This requires (a) a delcaration of the document id, (b) an abstract
// function whose text can be captured by the query, (c) some "query" code
// to capture the headings and their associated page numbers as well as
// the abstract.

#let lpitDocument(
  docId,
  shortTitle: [],
  longTitle: []
) = {
  context {
    let theData = (:)

    theData.queries = gatherMetaData()

    theData.docId = docId
    theData.shortTitle = shortTitle
    theData.longTitle = longTitle
    // theData.abstract = query(<abstract>)
    theData.inputs   = sys.inputs
    theData.test = sys.inputs.at("proj-" + "fp")
    [ #metadata(theData) <lpitMetaData> ]
  }
  [ #longTitle #label("title") ]
}

#let abstract(body) = [
  #align(center, body) #label("abstract")
]

#let interCollectionRefAt(project, docId, label, page, text) = {
  if "proj-" + project in sys.inputs {
    if page == 0 {
      page = "index"
    }
    link(
      sys.inputs.at("proj-" + project) + "/labels/" + docId + "/" + str(label) + "/" + str(page) + ".html",
      text
    )
  }
}

#let interCollectionRef(project, docId, label, text) = {
  interCollectionRefAt(project, docId, label, 0, text)
}

#let interDocRefAt(docId, label, page, text) = {
  interCollectionRef(sys.inputs.project, docId, label, page, text)
}

#let interDocRef(docId, label, text) = {
  interCollectionRefAt(sys.inputs.project, docId, label, 0, text)
}

#let icRefAt = interCollectionRefAt
#let icRef   = interCollectionRef
#let idRefAt = interDocRefAt
#let idRef   = interDocRef

#let setupDoc(lpitDef, doc) = {
  // document set and show rules
  set cite(style: "alphanumeric")
  set heading(numbering: "1.")
  // function which adds content
  lpitDocument(lpitDef.doc.id,
    shortTitle: lpitDef.title.short,
    longTitle: lpitDef.title.long
  )
  doc
}


