from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError,UserError
from odoo.modules.module import get_module_resource
from datetime import datetime
from datetime import timedelta
from datetime import date
from dateutil.relativedelta import relativedelta


class Biblioteka(models.Model):
    _name = "biblioteka.biblioteka"
    _description="Biblioteka"

    name = fields.Char(string="Name", required=True)
    status = fields.Char(string="Status")
    date_aprovimi = fields.Date(string='Start Date', default=datetime.today())
    date_dorezimi = fields.Date(string='End Date')

    arsye_vonese = fields.Text(string="Late explanation")
    lexues_id = fields.One2many('biblioteka.lexues', 'lexues_id', string="ID_User")
    liber_id = fields.One2many('biblioteka.librat', 'liber_id', string="ID_Book")


class Librat(models.Model):
    _name = "biblioteka.librat"
    _description = "Library"

    title = fields.Char(string="Title", required=True)
    author = fields.One2many('biblioteka.author', 'name',  string="Author", required=True)
    sasi_fizike = fields.Integer(string="Quantity")
    sasi_gjendje = fields.Integer(string="State")
    informacion = fields.Char(string="About")
    disponueshmeria = fields.Boolean(string="Disponible", default=True)
    rezervuar = fields.Char(string="Book Reservation")
    rezervuar = fields.Selection([('available', 'Available'), ('non-available', 'Non-Available')],
                                 string="Book Reservation", default='available')
    liber_id = fields.Many2one('biblioteka.biblioteka', string="ID")


class Lexues(models.Model):
    _name = "biblioteka.lexues"
    _description = "Lexues"

    lexues_id = fields.Many2one('biblioteka.biblioteka', string="ID_User")
    name = fields.Char(string="Name", required=True)
    mbiemer = fields.Char(string="Surname", required=True)
    mosha = fields.Date(string="Age", required=True)
    informacion = fields.Char(string="Information")
    date_regjistrimi = fields.Date(string="Date Regjistrimi")
    date_skadence = fields.Date(string="Date Skadence")
    date_cregjistrimi = fields.Date(string="Date Cregjistrimi")
    date_perjashtimi = fields.Date(string="Date Perjashtimi")
    status = fields.Selection([('draft', 'Draft'),('regjistruar', 'Regjistruar'), ('perjashtuar', 'Perjashtuar'), ('skaduar', 'Skaduar'), ('cregjistruar', 'Cregjistruar')], default='draft')
    vlefshmeria = fields.Date(string="Vlefshmeria", compute='_compute_duedate')
    afat_riregjistrimi = fields.Datetime(string="Riregjistrim")

    @api.multi
    def _compute_duedate(self):
        d = date.fromordinal(730920)
        datetime.date(datetime.today())
        t=d.timetuple()
        i=0
        for i in t:
            if i==1:
                muaji=t(i)+1
            if i==2:
                dita=t(i)
        self.vlefshmeria=datetime.date(2018,muaji,dita)


    @api.multi
    def draft_progressbar(self):
        self.ensure_one()
        self.write({
             'status': 'draft',
         })

    @api.multi
    def regjistruar_progressbar(self):
        self.ensure_one()
        self.write({
             'status': 'regjistruar',
        })

    @api.multi
    def skaduar_progressbar(self):
        self.ensure_one()
        self.write({
            'status': 'perjashtuar',
        })

    @api.multi
    def cregjistruar_progressbar(self):
        self.ensure_one()
        self.write({
            'status': 'skaduar',
        })

    @api.multi
    def riregjistruar_progressbar(self):
        self.ensure_one()
        self.write({
            'status': 'cregjistruar',
        })


    @api.multi
    def _check_date(self):
        for lexues in self:
            #raise UserError(_("%s,%s,%s")%(  lexues.vlefshmeria ,fields.Datetime.now(),lexues.vlefshmeria < fields.Datetime.now()))
            if lexues.vlefshmeria < fields.Datetime.now():
                return lexues.write({'status':'skaduar'})
            return True


    _constraints = [
        (_check_date, 'Your Message!', ['date_regjistrimi', 'date_skadence']),
    ]


class Author(models.Model):
    _name = 'biblioteka.author'
    _description = "Author"

    name = fields.Char(string="Name", required=True, select=True)
    born_date = fields.Date(string="Date of Birth")
    death_date = fields.Date(string="Date of Death")
    note = fields.Text(string="Information")
