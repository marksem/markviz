"""
markviz - Browser-based visualizer of an RDF file

Works best on smallish RDF, since visualizes all of it.

Author: Mark Wallace
"""

import sys
import rdflib

def main():
  """
  The main program
  """
  file = sys.argv[1]
  g = rdflib.Graph()
  loadGraphFromFile(g,file)
  
  print(html_pre)
  rdf2cy(g)
  print(html_post)

#--------------------------------------------
# Global vars
#--------------------------------------------

ns = [
  ["rdf:",   "http://www.w3.org/1999/02/22-rdf-syntax-ns#"],
  ["rdfs:",  "http://www.w3.org/2000/01/rdf-schema#"],
  ["xsd:",   "http://www.w3.org/2001/XMLSchema#"],
  ["owl:",   "http://www.w3.org/2002/07/owl#"],
  ["dc:",    "http://purl.org/dc/elements/1.1/"],
  ["skos:",  "http://www.w3.org/2004/02/skos/core#"],
  ["gist:",  "http://ontologies.semanticarts.com/gist/"]
]

#--------------------------------------------
# Functions
#--------------------------------------------

def rdf2cy(g):
  """
  Print Cytoscape JS statements directly from RDF graph
  """
  for subj,pred,obj in g:
    subj = toQname(subj)
    pred = toQname(pred)
    obj = toQname(obj)

    # Skip annoying owl:NamedIndividual in visualizations
    if obj.endswith("NamedIndividual"):
      continue

    # handle possible single quotes in data properties
    obj = obj.replace("'","\\'")

    # write subject nodes
    s = "    { data: { id: '"
    s += subj
    s += "'}},"
    print(s)
    
    # write object nodes
    s = "    { data: { id: '"
    s += obj
    s += "'}},"
    print(s)
    
    # write edges
    s = "    { data: { source: '"
    s += subj
    s += "', target: '"
    s += obj
    s += "', relname: '"
    s += pred
    s += "'}},"
    print(s)
    
  return None

def toQname(str):
  """
  Convert long URIs to QNames where possible.

  Uses global 'ns' variable.
  """
  # try to put in ns prefix
  for obj in ns:
    str = str.replace(obj[1],obj[0])
  # shorten it if ns didn't match
  str = str[str.rfind("#")+1:]
  str = str[str.rfind("/")+1:]
  return str

def loadGraphFromFile(g,file):
  """ Load RDF graph from a local file or URL
  """
  if file.upper().endswith("TTL"):
    g.parse(file,format="ttl")
  else:
    g.parse(file)


#--------------------------------------------
# Preformatted HTML for output
#--------------------------------------------

html_pre = """<!DOCTYPE html>
<html>
<head>
  <meta name="description" content="[An example of getting started with Cytoscape.js]" />
  <meta charset=utf-8 />
  <meta name="viewport" content="user-scalable=no, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, minimal-ui">
  <title>MarkViz</title>
  <style>
	body { font: 14px helvetica neue, helvetica, arial, sans-serif;	}
	#cy { height: 100%; width: 100%; position: absolute; left: 0; top: 0; }
	#info { color: #c88; font-size: 1em; position: absolute; z-index: -1; left: 1em; top: 1em; }
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/2.7.15/cytoscape.min.js"></script>
  <script src="cytoscape.min.js"></script>
  <script>
document.addEventListener('DOMContentLoaded', function(){ // on dom ready

var cy = cytoscape({
  container: document.getElementById('cy'),
    
  boxSelectionEnabled: false,
  autounselectify: true,
  
  style: cytoscape.stylesheet()
    .selector('node')
      .css({
        'content': 'data(id)', // Nodes use id for label for now
        'text-valign': 'center',
        'background-color': '#999',
      })
    .selector('edge')
      .css({
        'content': 'data(relname)',  // Edges use name for label, if no name, then no label. :)
        'curve-style': 'bezier',
        'target-arrow-shape': 'triangle',
        'target-arrow-color': '#ccc',
        'line-color': '#ccc',
		'color': 'lightblue',
		'font-size': '12px',
        'width': 1
      })
    .selector(':selected')
      .css({
        'background-color': 'black',
        'line-color': 'black',
        'target-arrow-color': 'black',
        'source-arrow-color': 'black'
      })
    .selector('.faded')
      .css({
        'opacity': 0.25,
        'text-opacity': 0
      }),
  
  elements: [
  // *** DATA ELEMENTS GO BETWEEN THESE COMMENTS ***
  //

"""

html_post="""

    // 
    // *** DATA ELEMENTS GO BETWEEN THESE COMMENTS ***
    ],
  
  layout: {
    name: 'cose', // values; cose, random, grid, circle, concentric, breadthfirst, 
    padding: 10,
    randomize: true
  }
});

cy.on('tap', 'node', function(e){
  var node = e.cyTarget; 
  var neighborhood = node.neighborhood().add(node);
  
  cy.elements().addClass('faded');
  neighborhood.removeClass('faded');
});

cy.on('tap', function(e){
  if( e.cyTarget === cy ){
    cy.elements().removeClass('faded');
  }
});

	
}); // on dom ready

  </script>
</head>
  
<body>
  <div id="cy"></div>
</body>
</html>

"""


#--------------------------------------------
# Run main?
#--------------------------------------------
if __name__ == "__main__":
  main()
