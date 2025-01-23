
how can I query a webservice over http using vlang for a simple post request


-------------------


```vlang

import freeflowuniverse.crystallib.clients.httpconnection
import json


mut conn := httpconnection.new(name: 'test', url: 'https://jsonplaceholder.typicode.com/')!


// adding a header field to be used in all requests.
// default header have the field Content-Type set to 'application/json',
// but we should reconsider this and leave it out, set it manually when needed
conn.default_header.add(.content_language, 'Content-Language: en-US')

// Getting a blog post with id 1 (us example), should be fresh response from the server
mut res := conn.send(prefix: 'posts', id: '1')!

// Result object have minimum fileds (code, data) and one method is_ok()
println('Status code: ${res.code}')

// you can check if you got a success status code or not
println('Success: ${res.is_ok()}')

// access the result data
println('Data: ${res.data}')


```