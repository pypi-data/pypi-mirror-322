
pub struct Milestone {
pub mut:
	oid string //is unique id for user in a circle, example=a7c  *
	signatures []Signature
	comments []string //list of oid's of comments linked to this story
    time_creation int //time when signature was created, in epoch  example=1711442827 *
	title string //title of a milestone example='this is our release tfgrif 3.1' *
	content string //description of the milestone="this is example content which gives more color" *
	owners []string //list of people (oid) who are the owners of this project example="f23" *
	notifications []string //list of people (oid) who want to be informed of changes of this milestone example="ad3"
	deadline int //epoch deadline for the milestone example="1711442827" *
	projects []Project //list of projects linked to milestone *
	comments []string //list of oid's of comments linked to this story
}


pub struct Project {
pub mut:
	oid string //is unique id for user in a circle, example=a7c  *
	signatures []Signature
	comments []string //list of oid's of comments linked to this story
    time_creation int //time when signature was created, in epoch  example=1711442827 *
	comments []string //list of oid's of comments linked to this story	
	title string //title of a story example='improve the UI for tfgrif 3.13' *
	project_type ProjectType // type of project *
	content string //description of what needs to be done example="this is example content" *
	owners []string //list of people (oid) who are the owners of this project example="f23" *
	notifications []string //list of people (oid) who want to be informed of changes of this project example="ad3"
	deadline int //epoch deadline for the project example="1711442827" *
	requirements []Requirement //list of requirements to fullfil linked to project
	stories []Story //list of stories linked to project *
	swimlanes SwimLaneTemplate //used to show e.g. Kanban
}


pub struct SwimLaneTemplate {
pub mut:
	oid string //is unique id for user in a circle, example=a7c  *
	signatures []Signature
	comments []string //list of oid's of comments linked to this story
    time_creation int //time when signature was created, in epoch  example=1711442827 *
	name string //name as need to be used in relation to project
	template []SwimLane
	comments []string //list of oid's of comments linked to this story
}



pub struct SwimLane {
pub mut:
	name string //short name for swimlane'
	purpose string //description, purpose of swimlane
	deadline int //epoch deadline for the swimlane, normally not used example="1711442827" *
}


enum ProjectType{
	product
	operations
	customerdelivery
	other
}
