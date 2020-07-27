from flask import Flask, render_template, request
from neo4j import GraphDatabase


def split_space(string):
    return " ".join(string.split("_")).capitalize()

def sendToNeo4j(query, **kwarg):
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'graph'))
    # driver = GraphDatabase.driver('bolt://100.25.164.167:33452', auth=('neo4j', 'magazines-chases-numerals'))
    db = driver.session()
    consumer = db.run(query, **kwarg) 
    # print(consumer)
    return [dict(i) for i in consumer]

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/search', methods=["POST"])
def search():
    if request.method == 'POST':
        text = request.form['text']
        # query = """
        # MATCH (a {text:$text})-[r]-(b)
        # //return a.text, b.text
        # CALL apoc.path.subgraphAll(a, {maxLevel:1}) YIELD nodes, relationships
        # unwind relationships as rel
        # unwind nodes as node
        # return collect(distinct properties(node)) as nodes, collect(Distinct {source:id(startNode(rel)), target:id(endNode(rel))}) as links

        # """
        query = """
        MATCH (a {text:$text})-[r]-(b)
        with a, b
        where size(b.text) > 1
        return a.text as name, b.text as relate, b.category as category
        """
        print(text)
        profile =  sendToNeo4j(query, text=text)



        query = """
        match path =  (node {text:$text})-[relationship]-(b)
        unwind nodes(path) as p 
        unwind relationships(path) as r
        with p, path, r
        where size(p.text) > 1
        with p, path, r
        where r.text <> "DATE OF BITH"

        return collect(distinct properties(p)) as nodes, collect(DISTINCT {source: id(startNode(r)), target: id(endNode(r))}) as links
        """
        graph = sendToNeo4j(query, text=text)



        return render_template('result.html', profile=profile, graph=graph)


if __name__ == "__main__":
    app.jinja_env.filters['split_space'] = split_space
    app.run(debug=True)