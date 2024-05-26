#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: merge_configuration

short_description: Merge settings into the Minecraft server configuration

version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    path:
        description: The path to the configuration file
        required: true
        type: str
    settings:
        description:
            - Settings to merge in a key-value format
        required: false
        type: dict

author:
    - Matthias Wolf (@matz-e)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule

import re


_KEY_VALUE = re.compile(r"^([A-Za-z0-9._-]+)(\s*[:=]?\s*)(.+)(\s*)$")


def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        settings=dict(type='dict', required=True)
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    filename = module.params["path"]
    settings = module.params["settings"]

    with open(filename) as fd:
        lines = fd.readlines()

    new_lines = []
    delim = "="
    rest = "\n"
    for line in lines:
        new_line = line
        if m := _KEY_VALUE.match(new_line):
            key, delim, value, rest = m.groups()
            if key in settings:
                new_value = settings.pop(key)
                if new_value != value:
                    result["changed"] = True
                    new_line = f"{key}{delim}{new_value}{rest}"
        new_lines.append(new_line)
    for key, value in settings.items():
        new_line = f"{key}{delim}{value}{rest}"
        new_lines.append(new_line)
        result["changed"] = True

    if module.check_mode:
        module.exit_json(**result)

    if result["changed"]:
        with open(filename, "w") as fd:
            fd.writelines(new_lines)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
