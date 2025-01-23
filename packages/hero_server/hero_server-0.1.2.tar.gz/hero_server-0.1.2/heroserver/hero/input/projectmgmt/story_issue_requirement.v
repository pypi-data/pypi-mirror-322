
pub struct Story {
pub mut:
	oid string //is unique id for user in a circle, example=a7c  *
	signatures []Signature
	comments []string //list of oid's of comments linked to this story
    time_creation int //time when signature was created, in epoch  example=1711442827 *
	title string //title of a story example='improve the UI for tfgrif 3.13' *
	content string //description of what needs to be done example="this is example content" *
	assignees []string //list of people (oid) who are the owners/executes of this story example="f23" *
	project string //optional oid for the project linked to this Story *
	swimlane string //name of the swimlane story is on *
	milestone []string //optional list of milestones linked to this Story (as oid) example="h62,t3fd" *
	notifications []string //list of people (oid) who want to be informed of changes example="ad3"
	deadline int //epoch deadline for the Story example="1711442827" *
	requirements []Requirement //list of requirements to fullfil
	issues []Issue //list of issues linked to story (can be bug, feature request, question, ...) *
}


pub struct Requirement {
pub mut:
	comments []string //list of oid's of comments linked to this story
    time_creation int //time when signature was created, in epoch  example=1711442827 *
	requirement_type RequirementType *
	title string //title of a story example='improve the UI for tfgrif 3.13' *
	content string //description of what needs to be done example="this is example content" *
	story string //the stories linked to requirements (as oid) example="h62,t3fd"
	comments []string //list of oid's of comments linked to this story
}

pub struct Issue {
pub mut:
	oid string //is unique id for user in a circle, example=a7c  *
	signatures []Signature
	comments []string //list of oid's of comments linked to this story
    time_creation int //time when signature was created, in epoch  example=1711442827 *
	issue_type IssueType *
	title string //title of a story example='improve the UI for tfgrif 3.13' *
	content string //description of what needs to be done example="this is example content" *
	assignees []string //list of people (oid) who are the owners/executes of this story example="f23" *
	notifications []string //list of people (oid) who want to be informed of changes example="ad3"
	deadline int //epoch deadline for the Story example="1711442827" *
	issues []Issues //list of issues linked to story (can be bug, feature request, question, ...) *
	comments []string //list of oid's of comments linked to this story
}


enum IssueType{
	bug
	feature
	question
	other
	task
}

enum RequirementType{
	feature
	performance
	scale
	operations
	ui
	other
}
