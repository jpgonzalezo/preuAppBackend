from datetime import datetime
from mongoengine.fields import ReferenceField, StringField, DateTimeField, FloatField, IntField, ListField, EmbeddedDocumentField, Document, DBRef

def get_value(value):
    if isinstance(value, datetime):
        return value.isoformat()
    elif isinstance(value, DBRef):
        return str(value.id)
    elif isinstance(value, list):
        for index in range(len(value)):
            value[index] = get_value(value[index])
        return value
    elif isinstance(value, EmbeddedDocumentField):
        return mongo_to_dict(value)
    else:
        return str(value) + " ->  "+ str(type(value))

def mongo_to_dict(obj):
    data = obj._data
    for key, value in data.items():

        if key is 'id':
            data[key] = str(value)
        else:
            data[key] = get_value(value)
        
        

        # data = obj._data[field_name]
        # print(data)

        # if isinstance(obj._fields[field_name], DateTimeField):
        #     return_data.append((field_name, str(data.isoformat())))
        # elif isinstance(obj._fields[field_name], StringField):
        #     return_data.append((field_name, str(data)))
        # elif isinstance(obj._fields[field_name], FloatField):
        #     return_data.append((field_name, float(data)))
        # elif isinstance(obj._fields[field_name], IntField):
        #     return_data.append((field_name, int(data)))
        # elif isinstance(obj._fields[field_name], ListField):
        #     return_data.append((field_name, data))
        # elif isinstance(obj._fields[field_name], EmbeddedDocumentField):
        #     return_data.append((field_name, mongo_to_dict(data)))
        # elif isinstance(obj._fields[field_name], DBRef):
        #     return_data.append((field_name, str(data)))

    return data