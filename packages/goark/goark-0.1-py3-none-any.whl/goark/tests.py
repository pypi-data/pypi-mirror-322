from tools import test_data
from main import Goark

# Usage example

def test_ingest_and_retrieveal(query, api_key, tools_array, max_outputs=2):
  client = Goark(api_key)
  client.delete_tools()
  print("Array below should be empty if this works")
  print(client.view_tools())
  print("Number below should be:" + " " + str(len(tools_array)))
  client.ingest(tools_array)
  print(len(client.view_tools()))
  answer = client.output(tools_array, query, max_outputs = max_outputs)
  print("The number below is the number of query results which should be:" + str(max_outputs))
  print(len(answer))
  print("The results should be relevant to this query:" + " " + query)
  print(answer)
  print("Done")
  client.delete_tools()

def test_multitenancy(query, api_token_1, api_token_2, tools_1, tools_2):
  ## Ingest(Also view): Ingest two, and compare both their lengths using view
  ## Output: Concept is that two different tool descriptions were loaded in. So the retrieved stuff needs to be different for the same query.
  ## Delete

  """ Ingest test, make sure that both the thing's lengths are unequal"""

  print("Initializing Ingestion test")
  tools_2 = tools_1[0:4]

  client_1 = Goark(api_token_1)
  client_2 = Goark(api_token_2)

  client_1.ingest(tools_1)
  client_2.ingest(tools_2)

  user_1 = client_1.view_tools()
  user_2 = client_2.view_tools()
  print("user_1 tool count:" + " " + str(len(user_1)))
  print("user_2 tool count:" + str(len(user_2)))
  print("#############")

  if len(user_1) != len(user_2):
    print("Test 1 Passed")
  else:
    print("Test 1 Failed")

  print("#############################")

  print("Initializing deletion test")

  client_1.delete_tools()

  user_1 = client_1.view_tools()
  user_2 = client_2.view_tools()

  if (len(user_1) == 0) and (len(user_2) != 0):
    print("Test 2 Passed")
  else:
    print("Test 2 Failed")

  client_2.delete_tools()

  print("##########################")

  print("Initializing Retrieval Test")

  client_1.ingest(tools_1)
  client_2.ingest(tools_2)

  output_1 = client_1.output(tools_1, query)
  output_2 = client_2.output(tools_2, query)

  if output_1 != output_2:
    print("Test 3 passed")
  else:
    print("Test 3 failed")
    print("here is a detailed log:")
    print(output_1)
    print(output_2)
  client_1.delete_tools()
  client_2.delete_tools()