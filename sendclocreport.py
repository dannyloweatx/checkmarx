import smtplib, ssl, getpass, subprocess, pip, sys, os, shutil, re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pip._internal import main
from datetime import datetime

# Send email with attached output
def sendEmail():
	subject = 'cloc report for branch %s of repository %s' % (branch, getRepoName())
	
	message = MIMEMultipart()
	message['Subject'] = subject
	message['From'] = senderEmail
	message['To'] = receiverEmail
	
	part = MIMEBase('application', "octet-stream")
	part.set_payload(open(outputFile, "rb").read())
	encoders.encode_base64(part)
	
	part.add_header('Content-Disposition', 'attachment; filename="'+ outputFile +'"')
	message.attach(part)
	
	context = ssl.create_default_context()
	print ('Emailing cloc report to  ' + receiverEmail + '...')
	with smtplib.SMTP(smtpServer, port) as server:
		server.starttls(context=context)
		server.login(senderEmail, password)
		server.sendmail(senderEmail, receiverEmail, message.as_string())

# Utility method to install packages if needed
def install(package):
	main(['install', package])

# Process the repository and build the cloc report
def processRepo():
	repo = getRepoName()
	print ('Begin processing repository ' + repo + '...')
	if not os.path.exists(curDirectory+repo):
		print ('Cloning repository ' + repo + '...')
		git.Git(curDirectory).clone(repoUrl)

	gitrepo = git.Repo(repo)
	gcmd = git.cmd.Git(repo)
	gcmd.pull()
	print ('Checking out branch ' + branch + " for repository " + repo + '...')
	gitrepo.git.checkout("-f", branch)
		
	print ('Obtaining cloc report for repository ' + repo + '...')
	proc = subprocess.Popen([binDirectory+clocExecutable,curDirectory+repo, "--csv","--out", outputFile , "--quiet"], stdout=subprocess.PIPE)
	proc.stdout.read()

# Get repository name from URL
def getRepoName():
	return(repoUrl[repoUrl.rfind('/')+1:repoUrl.rfind('.')])

# Input validation method
def validateInput():
	errorMessage = ""
	if not re.match(r"[^@]+@[^@]+\.[^@]+", senderEmail):
		errorMessage = "Sender email format is invalid"
	
	if not re.match(r"[^@]+@[^@]+\.[^@]+", receiverEmail):
		errorMessage = errorMessage+"\n" if len(errorMessage)>0 else ""
		errorMessage = errorMessage+"Destination email format is invalid"
		
	if not re.match(r"((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(\/)?", repoUrl):	
		errorMessage = errorMessage+"\n" if len(errorMessage)>0 else ""
		errorMessage = errorMessage+"Git repository is invalid. Must be a valid URL that ends with .git"
		
	if (len(errorMessage)>0):
		sys.exit(errorMessage)

#Global variables
port = 587
smtpServer = "smtp.gmail.com"
logtime = datetime.now().strftime("%Y%m%d%H%M%S")
senderEmail = ""
password = ""
receiverEmail = ""
repoUrl = ""
branch = ""
curDirectory = "./"
binDirectory = "./bin/"
clocExecutable = "cloc-1.80.exe"
defaultBranch = "master"

# Install git
try:
	import git
except ImportError:
	print('git is not installed, installing it now!')
	install('git')

# Install PyYAML
try:
	import yaml
except ImportError:
	print('PyYAML is not installed, installing it now!')
	install('PyYAML')

# Retrieve input
if len(sys.argv) > 1:
	fileName = sys.argv[1]
	with open(fileName) as yamlFile:
		yamlArgs = yaml.safe_load(yamlFile)
		senderEmail = yamlArgs['senderEmail']
		password = yamlArgs['password']
		receiverEmail = yamlArgs['receiverEmail']
		repoUrl = yamlArgs['repoUrl']
		branch = yamlArgs['branch']
else:
	senderEmail = input("Type your email and press enter: ")
	password = getpass.getpass(prompt='Sender email password: ', stream=None)
	receiverEmail = input("Type the destination email and press enter: ")
	repoUrl = input("Type the URL for the repository: ")
	branch = input("Type the branch name you want to process: ")

if (len(branch)==0):
	branch = defaultBranch
	
# Begin processing
validateInput()	
outputFile = logtime+getRepoName()+"-"+branch+".csv"
startTime = datetime.now()	
processRepo()
sendEmail()
endTime = datetime.now()	
totalTime = endTime - startTime
print ('Process for branch ' + branch + ' of repository ' + getRepoName() + ' completed successfully (' + str(totalTime.total_seconds()) + ' seconds)')
# End processing
	
