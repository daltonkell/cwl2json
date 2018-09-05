## CWL To JSON

The [Common Workflow Language](https://commonwl.org)(CWL) was developed in an effort to homogenize processes that call command line tools. By using the CWL, one basically constructs a schema used to validate expected inputs and outputs of the tools being called.

For those command line tools exchanging information with a GUI, some developers may choose to use JSON for this interaction (especially in web-based scenarios). An [existing JavaScript library](https://github.com/DynaSlum/cwl-json-schema/) already parses CWL files and turns them into valid JSON; this libray is for developers working in Python.
