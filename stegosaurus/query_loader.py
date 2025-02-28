import pkg_resources

def load_query(query_name):
    sql_file = pkg_resources.resource_filename("stegosaurus", "queries.sql")
    
    with open(sql_file, "r") as file:
        query_found = False
        query = ""
        for line in file:
            if line.strip().startswith("--") and query_name in line:
                query_found = True
                continue
            if query_found:
                if line.strip() == "":
                    break
                query += line
    return query.strip() if query else None
