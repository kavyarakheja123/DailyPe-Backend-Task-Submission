#basic flow for API end-point trigger using postman:- 

1. Make the Lambda function in AWS for desired functionality (CREATE_USER,GET_USER,DELETE_USER,UPDATE_USER)
2. Go to Configuration and Add permission - (full access to dynamodb) to configure the Lambda function code with desired DynamoDB table.
3. Get function URL for the Lambda function for API Calling.
4. We have used POSTMAN for calling API of respective functions.
5. While sending a http request for Lambda function choose the desired function (POST) in our case.
6. Set request body format as Raw (JSON).
7. At last click send to make the request and check its response ( we can see cloud-watch for detailed response of the API call)

---------------------------------------------------------------------------------------------------------------------------------------------
Function URLs for different functions:- 

create_user:- https://kngjl6utz6g7cwdfgu2o4mbwka0kxshg.lambda-url.ap-south-1.on.aws/

delete_user:- https://42gerorl6ixyhbrgl376uncuvi0faqkj.lambda-url.ap-south-1.on.aws/

get_user:- https://qzzf62c3gpmn5utarkg2ks3jb40gzfdt.lambda-url.ap-south-1.on.aws/

update_user:- https://z75hn2vrvom2l25l5xkhugyccu0bzjlm.lambda-url.ap-south-1.on.aws/


------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Manager table will have two attributes that are manager_id (uuid) and manager_name(string). We can add a new manager in the manager table and generated a uuid against each new manager. Active manager has been validated in the create_user code as well, which checks if an active member as the same uuid mentioned by user is present in the manager table or not. 
