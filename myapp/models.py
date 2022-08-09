# from django.db import models

#$$$$$$$$$$$$$$$$$$$$$$$$$$$Reference$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# # Create your models here.
#from neomodel import (StructuredNode, StringProperty,
# IntegerProperty,UniqueIdProperty, RelationshipTo)

# # Create your models here.


#class City(StructuredNode):
#     code = StringProperty(unique_index=True, required=True)
#     name = StringProperty(index=True, default="city")

#class Person(StructuredNode):
#     uid = UniqueIdProperty()
#     name = StringProperty(unique_index=True)
#     age = IntegerProperty(index=True, default=0)

#     # Relations :
#     city = RelationshipTo(City, 'LIVES_IN')
#     friends = RelationshipTo('Person','FRIEND')

#$$$$$$$$$$$$$$$$$$$$$$$$$$$Reference$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#!/usr/bin/env python
# coding: utf-8


from neomodel import (StructuredNode, StructuredRel, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, RelationshipFrom)



class Page(StructuredNode):
    
    """
    This class specifies node properties and relation

    Inputs:
        page_uid: unique identification for node
        page_name: name of the node
        page_url: url of the node
        relation: connection between the node

    Returns:
        None

    Output:
        Creation of node in Neo4j
    """

    page_uid = UniqueIdProperty()
    page_name = StringProperty(unique_index=True)
    page_url = StringProperty(index=True, default=" ")
    page_html = StringProperty(index=True, default=" ")    

    #Relations
    relation = RelationshipTo('Page', 'LINKED_TO')
    relationf = RelationshipFrom('Resultpage', 'LINKED_TO')


class Resultpage(StructuredNode):
    
    """
    This class specifies node properties, relation 
    and attributes

    Inputs:
        page_uid: unique identification for node
        page_name: name of the node
        page_url: url of the node
        relation: connection between the node

    Returns:
        None

    Output:
        Creation of node in Neo4j
    """

    resultpage_uid = UniqueIdProperty()
    resultpage_name = StringProperty(unique_index=True)
    resultpage_url = StringProperty(index=True, default=" ")
    resultpage_adult_occupant = StringProperty(index=True, default=" ") 
    resultpage_child_occupant = StringProperty(index=True, default=" ")    
    resultpage_vulnerable_roadusers = StringProperty(index=True, default=" ")    
    resultpage_safety_assist = StringProperty(index=True, default=" ")    
    resultpage_tested_model = StringProperty(index=True, default=" ")    
    resultpage_body_type = StringProperty(index=True, default=" ")    
    resultpage_year_of_publication = StringProperty(index=True, default=" ")    
    resultpage_kerb_weight = StringProperty(index=True, default=" ")    
    resultpage_vin = StringProperty(index=True, default=" ")    
    resultpage_class = StringProperty(index=True, default=" ")
    resultpage_test_image_url = StringProperty(index=True, default=" ")
    resultpage_adultoccupant_image_url = StringProperty(index=True, default=" ")
    resultpage_pedestrain_image_url = StringProperty(index=True, default=" ")
    resultpage_safety_image_url = StringProperty(index=True, default=" ")




    #Relations
    relationf = RelationshipTo('Page', 'LINKED_TO')
    relation = RelationshipFrom('Resultpage', 'LINKED_TO')



    


