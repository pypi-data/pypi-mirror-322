def distill(tools, framework="langchain"):
    """ This function takes in an array of tools(of any framework) and distills it down to an array of descriptions.

    validate:

    Distillation is basically just taking tools and then outputting the following:
    {
        index: 0,
        tool_name: get_github_token,
        description: this tool gets the github auth token,
        schema: {a: {int}, b: {string}}
    }

    In the future: Make sure the passed object is of type tool.
    """
    output_array = []

    def check_attributes(instance, required_attributes):
        missing_attributes = [attr for attr in required_attributes if not hasattr(instance, attr)]
        if missing_attributes:
            return (False, missing_attributes)
        return (True, "No missing attributes")

    if framework == "langchain":
        ##First check if each of them have the tool_name, schema and description and then add the distillation to the array.
        counter = 0
        for tool in tools:
            attributes_check = check_attributes(tool, ["name", "description", "args"])
            if attributes_check[0] == False:
                raise AttributeError(f"Please check tool number: " + str(counter) + " in inputted array. It is missing the following attributes: " + str(attributes_check[1]))
                return
            output_array.append(
                {
                    "index": counter,
                    "tool_name": tool.name,
                    "tool_description": tool.description,
                    "tool_args": tool.args
                }
            )
            counter += 1
    return output_array

def output_to_tools(tools, output_results, max_outputs=2):
    """Converts the output to tools that the user can use in their preferred framework.
    Parse through relevant tools and return the top tools based on max_outputs"""
    
    arr_indexes = []
    for i, result in enumerate(output_results):
        if len(arr_indexes) >= max_outputs:
            break
        arr_indexes.append(result['index'])
    
    # Return the corresponding tools using the indexes
    print("these are the tools that are passed")
    print(tools)
    print("Here ^^")
    relevant_tools = [tools[arr_index] for arr_index in arr_indexes]
    return relevant_tools
