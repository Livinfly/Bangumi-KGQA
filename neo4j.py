from const import neo4j_const
from py2neo import Graph, Node, Relationship

uri, usr, psw = neo4j_const.values()
graph = Graph(uri, auth=(usr, psw))

graph.delete_all()