all_required = [] # updated with every entry in all 'required' lists

class Converter(object):
    
    """
    Convert CWL in YAML syntax to valid JSON Schema syntax

    CommandLineTool Example
    =======================
    
    YAML example
    ------------
    $base: "http://...",
    class: CommandLineTool,
    baseCommand: bash,
    inputs:
      file:
        type: File,
        inputBinding:
          position: 1
    outputs: []
    
    Above YAML, loaded as dict
    --------------------------
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
    Valid JSONSchema of the above:
    ------------------------------
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
        properties: {           # properties2 
          path: {
            type: string
          }
        }
      },
      outputs: []
    }
    

    Workflow Example
    ================

    Workflow .cwl (YAML format)
    ---------------------------

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

    Above YAML, loaded as dict
    --------------------------

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

    In proper JSONSchema form:
    --------------------------

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
    """

    def __init__(self):
        self.cwl2jsonmap = {  # CWL types to JSON types
          "none": 'null',
          "boolean": 'boolean',
          "int": 'integer',
          "long": 'number',
          "float": 'number',
          "double": 'number',
          "string": 'string',
          "File": 'object',
          "Directory": 'object',
          # 'class' synonymous to 'type'
          "class": "type"
        }

        self.required_map = {  # required fields for input keys
          "file": 'path'
        }

        self.fieldtype = {  # types for the required fields
            'path': 'string'
        }

    def map_required(self, key):
        """Take a given input key and ouput the name of the field
        a user must supply a value for in order for that input key
        to be valid in a JSONSchema. For example, if the key is `file`
        a required field in a JSONSchema would be `path`, as the user
        must supply a valid path to this file.

        :param str key: input key"""

        # NOTE bit inefficient right now?
        for _k in self.required_map.keys():
            if _k in key: # if any part of the key is in _k (e.g. file in prefile)
                key = _k # rename the key so we get the right type
        field = self.required_map.get(key, None)
        return field

    def field_type(self, field):
        """Take a given field and output the type that field should be.

        :param str field: name of field"""

        _type = self.fieldtype.get(field, None)
        return _type


    def convert(self, cdict):
        """Main converter method. Loops through key-value pairs in a YAML dict 
           (loaded from a .cwl) and creates a corresponding JSON schema. This 
           schema can then be used to validate an input .yml file, which is 
           similarly loaded as a dictionary via yaml and json modules. 

           :param dict cdict: JSON dictionary from CWL file
           :param bool is_schema: specify if returned JSON should be a schema"""
        if 'inputs' in cdict.keys():
            for k, v in cdict['inputs'].items():
                if isinstance(v, dict): # insert key `required: []`
                    cdict['inputs'][k]['required'] = [self.map_required(k)]
                    all_required.append(self.map_required(k)) # store all here
            cdict['inputs']['properties'] = {} # insert properties2 dict
            for field in all_required:
                cdict['inputs']['properties'][field] = {'type': self.field_type(field)}
        
        # then we convert all the CWL types to JSON types
        out = self.map2json(cdict)
        return out


    def convert_workflow(self, wdict):
        """Insert the proper nested fields into a Workflow document to make it
        a valid JSONSchema.

        :param dict wdict: dict loaded from a Workflow document"""

        _inputs = wdict['inputs'] #inputs dict
        req = [] # empty array for required, to be updated
        for k, v in _inputs.items():
            # create the proper nesting
            if v.endswith('?'): # optional, do not add to required
                v = v.replace('?', '') # strip off the '?'
            else:
                req.append(k) # add key to required
            _inputs[k] = {'type': self.cwl2jsonmap.get(v)}

        wdict['required'] = req # put the required field into the schema
        wdict['properties'] = _inputs # rename the inputs key, delete inputs key
        del wdict['inputs']
        return wdict 

    def map2json(self, _dict):
        """Map YAML types to JSON types from a dictionary

           :param dict _dict: dictionary loaded from YAML file whose
               values may be YAML types. If values are another dictionary,
               the method operates recursively and loops through those keys."""

        out = dict(_dict) # create new memory address to avoid mutating orig
        for k, v in out.items(): # loop through all k-v pairs
            if not (isinstance(v, dict) or isinstance(v, list)) and v in self.cwl2jsonmap.keys():
                _v = self.cwl2jsonmap.get(v) # if not a dict, execute the mapping
            elif isinstance(v, dict): # if dict, need to loop through
                _v = self.map2json(v) # recursion
            elif v == []:
                _v = 'null' # empty array in CWL means nothing (usually found in 'required' field)                 
            else:
                _v = v # don't change the value
            out[k] = _v
        if out.get('required') == []:
            out['required'] = 'null' # empty array in CWL means nothing (usually found in 'required' field) 
        if 'inputs' in out.keys(): # rename to properties for validation keyword
            props = out['inputs']
            del out['inputs']
            out['properties'] = props
        return out
