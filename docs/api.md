# REST API

Default base URL: `http://127.0.0.1:8787`. Interactive OpenAPI docs: `/docs`.

## Add knowledge

```sh
curl -X POST http://127.0.0.1:8787/api/documents \
  -H 'Content-Type: application/json' \
  -d '{"name":"refund.md","text":"Customers can request a refund within 30 days."}'
```

`POST /api/upload` accepts multipart field `file`, a UTF-8 `.md` or `.txt` file, up to 200 KB. JSON document text is limited to 200,000 characters. The workspace holds up to 100 documents. Re-importing identical name + content is idempotent. Use `GET /api/documents` and `DELETE /api/documents/{id}` to manage sources. Deleting sources preserves saved traces.

## Inspect a question

```sh
curl -X POST http://127.0.0.1:8787/api/query \
  -H 'Content-Type: application/json' \
  -d '{"question":"How many days to request a refund?","provider":"ollama","generator":"ollama","top_k":4,"policy":{"support_threshold":0.7,"conflict_threshold":0.35}}'
```

PowerShell:

```powershell
$body = @{
  question="How many days to request a refund?"
  provider="ollama"
  generator="ollama"
} | ConvertTo-Json
$trace = Invoke-RestMethod http://127.0.0.1:8787/api/query -Method Post -ContentType "application/json" -Body $body
$trace.action
```

Providers: `demo`, `ollama`, `laya`, `jev`; omit to use the configured default. Generators: `extractive` (verbatim excerpts) or `ollama`. `top_k`: 1–8, default 4. Questions: 3–500 nonblank characters. `support_threshold`: 0.25–1; `conflict_threshold`: 0.05–1.

The response is a saved trace with `schema_version=1`, `id`, `created` (UTC), `action`, `reason`, `decision`, `evidence`, `claims`, `policy`, `timing_ms` and `input_state`. `generator_called` distinguishes a generator call from evidence-only output; `generation_error` records generation failures. `decision.raw_probabilities` preserves Ollama's original scores. `decision.question_schema` preserves the System One questions.

Routing order: no evidence → abstain; conflict threshold → review; support threshold → answer; combined support + partial ≥ 0.5 → retrieve more; otherwise abstain. The last boundary is fixed in this release.

Provider-reported truncation overrides the route with `retrieve_more` and blocks generation, including replay. Extra Laya usage fields such as `truncated_questions` are retained.

Provider failures return HTTP 502 without switching to demo. Generation failures preserve the judged trace and surface an empty answer with `generation_error`. They do not replace a failed model response with synthetic claims.

## Replay an existing judgment

```sh
curl -X POST http://127.0.0.1:8787/api/traces/TRACE_ID/replay \
  -H 'Content-Type: application/json' \
  -d '{"policy":{"support_threshold":0.95,"conflict_threshold":0.35}}'
```

Returns the new `action`, `original_action`, policy and `inference_calls: 0`. Does not retrieve, generate, or mutate the original trace.

## Other endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Process health and version |
| GET | `/api/config` | Public defaults; no credentials |
| POST | `/api/samples` | Add original fictional sample knowledge |
| POST | `/api/samples/conflict` | Add sample knowledge and conflicting refund draft |
| GET | `/api/traces` | Most recent 30 decisions |
| GET | `/api/traces/{id}` | Complete saved snapshot |
| GET | `/api/traces/{id}/export` | Download JSON with evidence text |

The workbench accepts localhost hosts and rejects cross-origin browser writes. CLI clients need no Origin header. It has no user authentication; it is intended to bind to loopback. Exported traces include questions and source text, so inspect them before sharing.
