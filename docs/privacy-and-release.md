# Privacy And Release Checklist

Use this before pushing a short-drama project to a public repository.

## Never Commit

- API keys
- `.env` files
- local keychain exports
- task IDs when they can expose private generation history
- signed download URLs
- raw API responses
- private product images
- customer files
- generated videos unless intentionally public
- local absolute paths that reveal private folders

## Safe To Commit

- sanitized methodology
- generic prompt templates
- sample scripts with placeholders
- example episode text with no private asset path
- `.env.example`
- public-safe README

## Key Scan

Before pushing, run a text scan for:

```text
API_KEY
SECRET
TOKEN
Bearer
sk-
gho_
SALPX_API_KEY
download-
task_
absolute home paths
```

Any hit must be reviewed. Some words may appear in safety docs, but real values must not.

## Product Claim Safety

For pet health or nutrition products, avoid:

- cure
- treat
- guaranteed
- instant recovery
- medical result
- disease claims

Safer language:

- daily nutrition support
- feeding routine
- body-weight feeding amount
- mixed with dog food
- feeding record
- observe and adjust
