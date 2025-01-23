//for get rest statement on on pubkey_existing_user, pubkey_new_user
//for list rest api statement do on from time_invited, to time_invites, from time_installed, to time_installed and pubkey_existing_user, pubkey_new_user
pub struct Referral {
pub mut:
	oid string //is unique id in a circle, example=a7c  *
	comments []string //list of oid's of comments linked to this story
	pubkey_existing_user string //the one who received the invitations
	pubkey_new_user string //the ones who get the invitation
	time_invited int	//time invitation was sent example=1711442827 *
	time_installed int //time when tfconnect was installed epoch) example=1711442827 *
	rewards []Reward
}

pub struct Reward {
pub mut:
	reward_time int //time when reward was done (as epoch) example=1711442827
	asset_type string //e.g. INCA, TFT example=tft
	amount u64 //amount of tokens send example=100
	transaction_id string //to find back on blockchain, is a transaction id on solana 
	reward_type RewardType
}

enum RewardType{
	l1 //is first level reward
	l2 //is 2nd level reward
}
