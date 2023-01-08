# slicebug
slicebug is a command-line tool for preparing and executing cutting jobs on Cricut cutters.

slicebug interacts with cutters by reusing undocumented components of Cricut Design Space. It is not developed or authorized by Cricut. Using slicebug might damage your cutter.

# Requirements
- Windows
- Cricut Design Space installed and used at least once

slicebug is developed in Python 3.10. You don't need Python to run it, just download a compiled version by clicking the "Releases" section on the right.

# Usage example

slicebug is a command-line utility, so you'll need a terminal to use it. On Windows, I recommend [Windows Terminal](https://aka.ms/terminal).

After downloading and unpacking slicebug, go to the directory where you unpacked it:

```
PS C:\Users\Bill> cd Downloads\slicebug
PS C:\Users\Bill\Downloads\slicebug>
```

The first time you use slicebug, you'll need to "bootstrap" it. This will copy some information over from your install of Cricut Design Space:

```
PS C:\Users\Bill\Downloads\slicebug> .\slicebug.exe bootstrap
Importing plugins from C:\Users\Bill\AppData\Local\Program\Cricut Design Space.
...
Machines imported.
```

Take a quick look at the output and make sure there aren't any errors. If everything went well, try using the `list-materials` and `list-tools` commands:

```
PS C:\Users\Bill\Downloads\slicebug> .\slicebug.exe list-materials
...
Cardstock:
  ...
  - [218] Light Cardstock - 65 lb (176 gsm)
  - [ 19] Medium Cardstock - 80 lb (216 gsm)
  ...
...
PS C:\Users\Bill\Downloads\slicebug> .\slicebug.exe list-tools 218
Tools for Light Cardstock - 65 lb (176 gsm):
  - scoring_stylus
  - scoring_wheel
  - pen
  ...
```

To cut something out, you'll first need to create a _plan_. A plan is a file containing full instructions for how to cut a single mat: what to cut and with which tools. slicebug includes a command that can create a plan from an SVG, picking tools based on stroke color:

```
PS C:\Users\Bill\Downloads\slicebug> .\slicebug.exe plan examples\blobs.svg blobs_plan.json `
>> --material 218 `
>> --map 000000:fine_point_blade `
>> --map ff0000:pen `
>> --map 0000ff:pen
```
(The tick \` at the end of a line means that the command continues on the next line. Try `slicebug plan --help` to learn about other options that this command accepts.)
```
Found 3 paths:
 - 1 paths with stroke color #000000, mapped to fine_point_blade.
 - 1 paths with stroke color #0000ff, mapped to pen.
 - 1 paths with stroke color #ff0000, mapped to pen.
```
You should now have a `blobs_plan.json` file you can use for a cut:
```
PS C:\Users\Bill\Downloads\slicebug> .\slicebug.exe cut blobs_plan.json
Load the following tools:
Clamp A: pen (#000000)
Clamp B: fine_point_blade

Insert mat and press the Load/Unload button.
...
```

Just follow the instructions and your cut should complete!

# Things that don't work yet

- Testing/support for anything other than the original Cricut Maker
  - Basic cutting will likely work on other machines supported by Cricut Design Space---please try it and report back!
  - Features specific to other machines, like Smart Materials, are not supported yet.
- Operating systems other than Windows
  - macOS: should be fairly easy, just some hardcoded paths that need tweaking.
  - Linux: 
  	- CricutDevice.exe does not run under Wine, but perhaps it does under one of the forks?
    - `slicebug plan` works under Linux already if you copy the bootstrapped files from a Windows machine and manually install usvg.
- Print then Cut
  - Should be doable.
