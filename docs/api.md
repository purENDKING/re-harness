# API

## Start session

```bash
curl -X POST http://127.0.0.1:8000/sessions/start \
  -H "Content-Type: application/json" \
  -d '{
    "sample_path": "samples/game.exe",
    "ghidra_project": "projects/demo.gpr",
    "target_process": "game.exe"
  }'
```

## Push context

```bash
curl -X POST http://127.0.0.1:8000/context/push \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "REPLACE_SESSION_ID",
    "current_function_addr": "0x140001000",
    "current_selection": "player->inventory",
    "current_decompile": "int __fastcall sub_140001000(Player* player) { return player->hp; }",
    "goals": ["verify structure field meaning", "generate hook prototype"]
  }'
```

## Run verify-structure workflow

```bash
curl -X POST http://127.0.0.1:8000/workflows/verify-structure \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "REPLACE_SESSION_ID"
  }'
```

## Run generate-hook path

```bash
curl -X POST http://127.0.0.1:8000/workflows/generate-hook \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "REPLACE_SESSION_ID"
  }'
```

## List review items

```bash
curl http://127.0.0.1:8000/review/REPLACE_SESSION_ID
```

## Approve review item

```bash
curl -X POST http://127.0.0.1:8000/review/REPLACE_ITEM_ID/approve
```

## Reject review item

```bash
curl -X POST http://127.0.0.1:8000/review/REPLACE_ITEM_ID/reject
```
