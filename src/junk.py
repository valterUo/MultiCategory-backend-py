# nested = NestedDatatype("Person", [], [])
# primitive_name = PrimitiveDatatype("Name", "String", [])
# primitive_age = PrimitiveDatatype("Age", "Int", [])

# name_morphism = Morphism("name", nested, primitive_name)
# age_morphism = Morphism("age", nested, primitive_age)

# nested.add_morphism(name_morphism)
# nested.add_morphism(age_morphism)
# primitive_name.add_morphism(name_morphism)
# primitive_age.add_morphism(age_morphism)

# #print(nested.outGoingMorphisms[0].targetObj.inComingMorphisms)

# schemaCategory = SchemaCategory([nested, primitive_name, primitive_age], [name_morphism, age_morphism])
# #print(schemaCategory)

# readToTable("C:\\Users\\Valter Uotila\\Desktop\\demo-system-backend-Haskell\\MultiCategory\\demoData\\locationsTable.csv", ";", ["id", "address", "city", "zipCode", "country"], "id")

# graph = parseDirectedGraph("C:\\Users\\Valter Uotila\\Desktop\\demo-system-backend-Haskell\\MultiCategory\\demoData\\customerVertex.csv",
# "C:\\Users\\Valter Uotila\\Desktop\\demo-system-backend-Haskell\\MultiCategory\\demoData\\customerEdge.csv", ";", ";", ["id", "name", "creditLimit", "locationId"], ["source", "target"], 
# "id", "source", "source", "target")
# print(graph.number_of_nodes())

# printTree(ordersXML.getCollection())
# print(customersGraph)

# rdf = RDFParser("http://www.w3.org/People/Berners-Lee/card")
# rdf.printRDF()

# fn = lambda c : locationsTable.getCollection().get(dict(c).get("locationId"), "Key not in the dictonary!")
# print(fn(frozenset({('name', 'Mill'), ('id', '6'), ('locationId', '11'), ('creditLimit', '0')})))
# print(ordersXML.getCollection().getroot().findall("Order"))
# for elem in ordersXML.getCollection().getroot().findall("Order"):
#     for elem2 in elem.findall("Order_no"):
#         print(elem2.tag, elem2.text)

# fn = lambda elem :  customersGraph.findFromNodes("id", orderToCustomerKeyValuePairs.getCollection().get(elem.findall("Order_no")[0].text))

# print(customersGraph.findFromNodes("id", orderToCustomerKeyValuePairs.getCollection().get(ordersXML.getCollection().getroot().findall("./Order/Order_no")[0].text)))

# composition = located.compose(knows)

# print(composition)

# print(composition.getRelation)
# for elem in composition.getRelation()(frozenset({('id', '20'), ('locationId', '14'), ('name', 'Charlotte'), ('creditLimit', '789')})):
#     print(elem)

# composition2 = knows.compose(knows.compose(knows.compose(knows)))

# Compose the knows morphism 20 times:
# composition = knows
# for i in range(20):
#     composition = composition.compose(knows)

# for elem in composition.getRelation()(frozenset({('id', '20'), ('locationId', '14'), ('name', 'Charlotte'), ('creditLimit', '789')})):
#     print(elem)



# def t(location): return reduce(lambda xs, x: add_to_dict(xs, x, sitesTable.getCollection()[x]) if sitesTable.getCollection()[
#     x].get("locationId") == location.get("id") else xs, sitesTable.getCollection(), dict())


# print(t({'id': '12', 'address': 'Pietari Kalmin katu 5',
#          'city': '00560', 'zipCode': 'Helsinki', 'country': 'Finland'}))


#print(reduce(lambda xs, x : add_to_dict(xs, x, sitesTable.getCollection()[x]), sitesTable.getCollection(), dict()))