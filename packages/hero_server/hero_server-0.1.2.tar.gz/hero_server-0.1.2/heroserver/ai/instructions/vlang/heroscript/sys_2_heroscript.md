
'heroscript' is a simple declarative language in following form

```heroscript
!!mother.define
    myname:'mymama'
    mylist:'20,200'
    myint:2                   

//this is how we define a child (is in list)
!!child.define
    mother:'mymama'
    name:'florine'
    length:100
    description:'
        multiline is supported 
        '                

!!child.define
    mother:'mymama'
    name:'aurelie'
    length:60
    description:'
        multiline is supported 
        now for aurelie
        '
```

some rules


- '0,70' is a list of 2 (when comma in example its a list)
- never use [] in lists, just have comma separation in between quotes ''
- in lists always put lowercase names
- node_name:'silver' is same as node_name:silver, when spaces always '' around
- // means comment
- all dates are in europe style: Format: DD/MM/YYYY e.g. 06/07/2023, always specify year

the corresponding model in vlang would be

```vlang
pub struct Mother {
pub mut:
    myname string
    mylist [20,200]
    myint 2
    children []Child
}

pub struct Child {
pub mut:
    name string
    length int
    description string
}
```


In a heroscript file, the second line after the `!!<module>.<name>.define` block is typically used to define the properties or fields of the struct being defined. [1] The properties are specified as <property_name>:<value>, with each property on a new line. For example:


