# sendclocreport
## *Send repository cloc report to a specified email address as an attachment*

* * *

Sendclocreport will clone a repository, check out a specified branch, scan the specified source repository with CLOC and send the output of CLOC to an email address specified.

Works with Github, Bitbucket, GitLab

### Requirements
- Python 3.7.2
    - Python executable must be on the system "path" in order to work as shown
- Gmail account to send the report

### Usage
- Works with both bash and Windows command prompt
- Syntax is the same with both bash and windows
- Must run the script from the *checkmarx* directory

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

#### YAML file format
<pre>
senderEmail: senderemail@gmail.com
password: &lt;sender email password&gt;
receiverEmail: destinationemail@gmail.com
repoUrl: https://github.com/username/repositoryname.git
branch: branch-name
</pre>

### Output
#### Console output
<pre>
Begin processing repository &lt;repository name&gt;...
Checking out branch &lt;branch name%gt; for repository &lt;repository name&gt;...
Obtaining cloc report for repository &lt;repository name&gt;...
Emailing cloc report to  dannyloweatx@gmail.com...
Process for branch &lt;branch name&gt; of repository &lt;repository name&gt; completed successfully (&lt;processing time&gt;)
</pre>
#### File output
An email will be sent to the destination email with the subject "cloc report for branch &lt;branch name&gt; of repository &lt;repository name&gt;"
- The email will contain no message
- The output of the script is emailed as an attachment to the specified destination email as a .CSV file
    - &lt;timestamp in yyyymmddHHMMSS format&gt;&lt;Repository Name&gt;-&lt;branch name&gt;.csv
    - **Example:** 20190205090440cloc-master.csv

#### CSV Column Headers
- **files** - Numbers of files per language 
- **language** - Programming language of the files
- **blank** - How many lines are blank in the files per language
- **comment** - How many lines are comments in the files per language
- **code** - How many lines are comments in the files per language
- **github.com/AlDanial/cloc v 1.80 &lt;processing time and processing speed&gt;**
	- Example: github.com/AlDanial/cloc v 1.80  T=1.00 s (380.0 files/s, 49176.0 lines/s)
