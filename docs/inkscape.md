The SVG importer is quite fussy. To produce SVGs that will work well with it
using Inkscape, do the following:

- Under File -> Document Properties, set "Display units" to inches, and
  set "Scale x" and "Scale y" to 72.
  - This will produce SVGs with a coordinate system that corresponds to
    Cricut's, so your drawing will be scaled correctly.
- When saving your drawing, choose file type "Optimize SVG". In the dialog
  that pops up, make sure that "Convert CSS attributes to XML attributes" is
  checked.
  - This will help the importer recognize colors correctly. Inkscape defaults
    to putting stroke colors into CSS attributes, but the importer only
    recognizes XML.
