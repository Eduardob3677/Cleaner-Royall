# Premium server helpers

Use `generate_premium_response.py` to create the JSON response the server expects
to mark a subscription as active. The script writes the response into
`server/premium/users/` by default.

Example:

```bash
python3 generate_premium_response.py --pid "<premium-id>" --key "<activation-key>" --uid "<device-uid>"
```

The response is created with status `1` (active) by default; pass `--status 0` to
disable an entry or `--force` to overwrite an existing file.
