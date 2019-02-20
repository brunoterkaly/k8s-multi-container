kubectl delete -f web-pod-1.yml
kubectl delete -f web-svc-1.yml
kubectl delete -f  db-pod-1.yml
kubectl create -f web-pod-1.yml
kubectl create -f web-svc-1.yml
kubectl create -f  db-pod-1.yml
