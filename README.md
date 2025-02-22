# URL Shortener Take-Home Project
Welcome to the Pocket Worlds URL Shortener Take-Home Project! In this repository, we'd like you to demonstrate your
engineering skills by creating a small Python project that implements a URL Shortener web service.

This project will serve as the primary jumping off point for our technical interviews. We expect you to spend a 
couple of hours building an MVP that meets the requirements in the Product Description. You are free to implement 
your solution and modify the provided template in the way that makes the most sense to you, but make sure to 
update the README accordingly so that it's clear how to run and test your project. During the interviews, you will 
be asked to demo your solution and discuss the reasoning behind your implementation decisions and their trade-offs. 
Be prepared to share your screen for live coding and problem solving with your interviewers based on this discussion.

## Project Description
Using the provided Python project template, your task is to implement a URL Shortener web service that exposes
the following API endpoints:

* POST `/url/shorten`: accepts a URL to shorten (e.g. https://www.google.com) and returns a short URL that 
  can be resolved at a later time (e.g. http://localhost:8000/r/abc)
* GET `r/<url_code>`: resolve the given short URL (e.g. http://localhost:8000/r/abc) to its original URL
  (e.g. https://www.google.com). If the short URL is unknown, an HTTP 404 response is returned.

Your solution must support running the URL shortener service with multiple workers.

For example, it should be possible to start two instances of the service, make a request to shorten a URL
to one instance, and be able to resolve that shortened URL by sending subsequent requests to the second instance. 

## Implementation

#### URL Encoding
To encode the URLs I have used the SHA-256 hashing function to encode the url. 
The hash is then split into N bytes (set to 7) which is then encoded in URl-safe base64 to reduce the size of the string.

If a collision is not detected in storage (hashtable) then the URL is stored. 
If a hash is detected then the next slice of N bytes in the SHA-256 hash is used for the base64 encoding.

#### Storage
To store the hashes I have opted to use a simple hash table for both *url to short url* and *short url to url*. 
This reduces redundancy in the hashtable when a url is uploaded multiple times saving 128/N amounts of space in the hash table.

This also allows for quick look ups both ways to reduce generation time.

Given the short timeframe for turnaround on this project, I opted for a simple approach which could be easily iterated upon later.
The storage solution could be further expanded using chaining in the hashtable or open assignment in a similar hash oriented data structure.

#### API
The API works as instructed, the only changes I made were adding error response codes and messages to potential edge cases:
 - Unable to safely store the short url (POST)
 - Short url does not exist (GET)

Further checks could also be done to verify that the url given actually exists, only safe content is being sent with the body of the POST request,
and that the urls being sent are safe.

I also changed the GET request to take the url code instead of the full url. This could be changed later but I felt it made the code more readable
and made it easier for the end users and developers to interact with.

## Getting Started

To begin the project, clone this repository to your local machine:

```commandline
git clone https://github.com/pocketzworld/url-shortener-tech-test.git
```

```commandline
# Install requirements via python environments
source url-shortener/bin/activate
pip3 install -r requirements.txt
```

This repository contains a skeleton of the URL Shortener web service written in Python 3.11
using the [FastAPI](https://fastapi.tiangolo.com/) framework.

The API endpoints can be found in `server.py`.

A Makefile and Dockerfile are also included for your convenience to run and test the web service.

Note that you are not required to use Docker or the provided FastAPI skeleton for your implementation, if you are 
more comfortable with other tools or frameworks. Your solution must still meet the requirements described in the 
Project Description. The following sections will assume that you are using Docker and FastAPI, but feel free to 
update the project and make sure to modify the README to reflect how your implementation should be run and tested. 

### Running the service

To run the web service in interactive mode, use the following command:
```commandline
make run
```

This command will build a new Docker image (`pw/url-shortener:latest`) and start a container
instance in interactive mode.

By default, the web service will run on port 8000.

### Testing

Swagger UI is available as part of the FastAPI framework that can be used to inspect and test
the API endpoints of the URL shortener. To access it, start run the web service and go to http://localhost:8000/docs

To test the generation of short urls and to verify that they have been stored correctly I have added the test.py file.

This tests *10,000 unique* urls to test the bounds of hashing collisions, speed of url encoding, and speed/accuracy of url retrieval.
```commandline
make test
# or
python3 test.py
```

## Submission Guidelines
When you have completed the project, please follow these guidelines for submission:

1. Commit and push your code to your GitHub repository.
2. Update this README with any additional instructions, notes, or explanations regarding your implementation, if necessary.
3. Provide clear instructions on how to run and test your project.
4. Share the repository URL with the hiring team or interviewer.

## Additional Information
Feel free to be creative in how you approach this project. Your solution will be evaluated based on code quality,
efficiency, and how well it meets the specified requirements. Be prepared to discuss the reasoning behind your
implementation decisions and their trade-offs.

Remember that this project is the basis for the technical interviews, which do include live coding. We will not
ask you to solve an algorithm, but you will be expected to demo your solution and explain your thought process.

Good luck, and we look forward to seeing your URL Shortener project! If you have any questions or need
clarifications, please reach out to us.
