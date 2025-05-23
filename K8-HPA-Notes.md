# Describe the HPA to see its status, targets, and current/desired replicas
kubectl describe hpa llm-app-hpa

# Get HPA status (will show current metrics and replica counts)
kubectl get hpa llm-app-hpa -w # -w for watch

# Check your pods
kubectl get pods -l app=llm-app # Filter by label

# Check CPU usage of pods (if metrics-server is working)
kubectl top pods -l app=llm-app

### k8-hpa.yaml
apiVersion: autoscaling/v2: Use v2 for Utilization targets and more advanced features. autoscaling/v1 only supports targetAverageUtilization as a percentage of requested CPU.
scaleTargetRef: Points to your llm-app-deployment.
minReplicas: 1: HPA will not scale below this number.
maxReplicas: 5: HPA will not scale above this number.
metrics:: Defines what the HPA should monitor.
type: Resource
resource.name: cpu
resource.target.type: Utilization
resource.target.averageUtilization: 70: This is the target. If the average CPU utilization across all Pods of the llm-app-deployment goes above 70% (of their requested CPU), the HPA will trigger a scale-up. If it drops significantly below 70%, it will trigger a scale-down.
behavior (Optional): Allows fine-tuning of scaling speed and stabilization. For starting simple, you can omit this.

### k8-deploy.yaml
replicas: 1: It's good to start with a low number; the HPA will take over.
resources::
requests.cpu: "1": This tells K8s that your application needs at least 1 CPU core to function properly.
  The HPA will calculate CPU utilization based on this request value. This is mandatory for CPU utilization-based HPA.
requests.memory: "4Gi": Important for scheduling.
limits.cpu: "2": Your Pod won't be allowed to use more than 2 CPU cores.
limits.memory: "8Gi": Your Pod won't use more than 8 GiB of RAM. If it tries, it might be OOMKilled.
limits."nvidia.com/gpu": 1: If you are using GPUs, you must request them here. 
  HPA can also scale on GPU utilization if your metrics system and device plugin support it (more advanced). For now, we're focusing on CPU.
Probes: Increased initialDelaySeconds for probes to give ample time for your potentially large LLM to load before K8s starts checking health/readiness. Adjust these based on your actual model load time.