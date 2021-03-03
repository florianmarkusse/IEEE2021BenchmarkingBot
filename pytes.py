testList = [
    "title",
    "createdAt",
    "participants {{ totalCount }}",
    "number"
]

testString = ""

for item in testList:
    testString += (item + "\n")

string = """
{{
    ... on PullRequest {{
        {attributes}
    }}
}}
""".format(attributes=testString)

print(string)
