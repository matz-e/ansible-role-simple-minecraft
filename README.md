# ansible-role-simple-minecraft

Basic role to configure a Minecraft server running on Fedora.  Will create a `minecraft`
user and use it to run the server, based on the latest JAR provided by Mojang.

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
