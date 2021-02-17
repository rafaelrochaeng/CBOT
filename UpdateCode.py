from subprocess import call

call(["git", "pull"])
exec(open("main.py").read())


