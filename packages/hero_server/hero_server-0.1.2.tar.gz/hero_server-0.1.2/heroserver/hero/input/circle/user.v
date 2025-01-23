pub struct User {
pub mut:
	oid string //is unique id for user in a circle, example=a7c  *
	signatures []Signature
	comments []string //list of oid's of comments linked to this story
    time_creation int //time when signature was created, in epoch  example=1711442827 *
	pubkey string //Unique key for a user, is on blockchain solana, also address where money goes example="3NsaCWs88aUnSyzGjGPE7vFE7zqRPLZhNe4Rs9CJi2kX" *
	name string //chosen name by user, need to be unique on tfgrid level example=myname *
	ipaddr string //mycelium ip address  example="fe80::5f21:d7a2:5c8e:ecf0" *
	email []string //Email addresses example=info@example.com,other@email.com  *
	mobile []string //Mobile number example="+324444444" *
}
