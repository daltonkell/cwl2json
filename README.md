## CWL To JSON

The [Common Workflow Language](https://commonwl.org)(CWL) was developed in an effort to homogenize processes that call command line tools. By using the CWL, one basically constructs a schema used to validate expected inputs and outputs of the tools being called.

For those command line tools exchanging information with a GUI, some developers may choose to use JSON for this interaction (especially in web-based scenarios). An [existing JavaScript library](https://github.com/DynaSlum/cwl-json-schema/) already parses CWL files and turns them into valid JSON; this libray is for developers working in Python.

CWL documents can be written in either YAML or JSON syntax. This module only converts CWLs written in the YAML syntax

### Convertable Document Types

The [Common Workflow Language](https://commonwl.org)(CWL) implements two document types a user can pass in as a .cwl. These are:
  1. CommandLineTool
  2. Workflow

In short, a CommandLineTool is a standlone document which executes a program upon receiving some input, produces some output, and then terminates. A Workflow, on the other hand, can describe multiple steps, where steps may be linked to outputs of others. 

This module only supports converting CommandLineTool documents from YAML syntax to valid JSON. Why? Have a look at the following:

 - a CommandLineTool example:
```
#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: bash
inputs:
  file:
    type: File    # <--- within the inputs, we declare the type of the specific input
                  # (among other things)
    inputBinding:
      position: 1
outputs: []
```
 - a Workflow example:

```
#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
  message: string  # <--- inputs in workflows do not allow typing; instead, they would
                   # be defined in one of these 
  infile : File                               |
                                              |
steps:                                        |
                                              |
  print:                                      /
    run: test-echo.cwl <----------------------
    in:                                       |
      message: message                        |
    out: []                                   |
                                              |
  wrf:                                        /
    run: wrf-test-cwl.cwl <-------------------                     
    in:
      file: infile
    out: []
outputs: []

```
