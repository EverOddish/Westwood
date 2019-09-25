import glob
import os
from lxml import etree

NS = 'http://www.w3.org/2001/XMLSchema'
NS_PREFIX = '{' + NS + '}'

django_models_path = os.path.join('django-westwood', 'westwood', 'models.py')

if os.path.exists(django_models_path):
    print(django_models_path + ' already exists! Overwriting...\n')

with open(django_models_path, 'w') as models_file:
    models_file.write('from django.db import models\n\n')

    models = {}

    for schema_file in glob.glob(os.path.join('xsd', '*.xsd')):
        try:
            root = etree.parse(schema_file)
            print('Processing ' + schema_file)

            for element in root.iter(NS_PREFIX + 'element'):
                # If this xs:element has children, treat it as a complexType
                if len(list(element)) > 0:
                    class_name = element.get('name')
                    if class_name:
                        # Convert the name to CamelCase
                        class_name = class_name.replace('_', ' ').title().replace(' ', '')

                        # If there is a single child xs:element with minOccurs=1, treat it as a list
                        child_elements = element.xpath(".//xs:element[@minOccurs='1']", namespaces={'xs': NS})
                        if len(child_elements) == 1:
                            class_name += 'ListElement'

                        # Track this model if we haven't seen it yet
                        if None == models.get(class_name):
                            content = ''

                            # Find all the simple xs:elements to describe the model's fields
                            child_elements = element.xpath(".//xs:element[not(@minOccurs)]", namespaces={'xs': NS})
                            for field in child_elements:
                                name = field.get('name')
                                if name:
                                    content += '    ' + name + ' = models.' 
                                    if field.get('type') == 'xs:string':
                                        content += 'CharField(max_length=500)'
                                    elif field.get('type') == 'xs:positiveInteger':
                                        content += 'IntegerField(default=0)'
                                    elif field.get('type') == 'xs:date':
                                        content += 'DateTimeField()'
                                    else:
                                        # Assume string type by default. This includes types like Westwood enumerations.
                                        content += 'CharField(max_length=500)'
                                    content += '\n'
                                else:
                                    ref = field.get('ref')
                                    if ref:
                                        print('ref')

                            models[class_name] = content

        except etree.XMLSyntaxError:
            print('INVALID: ' + schema_file)

    print('\nModels:\n')

    for name in models.keys():
        print(name)
        models_file.write('class ' + name + '(models.Model):\n')
        models_file.write(models[name] + '\n')
