# 02 — RQ (Redis Queue): Distributed Task Queuing Made Simple

RQ is a lightweight Python library for queueing jobs and processing them
in the background with workers. Backed by Redis.

## Prerequisites

Redis must be running locally:
```bash
# macOS
brew install redis && brew services start redis

# Ubuntu/Debian
sudo apt install redis-server && sudo systemctl start redis

# Docker (easiest)
docker run -d -p 6379:6379 redis:alpine
```

## Run the Examples

**Terminal 1 — Start a worker:**
```bash
cd 02_rq
rq worker            # starts a worker on the default queue
```

**Terminal 2 — Enqueue jobs:**
```bash
python basic_queue.py
python job_callbacks.py
python scheduled_jobs.py
```

## Key Concepts

- `Queue` — holds jobs waiting for a worker
- `job = q.enqueue(fn, args)` — puts a function call on the queue
- `rq worker` — CLI command to start a background worker process
- Jobs are serialized via `pickle` and stored in Redis
- Results are stored back in Redis (TTL configurable)

## Monitoring

```bash
# Built-in CLI
rq info

# Web dashboard (install separately)
pip install rq-dashboard
rq-dashboard
# → open http://localhost:9181
```
