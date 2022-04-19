# Path

Paths are specified in a restricted version of the [SVG path language](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths). They are sent directly to the Cricut driver as-is, so compatibility here depends mostly on what Cricut chooses to implement.

The commands `M`, `L`, `H`, `V`, `Z` for polylines are supported, and so is `C` for Bezier curves. Other commands (`S`, `Q`, `T`, `A`) are not supported. Commands with relative positioning (lowercase, like `l`) are not supported.

Commands and coordinates are separated by spaces, never commas, like `M 72 72 L 144 144 144 72 Z`. 
