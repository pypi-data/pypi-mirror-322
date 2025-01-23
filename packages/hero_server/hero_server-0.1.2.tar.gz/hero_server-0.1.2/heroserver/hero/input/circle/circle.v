
pub struct Circle {
pub mut:
	oid string //is unique id for user in a circle, example=a7c  *
	signatures []Signature
	comments []string //list of oid's of comments linked to this story
    time_creation int //time when signature was created, in epoch  example=1711442827 *
	pubkey string //unique public key for account which is linked to group (all admins are signer) example=AABBCCDDEEFFGG
	name string //chosen name by user, need to be unique on tfgrid level example=myclub1 *
	description string //description of the circle example="my football club"
	admins []string //list of the pubkeys of the admins, admins can change the group
	stakeholders []string //list of people who are stakeholders (are also members)
	members []string //list of members in the group (can contribute)
	viewers []string //list of people who can only see info in group
	admin_quorum int //nr of signers needed for e.g. using treasury of group
	groups []Group //to define one or more groups in the circle
}

pub struct Group {
pub mut:
	name string //is the name of a group, unique per circle
	members []string //list of gids which are globally unique ids, is cid.oid example='abc.a3f6'
}
