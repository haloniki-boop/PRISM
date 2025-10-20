# ./deploy/tailscale/README.md - v1.0.0

# Tailscale Connectivity (Optional)

This project does not depend on Tailscale at runtime. If your Notion MCP or other services are hosted behind a Tailscale network, connect your Docker host to the same tailnet before running `docker-compose`.

Steps (do not include secrets):
1. Install Tailscale on your host (`https://tailscale.com/download`).
2. `tailscale up` and authenticate to your tailnet (admin approval may be required).
3. Verify connectivity to internal services (e.g., `ping <tailscale-ip>`).
4. Start PRISM: `docker-compose up -d` from `prism/deploy`.

Security notes:
- Never commit auth keys or device IDs.
- Prefer ACLs and machine auth with expiry.
- Rotate keys regularly.

EOF ./deploy/tailscale/README.md - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成
