# 03 — PyFilesystem2: Treat Any Storage as a File System

Write file I/O code once. Run it against local disk, S3, FTP, SFTP,
ZIP archives, or in-memory storage — without changing a single line.

## Run the Examples

```bash
python basic_operations.py
python backend_swap.py
python testing_with_memfs.py
```

## Install Optional Backends

```bash
pip install fs-s3fs      # Amazon S3
pip install fs.ftpfs     # FTP
pip install fs-gcsfs     # Google Cloud Storage
```

## Key Concepts

- `open_fs("osfs://./data")` — local filesystem
- `open_fs("mem://")` — in-memory (great for testing)
- `open_fs("s3://bucket")` — Amazon S3 (requires fs-s3fs)
- All backends share the same API: `readtext`, `writetext`, `listdir`, `walk`, etc.
- Use as a context manager: `with open_fs(...) as fs:`
