import myclient
import string
import random


def str_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


if __name__ == "__main__":
    pubkey = str_generator(size=10)
    name = str_generator(size=8)
    oid = str_generator(size=6)
    res = myclient.set(
        myclient.User(
            oid=oid,
            name=name,
            pubkey=pubkey,
            comments=list(),
            email=list(),
            signatures=list(),
            mobile=list(),
        )
    )
    print(res)

    res = myclient.list(args=myclient.UserFilter(name=name))
    print(res)

    res = myclient.get(oid=oid)
    print(res)

    res = myclient.delete(oid=oid)
    print(res)
