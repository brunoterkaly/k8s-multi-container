kubectl create -f Deploy/web-pod-1.yml
kubectl create -f Deploy/web-svc.yml
kubectl create -f Deploy/db-pod.yml
kubectl create -f Deploy/db-svc.yml
kubectl edit svc/web
