# Kiro Integration Handoff (LiteLLM UI + Proxy)

This handoff doc summarizes what was implemented for Kiro provider support and where to continue if needed.

## Scope completed

- Added Kiro provider metadata to public provider fields endpoint.
- Added Kiro provider support in UI provider helper mappings.
- Added dedicated Kiro Settings page in dashboard app-router (`/ui/settings/kiro`).
- Added backend general settings fields for Kiro model id + refresh token.
- Added dashboard networking save logic for Kiro settings.
- Added AI Gateway board navigation entry for Kiro in legacy sidebar.
- Improved UI route restructuring logic in proxy startup for extensionless routes.

---

## Key files changed / relevant

### Backend: provider metadata + config types

- `litellm/proxy/public_endpoints/provider_create_fields.json`
  - Kiro entry present:
    - `provider: "KIRO_GATEWAY"`
    - `provider_display_name: "Kiro Gateway"`
    - `litellm_provider: "kiro_gateway"`
    - fields include `api_base`, `api_key`, `refresh_token`

- `litellm/constants.py`
  - `kiro_gateway` included in:
    - `openai_compatible_providers`
    - `openai_text_completion_compatible_providers`

- `litellm/proxy/_types.py`
  - `ConfigGeneralSettings` includes:
    - `kiro_model_id`
    - `kiro_refresh_token`

- `litellm/proxy/proxy_server.py`
  - config metadata includes types for:
    - `kiro_model_id`
    - `kiro_refresh_token`

### UI: provider mapping + settings page

- `ui/litellm-dashboard/src/components/provider_info_helpers.tsx`
  - `Providers.KiroGateway = "Kiro Gateway"`
  - provider map includes `kiro_gateway`
  - placeholder set to `kiro_gateway/claude-sonnet-4-5` (normalized kiro-gateway model id)

- `ui/litellm-dashboard/src/components/kiro_settings.tsx`
  - form to load/save:
    - Kiro Model ID
    - Kiro Refresh Token

- `ui/litellm-dashboard/src/components/networking.tsx`
  - `updateKiroSettings(...)` posts to `/config/field/update` with `config_type=general_settings`

- `ui/litellm-dashboard/src/app/(dashboard)/settings/kiro/page.tsx`
  - route component for `/settings/kiro`

- `ui/litellm-dashboard/src/app/(dashboard)/components/Sidebar2.tsx`
  - settings child menu entry for Kiro
  - route mapping for `kiro-settings -> settings/kiro`

### Legacy UI route/nav path (AI Gateway board)

- `ui/litellm-dashboard/src/components/leftnav.tsx`
  - added menu item:
    - key/page `kiro-settings`
    - label `Kiro`

- `ui/litellm-dashboard/src/app/page.tsx`
  - added legacy page switch case:
    - `page == "kiro-settings"` renders `<KiroSettings accessToken={accessToken} />`

### Proxy UI route restructuring fix

- `litellm/proxy/proxy_server.py`
  - added `_has_unrestructured_html_routes(...)`
  - restructured startup logic to run incremental restructuring when needed
  - fixes extensionless route gaps when UI is partially pre-restructured

---

## Tests and checks performed

- Unit/integration checks in prior run included:
  - provider metadata tests for Kiro public fields
  - provider helper placeholder tests for Kiro

- UI/Runtime checks done in local container/session:
  - `/ui/settings/kiro/` returns `200` in running LiteLLM container
  - save/load via backend endpoints verified:
    - `GET /config/list?config_type=general_settings`
    - `POST /config/field/update`

---

## Known runtime note

There is an unrelated DB schema error in logs:

- Missing column `LiteLLM_PolicyTable.version_number`

This is not part of Kiro changes, but appears repeatedly during startup/policy sync.

---

## Follow-up checklist for next agent

1. Verify current served UI bundle contains latest legacy sidebar Kiro item.
   - If stale chunk still served, ensure final static out copied from latest dashboard build before image build.
2. Open `/ui/` and verify AI Gateway sidebar includes `Kiro` entry.
3. Click `Kiro` entry and ensure it lands on Kiro settings UI and saves values correctly.
4. Keep proxy route restructuring logic as-is unless there is a regression in extensionless routes.

---

## Useful commands

```bash
# Build dashboard UI
cd /workspaces/litellm/ui/litellm-dashboard && npm run build

# (if needed) sync static out into proxy package dir
cp -r /workspaces/litellm/ui/litellm-dashboard/out/* /workspaces/litellm/litellm/proxy/_experimental/out/

# Rebuild/restart LiteLLM container from local source
docker compose -f /workspaces/litellm/docker-compose.yml build litellm
docker compose -f /workspaces/litellm/docker-compose.yml up -d --force-recreate litellm

# Basic route checks
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:4000/ui/settings/kiro/
```
