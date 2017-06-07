kubectl delete pod web1
kubectl delete pod mysql
kubectl delete svc mysql
kubectl delete svc web

kubectl create -f web-pod-1.yml
kubectl create -f db-pod.yml
kubectl create -f db-svc.yml
kubectl create -f web-svc.yml

# Expose public IP address
# This can take a few minutes (take some questions now)
kubectl edit svc/web
