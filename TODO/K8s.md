As you generate load:
kubectl top pods -l app=llm-app should show increasing CPU usage for your pod(s).
kubectl describe hpa llm-app-hpa or kubectl get hpa llm-app-hpa -w should eventually show:
The current CPU utilization increasing.
If it exceeds 70% (your target), the DESIRED replica count should increase.
kubectl get pods -l app=llm-app will then show new Pods being created (ContainerCreating, then Running).