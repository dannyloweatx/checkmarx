# sendclocreport.py
### Requirements
- Python 3.7.2
    - Must be on the system "path"
### Usage
*Works with both bash and Windows command prompt*

**Without YAML (Prompted for values)**
```sh
C:\dev\checkmarx>python sendclocreport.py
Type your email and press enter: <sender email address>
Sender email password: <sender email password>
Type the destination email and press enter: <destination email address>
Type the URL for the repository: <repository url>
Type location where you want the reposiroty to go: <file location>
Type the branch name you want to process: <branch name>
```

**With YAML**
```sh
C:\dev\checkmarx>python sendclocreport.py samplefile.yml
```