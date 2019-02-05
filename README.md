# sendclocreport
## *Send repository cloc report to a specified email*

* * *

Sendclocreport will clone a repository, check out a specified branch, scan the specified source repository with CLOC and send the output of CLOC to an email address specified.

### Requirements
- Python 3.7.2
    - Must be on the system "path"
- Gmail account to send the report

### Usage
- Works with both bash and Windows command prompt
- Run sendclocreport.py from the directory  containing the "bin" directory

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

### YAML file format
*Save as *filename.yml*
<pre>
    senderEmail: senderemail@gmail.com
    password: <sender email password>
    receiverEmail: destinationemail@gmail.com
    repoUrl: https://github.com/username/repositoryname.git
    branch: branch-name
</pre>