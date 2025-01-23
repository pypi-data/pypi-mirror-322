
how do I use heroscript for story and task management

-------------------------

heroscript has basic notations to deal with stories and tasks

when the user asks to translate an story or task action to heroscript use following rules and see example below

- all dates are in europe style: Format: DD/MM/YYYY e.g. 06/07/2023
- if year not specified by user then always use current year which is 2024
- if month not specified use current month which is september or month 9
- title is always required, if attendies or people mentioned they should be on assignment list
- date & time & duration is optional
- don't use comments in the heroscript (means no // at end of line for heroscript)
- duration expressed as 1m, 1h, 1d  (minute, hour, day)
- deadline is or a date or +1h, +1d, .. the + means time from now, just list same way e.g. +1h
  - 1 months is done as 30 days or +30 days, 2 months 60 days, ... (which means +30d for 1 month)
- stories cannot have a date, if a date given, giver an error
- owners, assignees, contributors, executors is all the same
- the description is always in markdown format
- the description always has the title repeated
- the description has title, purpose, deliverables
- try to figure out what purpose and deliverables are
- purpose is put as list in markdown

```heroscript

//to add a new story
!!story.add
    title:'need to improve UI for version 1.0'
    owners:'karoline, kristof'
    description:'
        # need to improve UI for version 1.0

        We got some complaints from our userbase and its overdue.

        ## deliverables

        - [ ] specs and check with kristof
        - [ ] implement mockup
        - [ ] implement prototype

        '


//to add a new task, which might (optional) be linked to a story
!!task.add
    title:'let our userbase know'
    story:10
    owners:'kristof'
    deadline:'+10d'
    description:'
        write email to userbase
        ask tom to check
        '



```
