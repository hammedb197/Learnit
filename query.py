from neo4j import GraphDatabase


def sendToNeo4j(query, **kwarg):
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'graph'))
    # driver = GraphDatabase.driver('bolt://100.25.164.167:33452', auth=('neo4j', 'magazines-chases-numerals'))
    db = driver.session()
    consumer = db.run(query, **kwarg) 
    
    
query = """
LOAD CSV WITH HEADERS FROM  "file:///data.csv" AS row
MERGE (name:NAME {text:row.nameLabel})
MERGE (image:IMAGE {text: coalesce(row.image, " ")})
MERGE (placeofburial:PLACEOFBURIAL {text: coalesce(row.placeofburial, " ")})
MERGE (birth:BIRTHPLACE_AR {text: coalesce(row.birthplacearabic, " ")})
MERGE (birthplacearabic: BIRTHPLACE_AR {text: coalesce(row.birthplacearabic, " ")})
MERGE (placeofdeath:PLACEOFDEATH {text:coalesce(row.placeofdeath, " ")})
MERGE (placeofdeatharabic: PLACEOFDEATH_AR {text: coalesce(row.placeofdeatharabic, " ")})
MERGE (spouse:SPOUSE {text: coalesce(row.spouse, " ")})
MERGE (spouse_ar:SPOUSE_AR {text: coalesce(row.spousearabic, " ")})
MERGE (children:CHILDREN {text: coalesce(row.children, " ")})
MERGE (childrenarabic: CHILDREN_AR_NAME {text: coalesce(row.childrenarabic, " ")})
MERGE (mother: MOTHER {text: coalesce(row.mother, " ")})
MERGE (dateofbirth: DATEOFBIRTH {text: coalesce(dateofbirth, " ")})

with name, image, placeofburial, birth, birthplacearabic, placeofdeath, placeofdeatharabic, spouse, spouse_ar,  children, childrenarabic, mother, dateofbirth
where size(image.text) > 1 or size(placeofburial.text) > 1 or size(birth.text) > 1 or size(birthplacearabic.text) > 1 or size(placeofdeath.text) > 1 or size(placeofdeatharabic.text) > 1 or size(spouse.text) > 1 or size(spouse_ar.text) > 1 or size(children.text) > 1 or size(childrenarabic.text) > 1 or size(mother.text) > 1 or size(dateofbirth.text) > 1
MERGE (name)<-[:IMAGE_OF {text:"IMAGE OF"}]-(image)
MERGE (name)-[:BURIED_AT {text:"BURIED AT"}]->(placeofburial)
MERGE (name)-[:BIRTH_PLACE {text: "BIRTH PLACE"}]->(birth)
MERGE (name)-[:BIRTH_PLACE_ARABIC {text: "BIRTH PLACE ARABIC"}]->(birthplacearabic)
MERGE (name)-[:PLACE_OF_DEATH {text: "PLACE OF DEATH"}]->(placeofdeath)
MERGE (name)-[:PLACE_OF_DEATH_ARABIC {text: "PLACE OF DEATH ARABIC"}]->(placeofdeatharabic)
MERGE (name)-[:SPOUSE {text:"MARRIED TO"}]->(spouse)
MERGE (name)-[:SPOUSE_ARABIC {text:"MARRED TO"}]->(spouse_ar)
MERGE (name)<-[:CHILD_OF {text:"CHILD OF"}]-(children)
MERGE (name)<-[:CHILD_OF_ARABIC {text:"CHILD OF"}]-(childrenarabic)
MERGE (name)<-[:MOTHER {text:"MOTHER OF"}]-(mother)
MERGE (name)-[:DATE_OF_BIRTH {text:"DATE OF BITH"}]->(dateofbirth)
//MERGE (name)-[:]-()

"""   
    
    
sendToNeo4j(query)
    
    
