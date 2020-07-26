from flask import Flask, render_template, request
from neo4j import GraphDatabase



def sendToNeo4j(query, **kwarg):
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'graph'))
    # driver = GraphDatabase.driver('bolt://100.25.164.167:33452', auth=('neo4j', 'magazines-chases-numerals'))
    db = driver.session()
    consumer = db.run(query, **kwarg) 

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/search', methods=["POST"])
def search():
    if request.method == 'POST':
        text = request.form['text']
        query = """
        MATCH (a {text:$text})-[r]-(b)
        return a, b
        //CALL apoc.path.subgraphAll(a, {maxLevel:1}) YIELD nodes, relationships
        //unwind relationships as rel
        //unwind nodes as node
        //return collect(distinct properties(node)) as nodes, collect(Distinct {source:id(startNode(rel)), target:id(endNode(rel))}) as links

        """
        profile =  sendToNeo4j(query, text=text)
        print(profile)


        # query = """

        # """
        graph = ""



        return render_template('result.html', profile=profile, graph=graph)


if __name__ == "__main__":
    app.run()