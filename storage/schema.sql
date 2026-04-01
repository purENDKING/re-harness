CREATE TABLE IF NOT EXISTS sessions (
  id TEXT PRIMARY KEY,
  sample_path TEXT NOT NULL,
  ghidra_project TEXT,
  target_process TEXT,
  status TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS observations (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  source TEXT NOT NULL,
  object_ref TEXT NOT NULL,
  payload TEXT NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  FOREIGN KEY(session_id) REFERENCES sessions(id)
);

CREATE TABLE IF NOT EXISTS hypotheses (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  status TEXT NOT NULL,
  confidence REAL NOT NULL,
  evidence TEXT NOT NULL,
  FOREIGN KEY(session_id) REFERENCES sessions(id)
);

CREATE TABLE IF NOT EXISTS patch_candidates (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  target_addr TEXT NOT NULL,
  method TEXT NOT NULL,
  rationale TEXT NOT NULL,
  project_path TEXT,
  build_ok INTEGER NOT NULL DEFAULT 0,
  runtime_ok INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY(session_id) REFERENCES sessions(id)
);

CREATE TABLE IF NOT EXISTS reviews (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  item_type TEXT NOT NULL,
  target_ref TEXT NOT NULL,
  proposal TEXT NOT NULL,
  status TEXT NOT NULL,
  FOREIGN KEY(session_id) REFERENCES sessions(id)
);
