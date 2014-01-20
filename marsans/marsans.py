##############################################################################
#
# Copyright (c) 2004 TINY SPRL. (http://tiny.be) All Rights Reserved.
#                    Fabien Pinckaers <fp@tiny.Be>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from osv import osv, fields
import time
from datetime import datetime, date

class marsans_room(osv.osv):
	_inherit='product.product'
	#_name = 'marsans.room'
	_columns = {
		'isroom': fields.boolean('Is a Room'),
		'price_night': fields.integer('Price Night'),
		'hotel': fields.many2one('marsans.hotel','Hotel', ondelete='cascade' ),
		'm2': fields.integer('M2'),
		'beds': fields.selection([('1','One Bed'),('2','Two Beds'),('21','Double Bed'),('3','Double Bed and Extra bed')],'Beds'),
		'ac': fields.boolean('A/C'),
		'bathroom': fields.binary('Bathroom'),
		'bed_image':fields.binary('Bed image'),
		
	}
marsans_room()


class marsans_city(osv.osv):
	"""(NULL)"""
	_name = 'marsans.city'
	_columns = {
		'name': fields.char('City', size=32, required=True),
		'hotels': fields.one2many('marsans.hotel', 'city_id', 'Hotels'),
		'image': fields.binary('Image'),
	}
marsans_city()

class marsans_hotel(osv.osv):
	def name_get (self, cr, uid, ids, context=None):
		res=[]
		records = self.browse(cr,uid,ids)
		for r in records:
			res.append((r.id,r.city_id.name+","+r.name))
		return res
	"""(NULL)"""
	
	_name = 'marsans.hotel'
	_columns = {
		'name': fields.char('Name', size=32, required=True),
		'image': fields.binary('Image'),
		#'price': fields.integer('Price', required=True),
		'city_id': fields.many2one('marsans.city', 'City', required=True, ondelete='restrict'),
		'gallery': fields.one2many('marsans.gallery.hotel', 'hotel_id', 'Gallery'),
		'partner': fields.many2one('res.partner', 'Supplier'),
		'rooms': fields.one2many('product.product','hotel','Rooms'),
	}
marsans_hotel()

class marsans_gallery_hotel(osv.osv):
	"""(NULL)"""
	_name = 'marsans.gallery.hotel'
	_columns = {
		'name': fields.char('Name', size=32, required=True),
		'hotel_id': fields.many2one('marsans.hotel', 'Hotel', required=True,ondelete='cascade' ),
		'image': fields.binary('Image'),
	}
marsans_gallery_hotel()

class marsans_travel(osv.osv):
	def _compute_total_price(self, cr, uid, ids, field_name, arg, context=None):
		result={}
		for h in self.browse(cr, uid, ids, context=None):
			total=0
			for s in h.scales:
				total=total+s.total
			result[h.id]=total
		return result
		
	"""(NULL)"""
	_inherit = 'sale.order'
	#_name = 'marsans.travel'
	_columns = {
		#'name': fields.char('Name', size=64, required=True),
		#'partner_id': fields.many2one('res.partner', 'Client'),
		'scales': fields.one2many('sale.order.line', 'order_id', 'Scales'),
		'total': fields.function(_compute_total_price, type='float', method=True, string='Total',store=False),
		'istravel' : fields.boolean('Is a travel'),
	}
marsans_travel()

class marsans_scale(osv.osv):
	"""(NULL)"""

	def _compute_days(self, cr, uid, ids, field_name, arg, context=None):
		result = {}
		for h in self.browse(cr, uid, ids, context=None):
			dias = 0
			d1 = datetime.strptime(h.end, '%Y-%m-%d %H:%M:%S')
			d0 = datetime.strptime(h.date_i, '%Y-%m-%d %H:%M:%S')
			dias = abs((d1-d0).days)
			result[h.id] = dias
		return result

	def _compute_price(self, cr, uid, ids, field_name, arg, context=None):
		result = {}
		for h in self.browse(cr, uid, ids, context=None):
			result[h.id] = h.days * h.price
			self.write(cr,uid,h.id,{'price_unit': h.price,'product_uom_qty': h.days})
			print result[h.id]
		return result
		
	def get_hotels(self, cr, uid, ids, city, context=None): #https://doc.openerp.com/6.1/developer/03_modules_3/#onchange-event-link
		c=self.pool.get('marsans.city').browse(cr,uid,city)
		return {'domain':{'hotel': [('city_id','=',c.id)]}}
		
	def get_rooms(self, cr, uid, ids, hotel, context=None): #https://doc.openerp.com/6.1/developer/03_modules_3/#onchange-event-link
		h=self.pool.get('marsans.hotel').browse(cr,uid,hotel)
		return {'domain':{'product_id':[('hotel','=',h.id)]}}
		
	def check_datei(self,cr,uid,ids,date_i,context=None):
		res={}
	#	escalas=self.pool.get('sale.order').browse(cr,uid,order_id).scales
	#	for i in escalas:
	#		print i.date_i
		
		#res = {'warning':{'tile':'Error de fechas','message':'Esa fecha es de otra escala'}}
		res['warning'] = {'title': 'Error de fechas', 'message': 'Este dia ya forma parte de otra escala'} 
		#res['value'] = {'date_i':fields.datetime.now()}
		
		return res 
		
	#def _def_sel_cities(self, cr, uid, context=None):
	#	res=[] #http://help.openerp.com/question/21529/how-to-extend-fieldsselection-options-without-overwriting-them/
	#	totes=self.pool.get('marsans.city').search(cr,uid,[])
	#	citis=self.pool.get('marsans.city').browse(cr,uid,totes,context=None)
	#	for i in citis:
		#	res.append((i.id,i.name))	
		#print(res)
	#	return[(r[0],r[1]) for r in res] 
		#http://stackoverflow.com/questions/16578570/many-to-one-relation-not-working-in-fields-selection-in-openerp
	"""def _def_sel_hotels(self, cr, uid, context=None):
		res=[]
		totes=self.pool.get('marsans.hotel').search(cr,uid,[])
		citis=self.pool.get('marsans.hotel').browse(cr,uid,totes,context=None)
		for i in citis:
			res.append((i.id,i.name))	
		
		return[(r[0],r[1]) for r in res] 
		"""	
	#_name = 'marsans.scale'
	_inherit='sale.order.line'
	_order = "order_id,order_n"
	_columns = {
		'order_n': fields.integer('Order', required=True),
		#'travel_id': fields.many2one('sale.order','Travel',required=True),
		'city': fields.many2one('marsans.city','City'),
		#'hotel': fields.selection(_def_sel_hotels,string='Hotel'),
		'hotel': fields.many2one('marsans.hotel', 'Hotel', required=True, ondelete='restrict' ),
		#'room': fields.many2one('product.product', 'Room' , required=True),
		'price': fields.related('product_id','price_night',type='integer', string='Price', store=False),
		'end': fields.datetime('End Day', required=True),
		'date_i': fields.datetime('Start Day', required=True),
		'days': fields.function(_compute_days, type='integer', method=True, string='Days',store=True),
		'total': fields.function(_compute_price, type='float', method=True, string='Total',store=False),
	}
	_defaults = {
		'name':'Escala',
	}
marsans_scale()

