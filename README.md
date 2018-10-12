## CWL To JSON

The [Common Workflow Language](https://commonwl.org)(CWL) was developed in an effort to homogenize processes that call command line tools. By using the CWL, one basically constructs a schema used to validate expected inputs and outputs of the tools being called.

For those command line tools exchanging information with a GUI, some developers may choose to use JSON for this interaction (especially in web-based scenarios). An [existing JavaScript library](https://github.com/DynaSlum/cwl-json-schema/) already parses CWL files and turns them into valid JSON; this libray is for developers working in Python.

CWL documents can be written in either YAML or JSON syntax. This module only converts CWLs written in the YAML syntax

### Convertable Document Types

The [Common Workflow Language](https://commonwl.org)(CWL) implements two document types a user can pass in as a .cwl. These are:
  1. CommandLineTool
  2. Workflow

In short, a CommandLineTool is a standlone document which executes a program upon receiving some input, produces some output, and then terminates. A Workflow, on the other hand, can describe multiple steps, where steps may be linked to outputs of others. 

This module only supports converting both CommandLineTool and Workflow documents from YAML syntax to valid JSON.

### CommandLineTool Example

   
__YAML__
```
    $base: "http://...",
    class: CommandLineTool,
    baseCommand: bash,
    inputs:
      file:
        type: File,
        inputBinding:
          position: 1
    outputs: []
```    
__Above YAML, loaded as dict__
```
    {
      
      $base: "http://...",
      class: CommandLineTool,          *To get to the below schema, follow these steps:*
      baseCommand: bash,
      inputs: { <--------------------- for each key inside inputs, if val is dict,
        file: {                        insert
          type: File,                  required: []; what goes inside [] will be mapped
          inputBinding: {
            position: 1
          }
        } <--------------------------- also inside inputs, we insert a new dict:
      },                               properties: { }
      outputs: []                                   |--> inside this dict, for each item in required,  
    }                                                    insert:
                                                         item: {type: <sometype>}
```
__Valid JSONSchema of the above:__
```
    {
      
      $base: "http://...",
      class: CommandLineTool,
      baseCommand: bash,
      properties: {             # properties1
        file: {
          type: File,
          inputBinding: {
            position: 1
          },
          required: [
            path
          ]
        },
          required: [
            path
          ]
        },
        properties: {           # properties2 
          path: {
            type: string
          }
        }
      },
      outputs: []
    }
    
```

### Workflow Example

__Workflow .cwl (YAML format)__
```
    cwlVersion: v1.0
    class: Workflow
    inputs:
      message: string
      infile : File?  # <- ----------------------- ? indicates optional input
    
    steps:
     
      print:
        run: test-echo.cwl
        in: 
          message: message
        out: []
    
      wrf:
        run: wrf-test-cwl.cwl
        in:
          file: infile
        out: []
    outputs: []
```
__Above YAML, loaded as dict__
```
    {
      cwlVersion: v1.0,
      class: Workflow,
      inputs:{
        message: string
        infile : File?
      },
      steps:{
       
        print:{
          run: test-echo.cwl
          in: 
            message: message
          out: []
        }
        wrf:{
          run: wrf-test-cwl.cwl
          in:
            file: infile
          out: []
        }
      },
      outputs: []
    }
```
__In proper JSONSchema form:__
```
    {
      cwlVersion: v1.0,
      class: Workflow,
      properties:{  # <--------------- use properties instead of inputs
        message: {
          type: string  # <----------- give each property a type
        },
        infile :{
          type: object
        }
      },
      required: [message], # <-------- identify the required properties
      steps:{
       
        print:{
          run: test-echo.cwl
          in: 
            message: message
          out: []
        }
        wrf:{
          run: wrf-test-cwl.cwl
          in:
            file: infile
          out: []
        }
      },
      outputs: []
    }
```
