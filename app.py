from flask import Flask, render_template, request

app = Flask(__name__)


# =========================================================
# DEVOPS TROUBLESHOOTING ENGINE
# =========================================================

def troubleshoot(question):

    q = question.lower().strip()

    # -----------------------------------------------------
    # Normalize common phrases
    # -----------------------------------------------------

    replacements = {
        "not working": "error",
        "doesn't work": "error",
        "doesnt work": "error",
        "is down": "stopped",
        "died": "stopped",
        "crashed": "stopped",
        "cannot connect": "connection",
        "can't connect": "connection",
        "cant connect": "connection",
        "unable to connect": "connection",
        "no connection": "connection",
        "not connecting": "connection",
    }

    for old, new in replacements.items():
        q = q.replace(old, new)

    # =====================================================
    # KUBERNETES
    # =====================================================

    if any(x in q for x in [
        "kubernetes", "k8s", "kubectl",
        "pod", "deployment", "service kubernetes"
    ]):

        # CrashLoopBackOff
        if "crashloopbackoff" in q:

            return """
            <h3>☸️ Kubernetes - CrashLoopBackOff</h3>

            <p><b>🔍 Diagnosis</b></p>

            <p>
            The container starts but keeps crashing.
            Kubernetes repeatedly restarts the container.
            </p>

            <b>🛠 Commands</b>

            <pre>
kubectl get pods
kubectl describe pod &lt;pod_name&gt;
kubectl logs &lt;pod_name&gt;
kubectl logs &lt;pod_name&gt; --previous
kubectl get events
            </pre>

            <b>🔎 Common Causes</b>

            <ul>
                <li>Application is crashing.</li>
                <li>Wrong environment variables.</li>
                <li>Missing ConfigMap or Secret.</li>
                <li>Incorrect command or entrypoint.</li>
                <li>Application dependency unavailable.</li>
                <li>CPU or memory problem.</li>
                <li>Incorrect configuration.</li>
            </ul>

            <b>✅ Troubleshooting</b>

            <ol>
                <li>Check current container logs.</li>
                <li>Check previous container logs.</li>
                <li>Check Pod Events.</li>
                <li>Check environment variables.</li>
                <li>Check Secrets and ConfigMaps.</li>
                <li>Check CPU and memory limits.</li>
                <li>Check command and image configuration.</li>
            </ol>

            <b>💡 Important</b>

            <p>
            Do not repeatedly restart the Pod without checking the
            actual application error first.
            </p>
            """

        # ImagePullBackOff
        if any(x in q for x in [
            "imagepullbackoff",
            "image pull",
            "imagepull",
            "image not found"
        ]):

            return """
            <h3>☸️ Kubernetes - ImagePullBackOff</h3>

            <p><b>🔍 Diagnosis</b></p>

            <p>
            Kubernetes cannot download the container image.
            </p>

            <b>🛠 Commands</b>

            <pre>
kubectl get pods
kubectl describe pod &lt;pod_name&gt;
kubectl get events
            </pre>

            <b>🔎 Check</b>

            <ul>
                <li>Image name.</li>
                <li>Image tag.</li>
                <li>Docker registry.</li>
                <li>Registry authentication.</li>
                <li>ImagePullSecrets.</li>
                <li>Network connectivity.</li>
            </ul>

            <b>Example</b>

            <pre>
image: nginx:latest
            </pre>
            """

        # Pending
        if "pending" in q:

            return """
            <h3>☸️ Kubernetes - Pod Pending</h3>

            <p><b>🔍 Diagnosis</b></p>

            <p>
            Kubernetes has not successfully scheduled or started the Pod.
            </p>

            <b>🛠 Commands</b>

            <pre>
kubectl get pods
kubectl describe pod &lt;pod_name&gt;
kubectl get nodes
kubectl get events
            </pre>

            <b>Common Causes</b>

            <ul>
                <li>Insufficient CPU.</li>
                <li>Insufficient memory.</li>
                <li>Node unavailable.</li>
                <li>Node selector mismatch.</li>
                <li>Taints and tolerations.</li>
                <li>Persistent volume problem.</li>
            </ul>
            """

        # Pod general
        if "pod" in q:

            return """
            <h3>☸️ Kubernetes - Pod Troubleshooting</h3>

            <b>🛠 Commands</b>

            <pre>
kubectl get pods
kubectl describe pod &lt;pod_name&gt;
kubectl logs &lt;pod_name&gt;
kubectl get events
            </pre>

            <b>Check</b>

            <ul>
                <li>Pod status.</li>
                <li>Container logs.</li>
                <li>Pod events.</li>
                <li>Image availability.</li>
                <li>Environment variables.</li>
                <li>CPU/memory resources.</li>
            </ul>
            """

        # Deployment
        if "deployment" in q:

            return """
            <h3>☸️ Kubernetes - Deployment Problem</h3>

            <pre>
kubectl get deployment
kubectl describe deployment &lt;name&gt;
kubectl get pods
kubectl rollout status deployment/&lt;name&gt;
kubectl rollout history deployment/&lt;name&gt;
            </pre>

            <b>Check</b>

            <ul>
                <li>Replica count.</li>
                <li>Container image.</li>
                <li>Pod status.</li>
                <li>Deployment events.</li>
                <li>Rollout status.</li>
            </ul>
            """

        # Service
        if "service" in q:

            return """
            <h3>☸️ Kubernetes - Service Problem</h3>

            <pre>
kubectl get svc
kubectl describe svc &lt;service_name&gt;
kubectl get endpoints
kubectl get pods --show-labels
            </pre>

            <b>Check</b>

            <ul>
                <li>Service selector.</li>
                <li>Pod labels.</li>
                <li>Target port.</li>
                <li>Endpoints.</li>
                <li>Network policy.</li>
            </ul>
            """

        # Kubernetes logs
        if "log" in q:

            return """
            <h3>☸️ Kubernetes - Logs</h3>

            <pre>
kubectl logs &lt;pod_name&gt;
kubectl logs &lt;pod_name&gt; --previous
kubectl logs -f &lt;pod_name&gt;
            </pre>

            Use logs to identify application startup and runtime errors.
            """

    # =====================================================
    # DOCKER
    # =====================================================

    if any(x in q for x in [
        "docker", "container"
    ]):

        # Container stopped/crashed
        if any(x in q for x in [
            "stopped",
            "container stopped",
            "container down",
            "container crash",
            "container error"
        ]):

            return """
            <h3>🐳 Docker - Container Stopped / Crashed</h3>

            <b>🔍 Diagnosis</b>

            <p>
            The container has stopped or the application inside it has crashed.
            </p>

            <b>🛠 Commands</b>

            <pre>
docker ps
docker ps -a
docker logs &lt;container_name&gt;
docker inspect &lt;container_name&gt;
            </pre>

            <b>Check</b>

            <ul>
                <li>Container status.</li>
                <li>Application logs.</li>
                <li>Exit code.</li>
                <li>Environment variables.</li>
                <li>Volumes.</li>
                <li>Network.</li>
            </ul>
            """

        # Build
        if any(x in q for x in [
            "build",
            "dockerfile",
            "build error",
            "docker build"
        ]):

            return """
            <h3>🐳 Docker - Build Error</h3>

            <pre>
docker build -t myapp .
docker images
docker history myapp
            </pre>

            <b>Check</b>

            <ol>
                <li>Dockerfile syntax.</li>
                <li>Base image.</li>
                <li>COPY paths.</li>
                <li>Dependencies.</li>
                <li>Build context.</li>
            </ol>
            """

        # Port
        if any(x in q for x in [
            "port",
            "localhost",
            "connection refused",
            "port conflict"
        ]):

            return """
            <h3>🐳 Docker - Port Problem</h3>

            <pre>
docker ps
docker port &lt;container_name&gt;
docker logs &lt;container_name&gt;
            </pre>

            <b>Check</b>

            <ul>
                <li>Host port.</li>
                <li>Container port.</li>
                <li>Application listening port.</li>
                <li>Another application using the port.</li>
            </ul>
            """

        # Network
        if "network" in q:

            return """
            <h3>🐳 Docker - Network Problem</h3>

            <pre>
docker network ls
docker network inspect &lt;network_name&gt;
docker inspect &lt;container_name&gt;
            </pre>

            Check whether the required containers are connected
            to the same Docker network.
            """

        # Volume
        if any(x in q for x in [
            "volume",
            "mount",
            "persistent data",
            "data missing"
        ]):

            return """
            <h3>🐳 Docker - Volume Problem</h3>

            <pre>
docker volume ls
docker volume inspect &lt;volume_name&gt;
docker inspect &lt;container_name&gt;
            </pre>

            Check volume name, mount path and permissions.
            """

        # Image
        if any(x in q for x in [
            "image",
            "docker pull",
            "image not found"
        ]):

            return """
            <h3>🐳 Docker - Image Problem</h3>

            <pre>
docker images
docker pull &lt;image&gt;
docker inspect &lt;image&gt;
            </pre>

            Check image name, tag, registry access and authentication.
            """

        # Compose
        if any(x in q for x in [
            "compose",
            "docker-compose"
        ]):

            return """
            <h3>🐳 Docker Compose Problem</h3>

            <pre>
docker compose config
docker compose ps
docker compose logs
docker compose up -d
            </pre>

            Check YAML syntax, services, networks, volumes and environment variables.
            """

        # Docker permission
        if "permission" in q:

            return """
            <h3>🐳 Docker - Permission Problem</h3>

            <pre>
docker ps
ls -l /var/run/docker.sock
groups
            </pre>

            Check Docker service and user permissions.
            """

    # =====================================================
    # LINUX
    # =====================================================

    if any(x in q for x in [
        "linux", "ubuntu", "redhat", "rhel",
        "centos", "server"
    ]):

        # Disk
        if any(x in q for x in [
            "disk", "space", "filesystem",
            "no space"
        ]):

            return """
            <h3>🐧 Linux - Disk Space Problem</h3>

            <pre>
df -h
df -i
du -sh *
sudo du -sh /var/*
            </pre>

            <b>Check</b>

            <ol>
                <li>Filesystem usage.</li>
                <li>Large directories.</li>
                <li>Large log files.</li>
                <li>Inode usage.</li>
            </ol>

            Remove unnecessary files carefully.
            """

        # Memory
        if any(x in q for x in [
            "memory", "ram", "oom"
        ]):

            return """
            <h3>🐧 Linux - High Memory Usage</h3>

            <pre>
free -h
top
ps aux --sort=-%mem | head
            </pre>

            Identify the process consuming high memory and investigate it.
            """

        # CPU
        if "cpu" in q:

            return """
            <h3>🐧 Linux - High CPU Usage</h3>

            <pre>
top
ps aux --sort=-%cpu | head
            </pre>

            Identify the process causing high CPU usage and check its logs.
            """

        # Permission
        if any(x in q for x in [
            "permission",
            "permission denied",
            "ownership",
            "chmod",
            "chown"
        ]):

            return """
            <h3>🐧 Linux - Permission Problem</h3>

            <pre>
ls -l filename
whoami
id
ls -ld directory
            </pre>

            Check ownership and read/write/execute permissions.
            """

        # SSH
        if "ssh" in q:

            return """
            <h3>🐧 Linux - SSH Troubleshooting</h3>

            <pre>
systemctl status ssh
ss -tlnp | grep 22
ping &lt;server-ip&gt;
            </pre>

            <b>Check</b>

            <ol>
                <li>Server reachability.</li>
                <li>SSH service.</li>
                <li>Port 22.</li>
                <li>Firewall.</li>
                <li>Username.</li>
                <li>SSH key permissions.</li>
            </ol>
            """

        # Service
        if any(x in q for x in [
            "service",
            "systemctl"
        ]):

            return """
            <h3>🐧 Linux - Service Problem</h3>

            <pre>
systemctl status &lt;service&gt;
systemctl restart &lt;service&gt;
journalctl -u &lt;service&gt;
            </pre>

            Check service status and logs.
            """

    # =====================================================
    # GIT / GITHUB
    # =====================================================

    if any(x in q for x in [
        "git", "github", "gitlab", "bitbucket"
    ]):

        # Merge conflict
        if any(x in q for x in [
            "merge", "conflict"
        ]):

            return """
            <h3>🔧 Git - Merge Conflict</h3>

            <pre>
git status
git diff
git pull
            </pre>

            <b>Steps</b>

            <ol>
                <li>Open conflicted files.</li>
                <li>Resolve conflict markers.</li>
                <li>Save files.</li>
                <li>Stage changes.</li>
                <li>Commit.</li>
                <li>Push.</li>
            </ol>

            <pre>
git add .
git commit -m "Resolve merge conflict"
git push
            </pre>
            """

        # Push
        if "push" in q:

            return """
            <h3>🔧 Git - Push Problem</h3>

            <pre>
git status
git remote -v
git branch
git pull
git push
            </pre>

            Check branch, remote URL and authentication.
            """

        # Pull
        if "pull" in q:

            return """
            <h3>🔧 Git - Pull Problem</h3>

            <pre>
git status
git remote -v
git fetch
git pull
            </pre>

            Check remote changes and merge conflicts.
            """

        # Branch
        if "branch" in q:

            return """
            <h3>🔧 Git - Branch Problem</h3>

            <pre>
git branch
git branch -a
git switch -c feature-name
git status
            </pre>

            Make sure you are working on the correct branch.
            """

        # Clone
        if "clone" in q:

            return """
            <h3>🔧 Git - Clone Problem</h3>

            <pre>
git clone &lt;repository-url&gt;
git remote -v
            </pre>

            Check repository URL, network and authentication.
            """

        # Authentication
        if any(x in q for x in [
            "authentication",
            "token",
            "login"
        ]):

            return """
            <h3>🔧 Git/GitHub - Authentication Problem</h3>

            <ol>
                <li>Check repository URL.</li>
                <li>Check GitHub authentication.</li>
                <li>Check Personal Access Token if required.</li>
                <li>Check repository permissions.</li>
            </ol>
            """

    # =====================================================
    # JENKINS / CI-CD
    # =====================================================

    if any(x in q for x in [
        "jenkins",
        "pipeline",
        "ci/cd",
        "cicd",
        "continuous integration",
        "continuous deployment"
    ]):

        # Build
        if any(x in q for x in [
            "build",
            "failed",
            "failure",
            "error"
        ]):

            return """
            <h3>🔨 Jenkins - Build Failed</h3>

            <b>🔍 Diagnosis</b>

            <ol>
                <li>Open Jenkins Console Output.</li>
                <li>Find the first meaningful error.</li>
                <li>Check source code.</li>
                <li>Check dependencies.</li>
                <li>Check environment variables.</li>
                <li>Check credentials.</li>
                <li>Check Docker/build tools.</li>
            </ol>

            <b>💡 Tip</b>

            Always investigate the first real error,
            not only the final FAILED line.
            """

        # Agent
        if any(x in q for x in [
            "agent",
            "offline",
            "node offline"
        ]):

            return """
            <h3>🔨 Jenkins - Agent Offline</h3>

            <ol>
                <li>Check agent status.</li>
                <li>Check network connectivity.</li>
                <li>Check Java/runtime.</li>
                <li>Check disk space.</li>
                <li>Check agent logs.</li>
            </ol>
            """

        # Webhook
        if any(x in q for x in [
            "webhook",
            "trigger"
        ]):

            return """
            <h3>🔨 Jenkins - Webhook Problem</h3>

            <ol>
                <li>Check GitHub webhook.</li>
                <li>Check Jenkins URL.</li>
                <li>Check webhook delivery.</li>
                <li>Check firewall/network.</li>
                <li>Check job trigger configuration.</li>
            </ol>
            """

        # Jenkinsfile
        if any(x in q for x in [
            "jenkinsfile",
            "pipeline syntax",
            "stage error"
        ]):

            return """
            <h3>🔨 Jenkins - Jenkinsfile Problem</h3>

            <pre>
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }
    }
}
            </pre>

            Check syntax, stages, agents, credentials and environment variables.
            """

        # Credentials
        if any(x in q for x in [
            "credential",
            "credentials",
            "secret"
        ]):

            return """
            <h3>🔨 Jenkins - Credentials Problem</h3>

            <ol>
                <li>Check Jenkins Credentials Manager.</li>
                <li>Check credential ID.</li>
                <li>Check permissions.</li>
                <li>Check whether the secret has expired.</li>
            </ol>
            """

    # =====================================================
    # AWS
    # =====================================================

    if any(x in q for x in [
        "aws",
        "amazon web services",
        "ec2",
        "s3",
        "iam",
        "vpc"
    ]):

        # EC2
        if "ec2" in q:

            if any(x in q for x in [
                "ssh",
                "connection",
                "timeout",
                "unreachable"
            ]):

                return """
                <h3>☁️ AWS EC2 - SSH / Connection Problem</h3>

                <ol>
                    <li>Check EC2 instance state.</li>
                    <li>Check public/private IP.</li>
                    <li>Check Security Group port 22.</li>
                    <li>Check Network ACL.</li>
                    <li>Check Route Table.</li>
                    <li>Check Internet Gateway where applicable.</li>
                    <li>Check username and SSH key.</li>
                </ol>

                <pre>
ssh -i key.pem user@&lt;public-ip&gt;
                </pre>
                """

            return """
            <h3>☁️ AWS EC2 Troubleshooting</h3>

            <ol>
                <li>Check instance state.</li>
                <li>Check status checks.</li>
                <li>Check CPU.</li>
                <li>Check Security Group.</li>
                <li>Check Network ACL.</li>
                <li>Check Route Table.</li>
                <li>Check storage.</li>
                <li>Check application/service.</li>
            </ol>
            """

        # S3
        if "s3" in q:

            return """
            <h3>☁️ AWS S3 Troubleshooting</h3>

            <ol>
                <li>Check bucket name.</li>
                <li>Check AWS region.</li>
                <li>Check IAM permissions.</li>
                <li>Check bucket policy.</li>
                <li>Check object permissions.</li>
                <li>Check Block Public Access.</li>
                <li>Check KMS permissions if encryption is used.</li>
            </ol>
            """

        # IAM
        if any(x in q for x in [
            "iam",
            "access denied",
            "not authorized",
            "permission"
        ]):

            return """
            <h3>☁️ AWS IAM - Permission Problem</h3>

            <ol>
                <li>Identify IAM user or role.</li>
                <li>Check attached policies.</li>
                <li>Check resource-based policies.</li>
                <li>Look for explicit Deny.</li>
                <li>Check permissions boundaries where applicable.</li>
            </ol>
            """

        # VPC
        if "vpc" in q:

            return """
            <h3>☁️ AWS VPC Troubleshooting</h3>

            <b>Check:</b>

            <ul>
                <li>VPC CIDR.</li>
                <li>Subnet.</li>
                <li>Route Table.</li>
                <li>Internet Gateway.</li>
                <li>NAT Gateway.</li>
                <li>Security Group.</li>
                <li>Network ACL.</li>
            </ul>
            """

        return """
        <h3>☁️ AWS Troubleshooting</h3>

        <p>Supported AWS areas:</p>

        <ul>
            <li>EC2</li>
            <li>S3</li>
            <li>IAM</li>
            <li>VPC</li>
        </ul>
        """

    # =====================================================
    # NETWORKING
    # =====================================================

    if any(x in q for x in [
        "network",
        "dns",
        "ip address",
        "connectivity",
        "firewall",
        "routing",
        "port"
    ]):

        # DNS
        if any(x in q for x in [
            "dns",
            "domain",
            "name resolution"
        ]):

            return """
            <h3>🌐 Network - DNS Problem</h3>

            <pre>
nslookup example.com
ipconfig /flushdns
ping example.com
            </pre>

            Check DNS server configuration, DNS records and connectivity.
            """

        # Port
        if any(x in q for x in [
            "port",
            "connection refused",
            "timeout"
        ]):

            return """
            <h3>🌐 Network - Port / Connection Problem</h3>

            <pre>
ping &lt;host&gt;
nslookup &lt;domain&gt;
tracert &lt;host&gt;
            </pre>

            <b>Check:</b>

            <ul>
                <li>IP connectivity.</li>
                <li>DNS.</li>
                <li>Required port.</li>
                <li>Firewall.</li>
                <li>Security Group.</li>
                <li>Routing.</li>
            </ul>
            """

        return """
        <h3>🌐 Network Troubleshooting</h3>

        <pre>
ipconfig
ping &lt;host&gt;
nslookup &lt;domain&gt;
tracert &lt;host&gt;
        </pre>

        Check IP configuration, DNS, routing, firewall and connectivity.
        """

    # =====================================================
    # DEFAULT
    # =====================================================

    return """
    <h3>🤖 DevOps Support Assistant</h3>

    <p>
    I could not identify the exact problem yet.
    </p>

    <p><b>Supported areas:</b></p>

    <ul>
        <li>🐧 Linux</li>
        <li>🐳 Docker</li>
        <li>🔧 Git / GitHub</li>
        <li>🔨 Jenkins / CI-CD</li>
        <li>☁️ AWS EC2 / S3 / IAM / VPC</li>
        <li>🌐 Networking / DNS / Ports</li>
        <li>☸️ Kubernetes</li>
    </ul>

    <p>
    <b>Example:</b>
    My Kubernetes pod is in CrashLoopBackOff
    </p>
    """


# =========================================================
# FLASK ROUTE
# =========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""

    if request.method == "POST":
        question = request.form.get("question", "")
        answer = troubleshoot(question)

    return render_template("index.html", answer=answer)


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)