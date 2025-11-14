# VO2 FIT Parser API

Simple Flask service that accepts `.fit` or `.zip` uploads and returns the VO2 value stored in the FIT file (message 140 field 7) converted using vo2 = value * 3.5 / 65536.

Endpoints
- GET /         => health check
- POST /upload  => form multipart file field `file`. Returns JSON.

Example:
curl -s -F "file=@/path/to/activity.fit" https://your-deploy-url/upload
