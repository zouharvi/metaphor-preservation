// This function gets your whole document as its `body` and formats
// it as an article in the style of the IEEE.
#let project(
  // The paper's title.
  title: "Paper Title",

  // An array of authors. For each author you can specify a name,
  // department, organization, location, and email. Everything but
  // but the name is optional.
  authors: (),

  // The paper's abstract. Can be omitted if you don't have one.
  abstract: none,

  date: none,

  // A list of index terms to display after the abstract.
  index-terms: (),

  // The article's paper size. Also affects the margins.
  paper-size: "a4",

  // The path to a bibliography file if you want to cite some external
  // works.
  bibliography-file: none,

  // The paper's content.
  body
) = {
  // Set document metdata.
  //set document(title: title, author: authors.map(author => author.name))

  // Set the body font.
  set text(font: "STIX Two Text", size: 10pt)

  // Configure the page.
  set page(
    paper: paper-size,
    // The margins depend on the paper size.
    margin: 
      //(x: 41.5pt, top: 80.51pt, bottom: 89.51pt),
      (x: 70pt, top: 85pt, bottom: 90pt),
    numbering: "1 / 1",
  )

  // Configure equation numbering and spacing.
  set math.equation(numbering: "(1)")
  show math.equation: set block(spacing: 0.65em)

  // Configure lists.
  set enum(indent: 10pt, body-indent: 9pt)
  set list(indent: 10pt, body-indent: 9pt)

  // Configure headings.
  set heading(numbering: "1.1.1.")
  // CHANGE replace the whole thing with stock headings
  show heading: it => locate(loc => {
    // Find out the final number of the heading counter.
    let levels = counter(heading).at(loc)
    let deepest = if levels != () {
      levels.last()
    } else {
      1
    }

    set text(10pt, weight: 600)
    if it.level == 1 [
      // First-level headings are centered smallcaps.
      // We don't want to number of the acknowledgment section.
      #let is-ack = it.body in ([Acknowledgment], [Acknowledgement])
      //#set align(center)
      #set text(if is-ack { 10pt } else { 12pt })
      
      #set par(first-line-indent: 0pt)
      #v(30pt, weak: true)
      #if it.numbering != none and not is-ack {
        counter(heading).display()
        //numbering("1.", deepest)
        h(7pt, weak: true)
      }
      #it.body
      #v(13.75pt, weak: true)
    ] else if it.level == 2 [
      // Second-level headings are run-ins.
      #set par(first-line-indent: 0pt)
      #v(10pt, weak: true)
      #if it.numbering != none {
        counter(heading).display()
        ///it.numbering
        //numbering("1.1.", deepest)
        h(7pt, weak: true)
      }
      #it.body
      #v(10pt, weak: true)
    ] else [
      
      // Third level headings are run-ins too, but different.
      /*#if it.level == 3 {
        //counter(heading).display()
        //numbering("1)", deepest)
        [ ]
      }*/
      //_#(it.body):_
      #v(2mm)
      #(it.body):
    ]
  })
  

  // Display the paper's title.
  v(3pt, weak: true)
  // original 18pt
  align(center, text(16.6pt, title))
  v(8.35mm, weak: true)
  
  // Display the authors list.
  for i in range(calc.ceil(authors.len() / 3)) {
    let end = calc.min((i + 1) * 3, authors.len())
    let is-last = authors.len() == end
    let slice = authors.slice(i * 3, end)
    grid(
      columns: slice.len() * (100%,),
      gutter: 12pt,
      ..slice.map(author => align(center, {
        text(12pt, author.name)
        if "misc1" in author [
          \ #author.misc1 #h(8mm)
        ]
        if "department" in author [
          \ #emph(author.department)
        ]
        if "organization" in author [
          #author.organization #h(8mm)
        ]
        if "location" in author [
          \ #author.location
        ]
        if "email" in author [
           #link("mailto:" + author.email) #h(8mm)
        ]
        if "misc2" in author [
          #author.misc2
        ]
      }))
    )

    if not is-last {
      v(16pt, weak: true)
    }
  }
  v(40pt, weak: true)

  // Start two column mode and configure paragraph properties.
  //show: columns.with(2, gutter: 12pt)
  set par(justify: true, first-line-indent: 1em)
  show par: set block(spacing: 0.65em)

  // Display abstract and index terms.
  if abstract != none [
    #set text(weight: 700)
    //#h(1em) _Abstract_---#abstract
    #h(1.5em)#abstract

    #if index-terms != () [
      #h(1em)_Index terms_---#index-terms.join(", ")
    ]
    #v(2pt)
  ]

  // Display the paper's contents.
  body

  // Display bibliography.
  if bibliography-file != none {
    pagebreak()
    show bibliography: set text(9pt)
    bibliography(bibliography-file, title: text()[References], style: "apa")
  }
}
