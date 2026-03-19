from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EventEvent(models.Model):
    _inherit = 'event.event'

    allowed_group_id = fields.Many2one(
        'res.groups', 
        string='Grupo Permitido'
    )
    
    # Campo calculado para controlar a visibilidade
    is_user_allowed = fields.Boolean(
        compute='_compute_is_user_allowed',
        compute_sudo=True # ESSENCIAL para o Website
    )

    @api.depends('allowed_group_id')
    def _compute_is_user_allowed(self):
        for event in self:
            # Se não houver grupo, todos podem ver
            if not event.allowed_group_id:
                event.is_user_allowed = True
                continue
            
            # Se for utilizador público, não tem acesso
            user = self.env.user
            if not user or user._is_public():
                event.is_user_allowed = False
                continue

            # Verifica se o ID do grupo está nos grupos do utilizador
            event.is_user_allowed = event.allowed_group_id.id in user.groups_id.ids

class EventRegistration(models.Model):
    _inherit = 'event.registration'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            event = self.env['event.event'].browse(vals.get('event_id'))
            if event and event.allowed_group_id:
                user = self.env.user
                if user._is_public() or event.allowed_group_id.id not in user.groups_id.ids:
                    raise ValidationError(_(
                        "Atenção! Este evento é exclusivo para o grupo '%s'."
                    ) % event.allowed_group_id.name)
        
        return super().create(vals_list)