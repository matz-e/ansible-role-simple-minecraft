# ansible-role-simple-minecraft

Basic role to configure a simplistic Minecraft server running on Fedora.  Will create a
`minecraft` user and use it to run the server, based on the latest JAR provided by Mojang.

This role also serves as a playground to test out Python modules, used to configure the
`server.properties`.  The Python module only handles the very basic principles of the Java
properties format, e.g., will not be able to handle multi-line properties.  But it can be
used to update settings as required and will propagate if any of the desired settings
were changed back to the ansible host.

Clone into a role directory:
```console
mkdir roles
gh repo clone matz-e/ansible-role-simple-minecraft roles/simple-minecraft
```
and then include in a playbook like:
```yaml
- name: Provide Minecraft
  hosts: minecraft_server
  become: true
  roles:
    - simple-minecraft
```

Use at your own risk.
