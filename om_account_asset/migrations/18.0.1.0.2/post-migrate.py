from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    lines = env['account.asset.depreciation.line'].search([])
    if not lines:
        return

    # Recompute move_posted_check (stored computed field)
    lines._get_move_posted_check()

    # Recompute parent_state (stored related field - use the auto-generated compute method)
    field = lines._fields.get('parent_state')
    if field and field.compute:
        lines.invalidate_recordset(['parent_state'])
        getattr(lines, field.compute)()