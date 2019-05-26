from flask_admin.contrib.mongoengine import ModelView as MV
from datetime import datetime

def date_time_formatter(view, context, model, name):
    fecha = model[name]
    return u"%s-%s-%s" % (fecha.year, fecha.month, fecha.day)

class ModelView(MV):
    can_export = True
    column_formatters = {
        'created': date_time_formatter,
        'updated': date_time_formatter
    }
    can_view_details = True
    column_labels = dict(
        created=u"Creado",
        updated=u"Editado"
    )
    