import time

output="""
-------------------------------------------------------------
To run the docker contaner created using the Dockerfile
present in the current folder use:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$ docker run -p 5500:5500 -v $(pwd):/app <container_name> python3 client_end_module.py -l <user load> -r <duration>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Before running the container make sure the following requirements are met: 
* hosts, ports, etc are configured correctly in the config.py file.
* there is a correct components.json file for log retrieval
* initial_script.py is defined as per requirement
* perfcheck.py is also created containing the performance testing scripts for desired APIs
* APIs.json is also apropiately defined
-------------------------------------------------------------
"""
print(output)


