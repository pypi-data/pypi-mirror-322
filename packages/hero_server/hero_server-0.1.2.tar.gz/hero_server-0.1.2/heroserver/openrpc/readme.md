## example how to use

```python

from openrpc import openrpc_spec_write

#load all the specs and write the result in a dir
openrpc_spec = openrpc_spec_write(
    path="~/code/git.ourworld.tf/projectmycelium/hero_server/generatorexamples/example1/specs"
    dest="/tmp/openrpc/example1"
)

```

## internal process

- first we clean the code to only have relevant parts
- then we find the blocks, can be function, enum or struct
- then we parse the blocks
