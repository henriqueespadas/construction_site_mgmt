from odoo import models, fields, api
import werkzeug
import logging

_logger = logging.getLogger(__name__)

class ConstructionProject(models.Model):
    _name = "cstr.project"
    _inherits = {"project.project": "project_id"}

    project_id = fields.Many2one("project.project", string="Project")
    supplier_id = fields.Many2one("cstr.supplier", string="Supplier")
    budget = fields.Float(string="Budget")
    costs = fields.Float(string="Costs")
    address = fields.Char(string="Address")
    number = fields.Char(string="Number")
    cep = fields.Char(string="cep")
    bairro = fields.Char(string="Bairro")
    google_maps_url = fields.Char(string="Google Maps URL", compute="_compute_google_maps_url")

    def _get_api_key(self):
        api_key = self.env['ir.config_parameter'].sudo().get_param('google_maps_api_key')
        if not api_key:
            _logger.warning("Google Maps API key not found")
        return api_key

    @api.depends('address', 'number', 'bairro', 'cep')
    def _compute_google_maps_url(self):
        api_key = self._get_api_key()
        if not api_key:
            self.google_maps_url = False
            return
        BASE_URL = "https://www.google.com/maps/embed/v1/place"
        address_parts = filter(None, [self.address, self.number, self.bairro, self.cep])
        address_full = ', '.join(address_parts)

        if not address_full.strip():
            self.google_maps_url = False
            return

        query = werkzeug.urls.url_encode({'key': api_key, 'q': address_full})
        self.google_maps_url = f"{BASE_URL}?{query}"


