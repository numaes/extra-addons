# muk_web_theme and theme_liquid_glass on 20.0 — plan

Date: 2026-09-24 · Source: extra-addons-18.0 (18.0 branch) · Target: extra-addons-20.0

Modules:
- muk_web_theme, with its dependencies muk_web_appsbar, muk_web_chatter,
  muk_web_colors and muk_web_dialog;
- theme_liquid_glass.
The customer's backend stack is muk_web_theme + theme_liquid_glass.

## Measured

| Module | JS files/lines | SCSS files/lines | Notes |
|---|---|---|---|
| muk_web_appsbar | 3/93 | 5/132 | webclient + apps bar, app menu service |
| muk_web_chatter | 4/180 | 2/17 | patches the chatter, form compiler/renderer |
| muk_web_colors | 0 | 3/62 | stores colours through `web_editor.assets` |
| muk_web_dialog | 1/16 | 1/6 | dialog size toggle |
| muk_web_theme | 2/79 | 5/90 | depends on the four above |
| theme_liquid_glass | 2/69 | 9/1226 | pure SCSS mostly |

Blocking differences in 20.0:
- `web_editor` no longer exists. muk_web_colors depends on it and uses its
  `web_editor.assets` model (save, reset and read customised SCSS). It will carry its
  own `muk_web_colors.assets` with the part it needs, on 20's `ir.attachment` (`raw`)
  and `ir.asset`.
- OWL 3: run the upstream script and `numa-addons-20.0/tools/owl3_fixup.py`, then check
  every patch target (NavBar, WebClient, Chatter, FormCompiler/Renderer, Dialog) still
  exists with the same shape.
- No Font Awesome: `numa-addons-20.0/tools/fa_to_oi.py`.
- The manifest version must be 20.0.x, or the module is uninstallable.

## Steps
- [ ] Copy the six modules; set 20.0 versions; replace web_editor with html_editor where
      a dependency is still needed at all.
- [ ] muk_web_colors: its own assets model; settings read/write colours.
- [ ] OWL 3 and icons.
- [ ] Install all six on a fresh 20.0 database; fix what the install finds.
- [ ] Browser tests (red first where applicable): the web client boots with no error; the
      apps bar renders; the chatter position setting applies; changing a colour in
      settings changes the compiled bundle; liquid glass loads.
- [ ] Screenshots light and dark, with the numa_planning Gantt (theme rule).

## Review
(to be filled in)
