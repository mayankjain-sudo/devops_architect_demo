🛡️ Enterprise DevSecOps Pipeline Documentation
===============================================

This GitHub Actions workflow implements a secure Software Supply Chain (SSC) by ensuring that every image deployed to the **GitHub Container Registry (GHCR)** is scanned for vulnerabilities and cryptographically signed.

🚀 Pipeline Architecture
------------------------

The pipeline is divided into five functional stages:

1.  **Build & Test:** Validates code quality.
    
2.  **Security Scanning:** Checks dependencies and the final container for vulnerabilities.
    
3.  **Immutable Build:** Builds the Docker image and captures its unique **SHA Digest**.
    
4.  **Cryptographic Signing:** Uses **Cosign** (Keyless) to sign the image digest.
    
5.  **Verified Deployment:** Verifies the signature before allowing deployment.
    

🛠️ Workflow Configuration Breakdown
------------------------------------

### 1\. Permissions & Triggers

To use **Keyless Signing**, the workflow requires specific permissions to interact with GitHub's OIDC (OpenID Connect) provider.

### 2\. The Build & Push Job (docker)

Instead of using standard tags (which can be overwritten), this job outputs the **Image Digest**. A digest is a unique, immutable SHA256 hash of the image layers.

*   **Tool:** docker/build-push-action@v5
    
*   **Why:** Capturing the outputs.digest ensures that the "Container Scan" and "Cosign Sign" jobs are looking at the exact same bits that were just built.
    

### 3\. Vulnerability Scanning (container-scan)

*   **Tool:** aquasecurity/trivy-action
    
*   **Action:** Scans the image for **HIGH** and **CRITICAL** vulnerabilities.
    
*   **Best Practice:** We point Trivy to the image@digest rather than image:tag to prevent "race conditions" where a tag might point to a different image during the scan.
    

### 4\. Keyless Signing (cosign-sign)

This is the heart of the "Sec" in DevSecOps.

*   **Mechanism:** It uses **Sigstore/Cosign**. Instead of managing a private .key file (which can be stolen), it uses the GitHub Action's identity.
    
*   **Command:** \`\`\`bash cosign sign --yes "env.IMAGEN​AME@{{ needs.docker.outputs.image\_digest }}"
    
*   **Result:** A signature is uploaded to GHCR alongside your image. It proves: "This image was built by _this_ specific GitHub repository and _this_ specific workflow."
    

### 5\. Verified Deployment (deploy-dev/prod)

Before any deployment code runs, the pipeline executes a **Verification Gate**.

> \[!IMPORTANT\] If a malicious actor manually pushes a different image to your registry with the same tag, the verify step will **FAIL** because the signature won't match. This prevents "Image Poisoning" attacks.

📋 Security Checklist Summary
-----------------------------

❓ Frequently Asked Questions
----------------------------

**Q: Why did I get a "DENIED: invalid token" error?** **A:** This usually happens if the cosign job doesn't have an explicit login-action step or if the permissions block is missing packages: write.

**Q: What is the difference between a Tag and a Digest?** **A:** A **Tag** (like :latest) is a pointer that can move. A **Digest**(like @sha256:abc...) is a permanent fingerprint. Security tools should always use Digests.