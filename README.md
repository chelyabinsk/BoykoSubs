# Boyko Subscribers

## Installation
`docker build --tag boykosubs .`

## Usage
`cd code`

`docker run --user 1000:1000 -v .:/app/code --rm boykosubs sh -c "python3 code/download_comments.py"`
