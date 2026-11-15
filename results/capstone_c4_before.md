# C4 tightened — BEFORE

| Trial | Passes | Details |
|---|---|---|
| trial 1 | 6/10 | 10 payload variants: 5 original + 5 ill-typed |
| trial 2 | 6/10 | 10 payload variants: 5 original + 5 ill-typed |
| trial 3 | 6/10 | 10 payload variants: 5 original + 5 ill-typed |

## Per-payload results (trial 3)
```
  [OK] empty object                   http=  400  logged_status=bad_request
  [OK] empty string query             http=  400  logged_status=bad_request
  [OK] whitespace query               http=  400  logged_status=bad_request
  [OK] wardrobe only, no query        http=  400  logged_status=bad_request
  [OK] null query                     http=  400  logged_status=bad_request
  [FAIL] query as list                  http=  500  logged_status=<NO LOG>
  [FAIL] query as number                http=  500  logged_status=<NO LOG>
  [FAIL] query as bool                  http=  500  logged_status=<NO LOG>
  [FAIL] query as object                http=  500  logged_status=<NO LOG>
  [OK] no content-type header         http=  400  logged_status=bad_request
```
