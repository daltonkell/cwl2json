cwl2jsonmap = {
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

class Converter(object):
    """Convert CWL in YAML syntax to valid JSON Schema syntax"""
    
    def __init__(self):
        pass

    def convert(self, jsondict, is_schema=False):
        """Main converter method. Loops through key-value pairs in a YAML dict 
           (loaded from a .cwl) and creates a corresponding JSON schema. This 
           schema can then be used to validate an input .yml file, which is 
           similarly loaded as a dictionary via yaml and json modules. 

           :param dict jsondict: JSON dictionary from CWL file
           :param bool is_schema: specify if returned JSON should be a schema"""

        fp_insert = {
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Filepath to said file"
                }
            }
        }
        
        jout = {}
        if is_schema: # make a full JSONSchema dict
            jout.update({
                   '$schema': 'http://json-schema.org/draft-07/schema#',
                   'type': 'object',
                   'title': "SchemaFromCWL",
                   'properties': {},
                   })
        for k, v in jsondict.items(): # map to valid JSON type
            if isinstance(v, dict): # send to map2json to loop & map types
                if "file" in v.keys():
                     #pdb.set_trace()
                     v['file']['required'] = ["path"] # should be inside "file"
                     # insert these necessary keys to be able to validate the fp is a string
                     v.update(fp_insert)
                _v = self.map2json(v)
            elif v == []:
                _v = 'null'
            else:
                _v = v # don't change value
            jout[k] = _v

        if 'inputs' in jout.keys(): # rename to properties for validation keyword
            jout['properties'] = jout['inputs']
            del jout['inputs']
        return jout

    def map2json(self, _dict):
        """Map YAML types to JSON types from a dictionary

           :param dict _dict: dictionary loaded from YAML file whose
               values may be YAML types. If values are another dictionary,
               the method operates recursively and loops through those keys."""

        out = dict(_dict) # create new memory address to avoid mutating orig
        for k, v in out.items(): # loop through all k-v pairs
            if not (isinstance(v, dict) or isinstance(v, list)) and v in cwl2jsonmap.keys():
                _v = cwl2jsonmap.get(v) 
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
