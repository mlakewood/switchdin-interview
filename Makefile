# this doesnt work, but its handy to know this.
ecr-login:
	aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 220445851985.dkr.ecr.ap-southeast-2.amazonaws.com