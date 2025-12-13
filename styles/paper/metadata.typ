#let getPageNum(aQuery) = {
  return aQuery.location().page()
}

#let abstractData(aQuery) = {
  return (
    "type": "abstract",
    "label": aQuery.at("label", default: "none"),
    "page": getPageNum(aQuery),
  )
}

// we use all of the heading data
#let headingData(aQuery) = {
  return (
    "type": "heading",
    "label": aQuery.at("label", default: "none"),
    "level": aQuery.level,
    "depth": aQuery.depth,
    "body": aQuery.body,
    "supplement": aQuery.supplement,
    "page": getPageNum(aQuery),
    // "heading": aQuery,
   )
}

// we only care about the target
#let refData(aQuery) = {
  return (
    "type": "ref",
    "target": aQuery.target,
    "label": aQuery.at("label", default: "none"),
    "page": getPageNum(aQuery),
    // "data": aQuery,
  )
}

// we use all of the cite data
#let citeData(aQuery) = {
  return (
    "type": "cite",
    "label": aQuery.at("label", default: "none"),
    "page": getPageNum(aQuery),
    "cite": aQuery,
  )
}

// 
#let figureData(aQuery) = {
  return (
    "type": "figure",
    "kind": aQuery.kind,
    "supplement": aQuery.supplement,
    "label": aQuery.at("label", default: "none"),
    "page": getPageNum(aQuery),
    //"data": aQuery,
  )
}

//#let tableData(aQuery) = {
//  return (
//    "type": "table",
//    "label": aQuery.at("label", default: "none"),
//    "page": getPageNum(aQuery),
//    "data": aQuery,
//  )
//}

#let linkData(aQuery) = {
  return (
    "type": "link",
    "label": aQuery.at("label", default: "none"),
    "page": getPageNum(aQuery),
    //"data": aQuery,
  )
}

#let equationData(aQuery) = {
  return (
    "type": "equation",
    "label": aQuery.at("label", default: "none"),
    "page": getPageNum(aQuery),
    //"data": aQuery,
  )
}

#let footnoteData(aQuery) = {
  return (
    "type": "footnote",
    "label": aQuery.at("label", default: "none"),
    "page": getPageNum(aQuery),
    //"data": aQuery,
  )
}

#let bibliographyData(aQuery) = {
  return (
    "type": "bibliography",
    "label": aQuery.at("label", default: "none"),
    "page": getPageNum(aQuery),
    //"data": aQuery,
  )
}

#let outlineData(aQuery) = {
  return (
    "type": "outline",
    "label": aQuery.at("label", default: "none"),
    "page": getPageNum(aQuery),
    //"data": aQuery,
  )
}

#let gatherMetaData() = {
  let queryData = ()

  for aQuery in query(<abstract>) {
    queryData.push(abstractData(aQuery))
  }

  for aQuery in query(heading) {
    queryData.push(headingData(aQuery))
  }

  for aQuery in query(ref) {
    queryData.push(refData(aQuery))
  }

  for aQuery in query(cite) {
    queryData.push(citeData(aQuery))
  }

  for aQuery in query(figure) {
    queryData.push(figureData(aQuery))
  }

//  for aQuery in query(table) {
//    queryData.push(tableData(aQuery))
//  }

  for aQuery in query(link) {
    queryData.push(linkData(aQuery))
  }

  for aQuery in query(math.equation) {
    queryData.push(equationData(aQuery))
  }

  for aQuery in query(footnote) {
    queryData.push(footnoteData(aQuery))
  }

  for aQuery in query(bibliography) {
    queryData.push(bibliographyData(aQuery))
  }

  for aQuery in query(outline) {
    queryData.push(outlineData(aQuery))
  }

  return queryData
}
