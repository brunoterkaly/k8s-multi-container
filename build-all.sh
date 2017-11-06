kubectl create -f Deploy/web-pod-1.yml
kubectl create -f Deploy/web-svc.yml
kubectl create -f Deploy/db-pod.yml
kubectl create -f Deploy/db-svc.yml
kubectl edit svc/web
python3 Run/s-and-r.py
bash Run/init.sh
bash Run/add.sh
bash Run/query.sh
