pub struct Message {
pub mut:
	oid string //is unique id for user in a circle, example=a7c  *
	signatures []Signature
	comments []string //list of oid's of comments linked to this story
    time_creation int //time when signature was created, in epoch  example=1711442827 *
	subject string //optional (never used for chat) *
	content string //the content of the message
	parent string //if its a child of other message *
	to []string //unique for user *
	to_group []string //unique for a group of people, see Group *
	time int //time when message was sent(epoch) example=1711442827  *
	msg_type MSGType //e.g. chat, mail, ... *
	content_type ContentType *
	tags string //our tag format e.g. color:red priority:urgent or just labels e.g. red, urgent (without :) *
}

enum MSGType{
	chat
	mail
}

enum ContentType{
	markdown
	text
	html
	heroscript
}