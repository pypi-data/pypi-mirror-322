module stellar
import freeflowuniverse.crystallib.core.texttools

pub struct DigitalAssets {
pub mut:


}

pub struct Owner {
pub mut:
    name        string
	accounts []Account
}

@[params]
pub struct AccountGetArgs{
pub mut:
	name string
	bctype BlockChainType	
}

pub fn (self DigitalAssets) account_get(args_ AccountGetArgs) !&Account {

    mut accounts := []&Account
	mut args:=args_

	args.name = texttools.name_fix(args.name)
    
    for account in self.accounts {
        if account.name == args.name && account.bctype == args.bctype {
            accounts<<&account 
        }
    }
    
    if accounts.len == 0 {
        return error('No account found with the given name:${args.name} and blockchain type: ${args.bctype}')
    } else if count > 1 {
        return error('Multiple accounts found with the given name:${args.name} and blockchain type: ${args.bctype}')
    }
        
    return accounts[0]
}

pub struct Account {
pub mut:
    name        string
    secret      string
    pubkey      string
    description string
    cat         string 
    owner 		string 
    assets      []Asset
	bctype 		BlockChainType
}

pub struct Asset {
pub mut:
	amount      int
	assettype 		AssetType
}

pub fn (self Asset) name() string {
	return self.assettype.name
}

pub struct AssetType {
pub mut:
    name        string
	issuer      string
	bctype 		BlockChainType
}

pub enum BlockChainType{
	stellar_pub
	stellar_test

}