# flaskTinyURL

A flask API that uses pynamoDB to store long urls mapped to short IDs to be accessed via /t/
Uses JWT as authentication, mostly for experimentation, currently passed in as URL parameter but needs to be included in the request body

Requires:
AWS Secrets Manager to host
PynamoDB
Flask


