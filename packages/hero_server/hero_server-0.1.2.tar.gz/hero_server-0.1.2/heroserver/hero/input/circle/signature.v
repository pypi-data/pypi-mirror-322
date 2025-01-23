
//is always part of another object
pub struct Signature {
pub mut:
	pubkey string //the public key of the signer example="3NsaCWs88aUnSyzGjGPE7vFE7zqRPLZhNe4Rs9CJi2kX" *
	content string //content that got signed  example=some content
	signature string //signature of the content  example=5eykt4dfasdfadfadfEpY1vzqKqZKvdpHGqpCD3ZKFSs
	time_creation int //time when signature was done, in epoch  example=1711442827 *
	comments []string //list of oid's of comments linked to this story
}

