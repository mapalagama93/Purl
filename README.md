

![enter image description here](https://i.postimg.cc/28fCs1qt/purl.png)

# Better way to do API calls
Simply Purl is a command line tool to makes API calls. 
### How to install
You need python 3.1x and setuptools to install Purl
#### Option 1
Using python setuptools

    git clone https://github.com/mapalagama93/Purl.git
    cd Purl
    python setup.py install
#### Option 2
    git clone https://github.com/mapalagama93/Purl.git
And create alias in your `~/.bashrc` or `~/.zshrc`

    alias Purl="python prul.py"


### Purl sample request
Create `sample.yaml` file with below content.
```yaml
Method: GET
Endpoint: https://dummyjson.com/http/200
```
   
Run with following command
  

    purl -f sample.yaml
**Output**
![enter image description here](https://i.postimg.cc/Z5Mg2C0v/out.png)

### Purl initialize

   ```shell
   purl -i -e dev uat
   ```
purl -i or --initialize will initialize basic purl directory structure. Additionally you can specify environments to be created using -e option.

    MyFirstPurlProject/
	├─ configs/
	│  ├─ config.properties
	│  ├─ store.properties
	│  ├─ dev.properties
	│  ├─ uat.properties
	├─ sample.yaml

#### config.properties
Use this file to define environment independent properties. 
**Example**
```properties
    server=http://localhost:3000
    username=mapalagama
    password=mypass123
```
####  store.properties
Purl will use this property file to store dynamic variables. Normally you don't need to worry about this file
#### dev.properties/uat.properties
You can use to specify environment specific properties. When executing purl you can specify which files apply. Feel free to create your own environment properties files.

# Purl specs

Use `${variableName}` to inject properties in to prul yaml. Properties source order is,
 1. store.properties
 2. {env}.properties
 3. config.properties
Eg: If the property `username` define in both env properties and config properties value from env properties will be injected.

## Create Request

#### Define
`Define` field allow to define properties. These properties are persists and can be used in the same requests or subsequent requests. 

```yaml
Define:
  userEmail: "${fake.random_string()}@exmaple.com"
  userPhone: "${fake.random_number(10)}"

JsonBody: |
  {
	  "email" : "${userEmail}"
  }
```
 
#### Method, Endpoint, QueryParams, PathParams, Status
```yaml
Method: GET
Endpoint: https://example.com/user/:userId/posts
Status: 200
PathParams:
  userId: user123
QueryParams:
  page: 1
  size: ${page_size}
```
In the `Endpoint` field path parameters can be defined as `:userId` and values can be inject via `PathParams` field as a key-value pair. 

`Status` will be asseted with the response status code  

#### Headers
```yaml
Method: POST
Endpoint: https://example.com/user/posts
Headers:
  Authorization: ${authorization_token}
  Content-Type: application/json
  Custom-Header-One: My Custom header
```

### Request Body Types

#### JsonBody
`JsonBody` allows to add json to the request body
```yaml
Method: POST
Endpoint: https://example.com/user/posts
JsonBody: |
  {
    "id" : "1234",
    "post" : "This is my first post",
    "author" : "${userEmail}"
  }
```
#### FormParams
`FormParams` allows to add x-www-form-urlencoded body to the request
```yaml
Method: POST
Endpoint: https://example.com/user/posts
FormParams:
  id: 1234
  post: "This is my first post"
  author: ${userEmail}
```

#### MultipartData
`MultipartData` allows to add multipart form data to the request body including files and text
```yaml
Method: POST
Endpoint: https://example.com/user/photo
MultipartData:
  userId: "1234"
  profileImage: "@file://sample.jpg | profile.jpg | image/png"
```
Specify file syntax
`@file://path_to_the_file | filename | mimetype`


#### TextBody
`TextBody` allows to add text to the request body
```yaml
Method: POST
Endpoint: https://example.com/user/post
TextBody: "This test post"
```

## Handle Response

#### Captures
`Captures` allow to extract response data and store in the store.properties file. These capture values can be use in subsequent requests.
```yaml
Method: POST
Endpoint: https://example.com/user/posts
JsonBody: |
  {
    "id" : "1234",
    "post" : "This is my first post",
    "author" : "${userEmail}"
  }
Captures:
 authorization_token: "@headers Authorization"
 postId: "@body jsonpath $.id"
 statuCode: "@status"
 responseTime: "@time"
```
##### Capture Headers
`@headers` allow to capture response headers. Syntax as follow,
`@headers response_header_name`

##### Capture Body
`@body` allow to capture response body. Syntax as follows,
`@body capture_type capture_query`

To capture json response body value use jsonpath with json path syntaxt, eg:
`@body jsonpath $.user.id`
To learn more about jsonpath syntax visit : https://jsonpath.com/

##### xpath and regex capture type will be implemented in future releases.

#### Assertions

```yaml
Method: POST
Endpoint: https://example.com/user/posts
JsonBody: |
  {
    "id" : "1234",
    "post" : "This is my first post",
    "author" : "${userEmail}"
  }
Asserts:
  "status code is 200" : "@status |==| 200" # check if status code is 200
  "date header" : "@headers Date" # Check if Date header is not null
  "check value not null" : "@body jsonpath $.glossary.title" # Check if json body value is not null
  "check value equal" : "@body jsonpath $.glossary.title |==| example glossary" # Check if body value is equal to expected value
  "check value not equal" : "@body jsonpath $.glossary.title |!=| not example glossary" # Check if body value is not equal
```

#### Options

```yaml
Options:
  insecure: true # ignore ssl verification
  timeout: 20 # set custom timeout value, default is 60 seconds
 
```
  

