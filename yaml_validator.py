#!/usr/bin/env python

import yaml
from cerberus import Validator

template_file = "m_template.yaml"
source_file = "m_sample.yaml"
def load_source_yaml(src_yaml):
    with open(src_yaml, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exception:
            raise exception

## Now, validating the yaml file is straightforward:

template_schema = eval(open(template_file, 'r').read())
validation_handler = Validator(template_schema)

source_doc = load_source_yaml(src_yaml=source_file)
validation_result = validation_handler.validate(source_doc, template_schema)

if validation_result == True:
    print(f"\n\nSource file ({source_file}) vaildation is complete and successful - good to proceed to furhter\n\n")
else:
    print(f"\n\nSource file ({source_file}) vaildation is failed - ABORT further processing (please check below for details)\n\n")

validation_errors = validation_handler.errors
count=0
for element in validation_errors:
    count += 1
    print(f"{count:3}. {element} - {validation_errors[element]}")