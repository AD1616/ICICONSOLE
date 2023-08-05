def getAll():
    return "MATCH(n) RETURN n"

def getOne(id):
    return "MATCH(n) WHERE n.id = '" + id + "' RETURN n"

def getOneByType(type):
    return "MATCH(n:" + type + ") RETURN n"

def allProperty(property):
    return "MATCH(n) RETURN n." + property

def allPropertiesForNode(id):
    return "MATCH(n) WHERE n.id = '" + id + "' RETURN keys(n)"

def createSingularNode(label, name):
    return "CREATE (n:" + label + " {name: '" + name + "'})"

def deleteSingularNode(id):
    return "MATCH(n) WHERE n.id = '" + id + "' DELETE n"

def reverseRelationshipDirection(label1, rel_label, label2):
    return f"""MATCH (n:{label1})-[rel:{rel_label}]->(m:{label2})
    CALL apoc.refactor.invert(rel)
    yield input, output
    RETURN input, output"""