
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

    purl -i -e dev uat
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

    server=http://localhost:3000
    username=mapalagama
    password=mypass123

####  store.properties
Purl will use this property file to store dynamic variables. Normally you don't need to worry about this file
#### dev.properties/uat.properties
You can use to specify environment specific properties. When executing purl you can specify which files apply. Feel free to create your own environment properties files.

### Purl specs

```yaml
Method: GET
Endpoint: ${server}/users/:userId/posts
Status: 200 # Expect 200 status code
# Define query parameters
QueryParams:
  page: 1
  size: 10

# Define path parameters. :userId in the url will be replace with following userId value.
PathParams:
  userId: user123

Headers:
  Authorization: Basic ${auth_header}

FormParams:
  myFormKey: Form parameter value.

JsonBody: |
  {
    "myJsonKey" : "myJsonValue"
  }

TextBody: |
  Sample text body 


MultipartData:
  myTextKey: My text value 
  file2: "@file://files/sample.jpg | ifilename2.jpeg | image/jpeg" # filepath | filename | content type

# Assertion Syntax
# @status to get response status code
# @heaader to get reponse headers : @header Authorization 
# @body to capture body and then specify parse method such as regex, jsonpath, xpath : @body jsonpath $.user.name
Asserts:
  "status code is 200" : "@status |==| 200" # check if status code is 200
  "date header" : "@headers Date" # Check if Date header is not null
  "check value not null" : "@body jsonpath $.glossary.title" # Check if json body value is not null
  "check value equal" : "@body jsonpath $.glossary.title |==| example glossary" # Check if body value is equal to expected value
  "check value not equal" : "@body jsonpath $.glossary.title |!=| not example glossary" # Check if body value is not equal

# Capture response data. These capture data will persists in configs/store.properties file
Captures:
  authorizationToken : "@header authorization"
  username: "@body jsonpath $user.name"

Options:
  insecure: true # ignore ssl verification
  timeout: 20 # set custom timeout value, default is 60 seconds
  

```
  

