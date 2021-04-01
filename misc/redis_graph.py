import redis
from redisgraph import Node, Edge, Graph

def print_res(result):
	# Iterate through resultset, skip header row at position 0
	for record in result.result_set:
		person_name = record[0]
		person_age = record[1]
		person_status = record[2]
		country_name = record[3]
		print(('Name: {}\tAge: {}\tStatus: {}\tCountry: {}'.format(person_name, person_age,
			person_status, country_name)).expandtabs(10))

def main():
	r = redis.Redis(decode_responses=True)
	r.delete('social')
	redis_graph = Graph('social', r)

	john = Node(label='person', properties={'name':'John Doe', 'age': 33, 'gender':'male', 'status': 'single'})
	redis_graph.add_node(john)
	japan = Node(label='country', properties={'name':'Japan'})
	redis_graph.add_node(japan)
	edge_john = Edge(john, 'visited', japan, properties={'purpose':'pleasure'})
	redis_graph.add_edge(edge_john)

	pearl = Node(label='person', properties={'name':'Pearl White', 'age':25, 'gender':'female', 'status':'married'})
	redis_graph.add_node(pearl)
	australia = Node(label='country', properties={'name':'Australia'})
	redis_graph.add_node(australia)
	edge_pearl = Edge(pearl, 'visited', australia, properties={'purpose':'business'})
	redis_graph.add_edge(edge_pearl)

	mary = Node(label='person', properties={'name':'Mary Mueller', 'age':45, 'gender':'divers', 'status':'divers'})
	redis_graph.add_node(mary)
	germany = Node(label='country', properties={'name':'Germany'})
	redis_graph.add_node(germany)
	edge_mary = Edge(mary, 'visited', germany, properties={'purpose':'business'})
	redis_graph.add_edge(edge_mary)

	redis_graph.commit()

	for i in ['pleasure', 'business']:
		print('==== Purpose: {} ===='.format(i))
		query = '''MATCH (p:person)-[v:visited {{purpose:"{}"}}]->(c:country) 
			RETURN p.name, p.age, p.status, c.name'''.format(i)
		result = redis_graph.query(query)
		print_res(result)

if __name__ == '__main__':
    exit(main())
