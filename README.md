# autoscaler
autoscaler app for docker swarm

# Deployment
docker run -dit \\
   --name web.scaler \\
   -p 733:733 \\
   -v ~/autoscaler/docker/conf:/conf \\
   -v /var/run/docker.sock:/var/run/docker.sock \\
   --restart=always \\
   --log-driver json-file \\
   --log-opt max-size=10m \\
   stevenli2019/autoscaler:1.0
