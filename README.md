# sendclocreport
## *Send repository cloc report to a specified email*

* * *

Sendclocreport will clone a repository, check out a specified branch, scan the specified source repository with CLOC and send the output of CLOC to an email address specified.

Works with Github, Bitbucket, GitLab

### Requirements
- Python 3.7.2
    - Must be on the system "path"
- Gmail account to send the report

### Usage
- Works with both bash and Windows command prompt

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

### Output
An email will be sent to the destination email with the subject "cloc report for branch <branch name> of repository <repository name>"
- The email will contain no message
- The output of the script is emailed as an attachment to the specified destination email as a .CSV file
    - <timestamp in yyyymmddHHMMSS format>Repository Name-branch name.csv
    - **Example:** 20190205090440cloc-master.csv

#### CSV Column Headers
- **files** - Numbers of files per language 
- **language** - Programming language of the files
- **blank** - How many lines are blank in the files per language
- **comment** - How many lines are comments in the files per language
- **code** - How many lines are comments in the files per language
- github.com/AlDanial/cloc v 1.80 <processing time and processing speed>
	- Example: github.com/AlDanial/cloc v 1.80  T=1.00 s (380.0 files/s, 49176.0 lines/s)
