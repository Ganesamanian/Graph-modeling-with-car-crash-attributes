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
    UniqueIdProperty, RelationshipTo, RelationshipFrom, JSONProperty)



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
    resultpage_tested_model = StringProperty(index=True, default=" ")    
    resultpage_body_type = StringProperty(index=True, default=" ")    
    resultpage_year_of_publication = StringProperty(index=True, default=" ")    
    resultpage_kerb_weight = StringProperty(index=True, default=" ")    
    resultpage_vin = StringProperty(index=True, default=" ")    
    resultpage_class = StringProperty(index=True, default=" ")
    resultpage_test_image_url = StringProperty(index=True, default=" ")
    resultpage_adultoccupant = StringProperty(index=True, default=" ")
    resultpage_childoccupant = StringProperty(index=True, default=" ")
    resultpage_pedestrain = StringProperty(index=True, default=" ")
    resultpage_safety_assist = StringProperty(index=True, default=" ")




    #Relations
    relationf = RelationshipTo('Page', 'LINKED_TO')
    relation = RelationshipFrom('Resultpage', 'LINKED_TO')
    relationclass = RelationshipTo('Class', 'INCLUDE_VEHICLE')


class Class(StructuredNode):
    
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

    class_uid = UniqueIdProperty()
    class_name = StringProperty(unique_index=True)


    #Relations
    relation = RelationshipTo('Page', 'VEHICLE_CLASS')


class Vehicle(StructuredNode):
    
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

    vehicle_uid = UniqueIdProperty()
    vehicle_name = StringProperty(unique_index=True)
    vehicle_url = StringProperty(index=True, default=" ")
    vehicle_uid = UniqueIdProperty()
    vehicle_body_type = StringProperty(index=True, default=" ")    
    vehicle_year_of_publication = StringProperty(index=True, default=" ")    
    vehicle_kerb_weight = StringProperty(index=True, default=" ")    
    vehicle_vin = StringProperty(index=True, default=" ")
    vehicle_test_image_url = StringProperty(index=True, default=" ")


    #Relations
    relation = RelationshipTo('Class', 'INCLUDE_VEHICLE')


class Ratingproperty(StructuredRel):

    aop_ratings = StringProperty()
    cop_ratings = StringProperty()
    vru_ratings = StringProperty()
    sas_ratings = StringProperty()



class Aop(StructuredNode):
    
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

    aop_uid = UniqueIdProperty()
    aop_name = StringProperty(index=True, default=" ")         

    


    #Relations
    relation = RelationshipTo('Vehicle', 'RATING', model= Ratingproperty)


class Cop(StructuredNode):
    
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

    cop_uid = UniqueIdProperty()
    cop_name = StringProperty(index=True, default=" ")         

    


    #Relations
    relation = RelationshipTo('Vehicle', 'RATING', model= Ratingproperty)




class Sas(StructuredNode):
    
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

    sas_uid = UniqueIdProperty()
    sas_name = StringProperty(index=True, default=" ")         

    


    #Relations
    relation = RelationshipTo('Vehicle', 'RATING', model= Ratingproperty)



class Vru(StructuredNode):
    
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

    vru_uid = UniqueIdProperty() 
    vru_name = StringProperty(index=True, default=" ")         

    


    #Relations
    relation = RelationshipTo('Vehicle', 'RATING', model= Ratingproperty)


class Prtcl(StructuredNode):
    
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

    prtcl_uid = UniqueIdProperty() 
    prtcl_name = StringProperty(index=True, default=" ")         
    prtcl_url = StringProperty(index=True, default=" ")
    


    #Relations
    relation1 = RelationshipTo('Cop', 'DEFINE_AS')
    relation2 = RelationshipTo('Aop', 'DEFINE_AS')
    relation3 = RelationshipTo('Sas', 'DEFINE_AS')
    relation4 = RelationshipTo('Vru', 'DEFINE_AS')
    relation5 = RelationshipFrom('Year', 'From')
    relation6 = RelationshipFrom('Page', 'LINKED_TO')




class Year(StructuredNode):
    
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

    year_uid = UniqueIdProperty()
    year_name = StringProperty(unique_index=True)


    # #Relations
    relation = RelationshipTo('Vehicle', 'PUBL_IN')

class Attr(StructuredNode):

    uid = UniqueIdProperty()
    attr_name = StringProperty(unique_index=True)
    attr_spec = JSONProperty()
    
    attr_prtcl = RelationshipTo('Prtcl', 'ATTR_PRTCL')






    


