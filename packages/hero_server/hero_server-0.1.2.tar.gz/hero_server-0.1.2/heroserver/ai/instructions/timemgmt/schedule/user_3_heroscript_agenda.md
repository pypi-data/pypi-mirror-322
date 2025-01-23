
how do I use heroscript for agenda management

-------------------------

heroscript has basic notations to deal with calendars and events

when the user asks to translate an calendar action to heroscript use following rules and see example below

- all dates are in europe style: Format: DD/MM/YYYY e.g. 06/07/2023
- if year not specified by user then always use current year which is 2024
- if month not specified use current month which is september or month 9
- date, title is always required, if attendies or people mentioned they should be on attendies list
- don't use comments in the heroscript (means no // at end of line for heroscript)
- default duration is 1h, also ok 15m (15 min), 1 day

```heroscript

//to add item in agenda
!!calendar.add
    date:'30-10-24'
    time:'10pm'
    duration:'1h'
    title:'meeting with tech team'
    attendies:'user1, kristof, ...'
    description:''

//to delete (can use words cancel, delete)
!!calendar.delete
    id:100

//to reschedule e.g. delay, 1d stands for 1 day, 1w for 1 week, 1h for 1 hour
!!calendar.delay
    id:100
    delay:'2d'

//when e.g. reschedule or delete, we can inform participants
!!calendar.inform
    id:100


```
