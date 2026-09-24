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
- [x] Copy the six modules; set 20.0 versions; replace web_editor with html_editor where
      a dependency is still needed at all.
- [x] muk_web_colors: its own assets model; settings read/write colours.
- [x] OWL 3 and icons.
- [x] Install all six on a fresh 20.0 database; fix what the install finds.
- [x] Browser tests (red first where applicable): the web client boots with no error; the
      apps bar renders; the chatter position setting applies; changing a colour in
      settings changes the compiled bundle; liquid glass loads.
- [x] Screenshots light and dark, with the numa_planning Gantt (theme rule).

## Review (2026-09-24)

The six modules install and work on 20.0. Verified in a browser: the customer stack
(both themes), MuK alone, and the numa_planning Gantt under liquid glass.

What 20.0 changed, module by module:
- **muk_web_colors**: web_editor is gone. `muk_web_colors.assets` carries the part of
  `web_editor.assets` it used, on `ir.attachment.raw` (`datas` is gone), and follows the
  same `/_custom/<bundle><url>` scheme, so 18.0 customisations are read back. The dark
  reset called the generic `reset_asset`; both modes now use `reset_color_asset`.
- **muk_web_theme**: it still asked `web_editor.assets` for its theme colours, so
  Settings would not open. The post-install hook writes images as `BinaryBytes` (a
  Binary field no longer takes base64 bytes).
- **muk_web_appsbar**: `web.webclient_bootstrap` passes `body_classname.f` to
  web.layout instead of a t-set. It also fixes an 18.0 precedence bug: `'x' + y or
  'large'` never fell back. The `company` service is gone: `user.activeCompany`.
- **muk_web_chatter**:
  - The Chatter moved to `@mail/chatter/web_portal_project/chatter`.
  - Thread declares strict props with `useProps`, so the tracking toggle cannot pass
    a prop any more. It shares a reactive `trackingState`, and Thread filters
    `message_type == 'tracking'` in record chatters only, never in Discuss.
  - The topbar buttons follow 20.0's logic (`canPostMessage`, `webChatterProps`).
  - The compiled form ref is `__comp__.chatterContainer`.
- **muk_web_dialog**: rewritten on the dialog's own `dialogSize` signal, instead of a
  `data.size` the template had to be rewired to read.
- **theme_liquid_glass**:
  - The inherited templates got `this.` and `t-custom-portal`.
  - Core now paints the chatter container with the web client background, so it is
    made transparent again.
  - Each field has a label cell that is empty on desktop; liquid glass drew it as an
    empty bar, and that cell is no longer painted.
- Everywhere: OWL 3 (the upstream script plus owl3_fixup), Font Awesome replaced with
  Material Symbols, and manifest versions set to 20.0.

Tests:
- muk_web_colors, 3 (Python): save and read back, the dark bundle, reset.
- muk_web_theme, 6 (browser): the apps bar, the tracking toggle, chatter resize, dialog
  full screen, Settings opening, the apps menu.
- theme_liquid_glass, 2 (browser): the apps sidebar, and the form on the glass.
- Customer stack: 11, 0 failed. The apps menu test is skipped there, because liquid
  glass replaces that menu. MuK alone: 6, 0 failed.
- Red checks: each of these was reverted on its own, and its test failed.
  - the Settings fix;
  - the chatter background rule;
  - the empty-cell rule;
  - the Thread filter.
- The light and dark bundles compile on both databases. Community 20.0 never turns dark
  mode on (`color_scheme()` returns "light"; enterprise overrides it), so the dark
  styles are compiled but were not seen.

Seen, not changed:
- Discuss under liquid glass shows white text on a light panel. It is the same in
  18.0 on the customer mirror.
- MuK's apps menu nests an `<a>` inside the DropdownItem's `<a>`, as in 18.0.
