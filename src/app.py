from SchemaCategory.Objects.NestedDatatype import NestedDatatype
from SchemaCategory.Objects.PrimitiveDatatype import PrimitiveDatatype
from SchemaCategory.Morphisms.Morphism import Morphism

nested = NestedDatatype("Person", [], [])
primitive_name = PrimitiveDatatype("Name", "String", [])
primitive_age = PrimitiveDatatype("Age", "Int", [])

name_morphism = Morphism(nested, primitive_name)
age_morphism = Morphism(nested, primitive_age)

nested.add_morphism(name_morphism)
nested.add_morphism(age_morphism)
primitive_name.add_morphism(name_morphism)
primitive_age.add_morphism(age_morphism)

print(nested.outGoingMorphisms[0].targetObj.inComingMorphisms)