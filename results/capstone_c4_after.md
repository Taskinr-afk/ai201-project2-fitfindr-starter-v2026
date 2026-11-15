# C4 tightened — AFTER

| Trial | Passes | Details |
|---|---|---|
| trial 1 | 10/10 | 10 payload variants: 5 original + 5 ill-typed |
| trial 2 | 10/10 | 10 payload variants: 5 original + 5 ill-typed |
| trial 3 | 10/10 | 10 payload variants: 5 original + 5 ill-typed |

## Per-payload results (trial 3)
```
  [OK] empty object                   http=  400  logged_status=bad_request
  [OK] empty string query             http=  400  logged_status=bad_request
  [OK] whitespace query               http=  400  logged_status=bad_request
  [OK] wardrobe only, no query        http=  400  logged_status=bad_request
  [OK] null query                     http=  400  logged_status=bad_request
  [OK] query as list                  http=  400  logged_status=bad_request
  [OK] query as number                http=  400  logged_status=bad_request
  [OK] query as bool                  http=  400  logged_status=bad_request
  [OK] query as object                http=  400  logged_status=bad_request
  [OK] no content-type header         http=  400  logged_status=bad_request
```
