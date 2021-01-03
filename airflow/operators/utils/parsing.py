import re

def detect_schema_tables(query, schema):
    query = re.sub(re.compile(r'\/\*.*\*\/', re.MULTILINE), "", query)
    query = re.sub("--.*\n", "", query)
    query = re.sub(re.compile(r'[\s]+', re.MULTILINE), " ", query)

    regex = "[^a-z\d_\.]" + schema + "\.([a-z\d_\.]*)"
    query_tables = re.finditer(regex, query)
    ret = list(set(m.group(1) for m in query_tables))

    return ret

def detect_dependencies(query, schemas):
    deps = []
    for schema in schemas:
        deps.append(detect_schema_tables(query, schema))
    return [dep for schema_deps in deps for dep in schema_deps]
