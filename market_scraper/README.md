 # Create docker image

 $ aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 034827030859.dkr.ecr.eu-central-1.amazonaws.com
 $ docker build -t market .
 $ docker tag market:latest 034827030859.dkr.ecr.eu-central-1.amazonaws.com/market:latest
 $ docker push 034827030859.dkr.ecr.eu-central-1.amazonaws.com/market:latest

