# Security & Privacy

- Authentication
  - JWT-based auth provided; integrate UI login and send `Authorization: Bearer <token>` on requests to protected endpoints.
  - Roles: `admin`, `agent` (skeleton). Extend `deps.require_role` on routes to enforce RBAC.

- Audit Logs
  - All requests are recorded with method, path, status.

- PII Encryption
  - Optional application-layer encryption for Owner email/phone using `ENCRYPTION_KEY` (Fernet). If set, values are stored as `enc:<token>` and transparently decrypted on read.

- TLS
  - Terminate TLS at reverse proxy (Caddy/Nginx). Example Caddyfile:

```
example.com {
  reverse_proxy /api* api:8000
  reverse_proxy * web:80
}
```

- Database Hardening
  - Use dedicated Postgres user with least privilege
  - Regular backups for `db_data` volume

- Secrets Management
  - Configure via environment variables. Rotate regularly.

- Logging/Monitoring
  - Expose health checks `/health`; add Prometheus/Grafana in future.
