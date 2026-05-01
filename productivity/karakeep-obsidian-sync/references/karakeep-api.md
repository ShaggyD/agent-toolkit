# Karakeep API Reference

Karakeep is a self-hostable bookmarking / read-it-later service (formerly Hoard/Hoarder).
Docs: https://docs.karakeep.app/api/karakeep-api

## Base URL

`https://<your-instance>/api/v1`

## Authentication

Bearer token in `Authorization` header. Generate from: Settings → API Keys.

```
Authorization: Bearer <api-key>
```

Key format: `ak2_...` (starts with `ak2_` prefix).

## Bookmark Types

| Type | Description |
|------|-------------|
| `link` | URL with optional crawled metadata (title, description, OG image, screenshot) |
| `text` | Plain text note |
| `asset` | Uploaded file (image or PDF) |

## Key Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/bookmarks` | List bookmarks (cursor pagination) |
| `GET` | `/bookmarks/{id}` | Get single bookmark |
| `POST` | `/bookmarks` | Create bookmark (`type` + `url`/`text`) |
| `PATCH` | `/bookmarks/{id}` | Update fields (title, note, archived, favourited) |
| `DELETE` | `/bookmarks/{id}` | Delete bookmark |
| `POST` | `/bookmarks/{id}/tags` | Attach tags (body: `{"tags": [{"tagName": "..."}]}`) |
| `DELETE` | `/bookmarks/{id}/tags` | Detach tags (body: `{"tags": [{"tagName": "..."}]}`) |
| `GET` | `/tags` | List all tags (cursor pagination) |

## Pagination

Cursor-based. Response includes `nextCursor`. Pass as `cursor` param for next page.
`null` nextCursor = no more results.

## Known Quirks

- **User-Agent block:** Python's default `urllib` User-Agent (`Python-urllib/3.x`) returns 403.
  Always set a custom UA like `kk-cli/0.3`.
- **DELETE responses:** Returns 204 No Content with empty body. Client must handle empty
  response gracefully.
- **Tag format:** Tag attach/detach uses `POST` and `DELETE` (not `PUT`), and the body format
  is `{"tags": [{"tagName": "tag-name"}]}` — objects with `tagName` keys, not plain strings.
- **Short IDs:** The API uses long alphanumeric IDs. You cannot use truncated IDs.
- **No `after` filter on list:** The `GET /bookmarks` endpoint doesn't support time-based
  filtering by default. Use cursor pagination and client-side filtering by `createdAt`.
