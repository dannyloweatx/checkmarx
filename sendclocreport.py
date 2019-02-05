import smtplib, ssl, getpass, subprocess, pip, sys, os, shutil, re
from email.mime.text import MIMEText
from pip._internal import main

def sendEmail():
	port = 587
	smtpServer = "smtp.gmail.com"

	message = MIMEText(messageBody)
	message['Subject'] = subject
	message['From'] = senderEmail
	message['To'] = receiverEmail
	context = ssl.create_default_context()
	print ('Emailing cloc report to  ' + receiverEmail + '...')
	with smtplib.SMTP(smtpServer, port) as server:
		server.starttls(context=context)
		server.login(senderEmail, password)
		server.sendmail(senderEmail, receiverEmail, message.as_string())
		
def install(package):
	main(['install', package])
	
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
	proc = subprocess.Popen([binDirectory+clocExecutable,curDirectory+repo, "--quiet"], stdout=subprocess.PIPE)
	output = proc.stdout.read()
	return(output.decode("utf-8"))
	
def getRepoName():
	return(repoUrl[repoUrl.rfind('/')+1:repoUrl.rfind('.')])
	
def validateInput():
	errorMessage = ""
	if not re.match(r"[^@]+@[^@]+\.[^@]+", senderEmail):
		errorMessage = "\n" if len(errorMessage)>0 else ""
		errorMessage = "Sender email format is invalid"
	
	if not re.match(r"[^@]+@[^@]+\.[^@]+", receiverEmail):
		errorMessage = "\n" if len(errorMessage)>0 else ""
		errorMessage = "Destination email format is invalid"
		
	if not re.match(r"((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(\/)?", repoUrl):	
		errorMessage = "\n" if len(errorMessage)>0 else ""
		errorMessage = "Git repository is invalid. Must end with .git"
		
	if (len(errorMessage)>0):
		sys.exit(errorMessage)

senderEmail = ""
password = ""
receiverEmail = ""
repoUrl = ""
branch = ""
curDirectory = "./"
binDirectory = "./bin/"
clocExecutable = "cloc-1.80.exe"
defaultBranch = "master"

try:
	import git
except ImportError:
	print('git is not installed, installing it now!')
	install('git')

try:
	import yaml
except ImportError:
	print('PyYAML is not installed, installing it now!')
	install('PyYAML')

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

validateInput()	
	
output = processRepo()
subject = 'cloc report for branch %s of repository %s' % (branch, getRepoName())
messageBody = output
sendEmail()

print ('Process completed successfully')
	
