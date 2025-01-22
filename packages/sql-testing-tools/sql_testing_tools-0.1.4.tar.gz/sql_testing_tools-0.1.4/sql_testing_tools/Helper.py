import os
from . import BaseAccess as Ba


try:
    import sqlparse
except ImportError:
    print("Trying to Install required module: sqlparse\n")
    os.system('pip install sqlparse')
    import sqlparse


try:
    import requests
except ImportError:
    print("Trying to Install required module: requests\n")
    os.system('pip install requests')
    import requests

from sqlparse.sql import Identifier, IdentifierList, Where, Comparison, Function, Parenthesis
from sqlparse.tokens import Keyword, DML, Name, Wildcard


def normalizeSQLQuery(query, baseDict):
    try:
        query = query.replace("\"", "'")
        parsed = sqlparse.parse(query)[0]
        parsed.tokens = [token for token in parsed.tokens if not token.is_whitespace]
    except Exception as e:
        raise Exception(f"\nSyntax-Fehler in der SQL-Abfrage.")

    formatted_query = []
    alias_map = {}

    def process_identifier(identifier, alias_map, baseDict: dict):
        if isinstance(identifier, Identifier):
            if identifier.get_real_name() and identifier.get_parent_name() and identifier.get_parent_name().lower() in alias_map.keys():
                return f"{alias_map[identifier.get_parent_name().lower()].lower()}.{identifier.get_real_name().lower()}"
            elif identifier.get_real_name():
                tables = findTableForColumn(baseDict, identifier.get_real_name(), alias_map.keys())
                if len(tables) == 1:
                    alias_map[tables[0].lower()] = tables[0]
                    return f"{tables[0].lower()}.{identifier.get_real_name().lower()}"
                else:
                    return f"{identifier.get_real_name().lower()}"
        return str(identifier)

    def process_select(select, alias_map, insideFunction=False):
        select_tokens = []
        for token in select.tokens:
            if isinstance(token, IdentifierList):
                for identifier in token.get_identifiers():
                    select_tokens.append(f"{process_identifier(identifier, alias_map, baseDict).lower()} as {identifier.get_real_name().lower()}")
            elif isinstance(token, Identifier):
                if insideFunction:
                    select_tokens.append(process_identifier(token, alias_map, baseDict).lower())
                else:
                    select_tokens.append(f"{process_identifier(token, alias_map,  baseDict).lower()} as {token.get_real_name().lower()}")
            elif isinstance(token, Function):
                #select_tokens.append(f"{token.get_name().lower()}({process_identifier(token.get_parameters(), alias_map, baseDict).lower()})")
                for par in token.tokens:
                    if isinstance(par, Identifier):
                        select_tokens.append(par.get_name().lower()+"(")
                    if isinstance(par, Parenthesis):
                        select_tokens[-1] += process_select(par, alias_map, True)+") as funcResult" 
            elif token.ttype is Wildcard:
                select_tokens.append("*")
            else:
                continue
        select_tokens.sort()
        return ",".join(select_tokens)

    def process_from(from_, alias_map):
        from_tokens = []
        if hasattr(from_, 'tokens'):
            for token in from_.tokens:
                if isinstance(token, IdentifierList):
                    for identifier in token.get_identifiers():
                        alias_map[identifier.get_real_name().lower()] = identifier.get_alias() or identifier.get_real_name()
                        from_tokens.append(f"{identifier.get_real_name().lower()} {alias_map[identifier.get_real_name().lower()].lower()}")
                elif isinstance(token, Identifier):
                    alias_map[token.get_real_name().lower()] = token.get_alias() or token.get_real_name()
                    from_tokens.append(f"{token.get_real_name().lower()} {alias_map[token.get_real_name().lower()].lower()}")
                elif token.ttype is not None and token.ttype is Name:
                    alias_map[token.value.lower()] = token.value.lower()
                    from_tokens.append(f"{token.value.lower()} {alias_map[token.value.lower()].lower()}")
                else:
                    continue
        from_tokens.sort()
        return ",".join(from_tokens)

    def process_groupby(groupby_, alias_map):
        groupby_tokens = []
        if(isinstance(groupby_, Identifier)):
            groupby_tokens.append(process_identifier(groupby_, alias_map, baseDict).lower())
        elif isinstance(token, IdentifierList):
            for identifier in token.get_identifiers():
                groupby_tokens.append(process_identifier(identifier, alias_map, baseDict).lower())
        groupby_tokens.sort()
        return ",".join(groupby_tokens)

    def process_condition(token, alias_map, baseDict):
        left, operator, right = [t for t in token.tokens if not t.is_whitespace]

        flipAllowed = True
        leftLiteral = False
        rightLiteral = False

        if is_value(right):
            flipAllowed = False
            rightLiteral = True

        if is_value(left):
            left, right = right, left
            if operator.value == ">":
                operator.value = "<"
            elif operator.value == "<":
                operator.value = ">"
            leftLiteral = rightLiteral
            rightLiteral = True
            flipAllowed = False

        left = process_identifier(left, alias_map, baseDict)
        right = process_identifier(right, alias_map, baseDict)

        if flipAllowed and left.lower() >= right.lower():
            left, right = right, left
            if operator.value == ">":
                operator = "<"
            elif operator.value == "<":
                operator = ">"

        return f"{left if leftLiteral else left.lower()} {operator} {right if rightLiteral else right.lower()}"

    def is_value(token):
        return token.ttype in (sqlparse.tokens.Token.Literal.Number.Integer,
                               sqlparse.tokens.Token.Literal.Number.Float,
                               sqlparse.tokens.Token.Literal.String.Single,
                               sqlparse.tokens.Token.Literal.String.Symbol)

    def process_paranthesis(parenthesis, alias_map, baseDict):
        toks = []

        bracketsRequired = True


        for token in parenthesis.tokens:
            if isinstance(token, Comparison):
                toks.append(process_condition(token, alias_map, baseDict))
            elif isinstance(token, Parenthesis):
                toks.append(process_paranthesis(token, alias_map, baseDict))

            elif token.value == '(':
                toks.append(token.value)
            else:
                continue
        x = parenthesis.flatten()
        return " ".join(toks)

    def process_where(where, alias_map, baseDict):
            conditions = []
            current_condition = []

            for token in where.tokens:
                if token.is_whitespace or (token.ttype is Keyword and token.value.upper() == "WHERE"):
                    continue

                if token.ttype is Keyword and token.value.upper() in ('AND', 'OR'):
                    if current_condition:
                        conditions.append(''.join(str(t) for t in current_condition).strip())
                        current_condition = []
                    conditions.append(token.value.upper())
                elif isinstance(token, Comparison):
                    current_condition.append(process_condition(token, alias_map, baseDict))
                elif isinstance(token, Parenthesis):
                    current_condition.append(process_paranthesis(token, alias_map, baseDict))
                else:
                    current_condition.append(token)

            if current_condition:
                conditions.append(''.join(str(t) for t in current_condition).strip())

            sorted_conditions = []
            current_group = []
            last_connector = ""

            if "OR" not in conditions:
                for condition in conditions:
                    if condition == 'AND':
                        pass
                    else:
                        current_group.append(condition)

                if current_group:
                    sorted_conditions.extend(sorted(current_group))

                return " AND ".join(sorted_conditions)
            else:
                return " ".join(conditions)

                where_index = query.upper().find('WHERE')
                normalized_query = query[:where_index + 5] + ' ' + ' '.join(sorted_conditions)

    def process_where_xx(where, alias_map, baseDict):
        where_tokens = []
        for token in where.tokens:

            if isinstance(token, Comparison):
                left, operator, right = [t for t in token.tokens if not t.is_whitespace]
                left = process_identifier(left, alias_map, baseDict)
                right = process_identifier(right, alias_map, baseDict)
                if left.lower() >= right.lower():
                    left, right = right, left
                    if operator.value == ">":
                        operator = "<"
                    elif operator.value == "<":
                        operator = ">"

                where_tokens.append(f"{left.lower()} {operator} {right.lower()}")
            elif token.ttype is Keyword:
                where_tokens.append(token.value.upper())
            elif token.is_whitespace or (token.ttype is Keyword and token.value.upper() == "WHERE"):
                continue
            else:
                where_tokens.append(str(token))
        return " ".join(where_tokens)

    # First pass to process FROM clause and populate alias_map
    for token in parsed.tokens:
        if token.is_whitespace:
            continue
        elif token.ttype is Keyword and token.value.upper() == 'FROM':
            formatted_query.append('FROM')
            pass
        elif isinstance(token, Identifier) and formatted_query and formatted_query[-1] == 'FROM':
            il = IdentifierList([token])
            formatted_query.append(process_from(il, alias_map))
            process_from(il, alias_map)
        elif isinstance(token, IdentifierList) and formatted_query and formatted_query[-1] == 'FROM':
            formatted_query.append(process_from(token, alias_map))
            process_from(token, alias_map)

    formatted_query = []

    # Second pass to process SELECT and WHERE clauses
    for token in parsed.tokens:
        if token.is_whitespace:
            continue
        elif token.ttype is DML and token.value.upper() == 'SELECT':
            formatted_query.append('SELECT')
        elif token.ttype is Keyword and token.value.upper() == 'FROM':
            formatted_query.append('FROM')  
        elif token.ttype is Keyword and token.value.upper() == 'GROUP BY':
            formatted_query.append('GROUP BY')
        elif (isinstance(token, IdentifierList) or isinstance(token, Identifier)) and formatted_query and formatted_query[-1] == 'FROM':
            formatted_query.append(process_from(token, alias_map))
        elif (isinstance(token, IdentifierList) or isinstance(token, Identifier)) and formatted_query and formatted_query[-1] == 'GROUP BY':
            formatted_query.append(process_groupby(token, alias_map))
        elif isinstance(token, Where):
            formatted_query.append('WHERE')
            formatted_query.append(process_where(token, alias_map, baseDict))
        elif formatted_query and formatted_query[-1] == 'SELECT' and (isinstance(token, IdentifierList) or isinstance(token, Function) or isinstance(token, Identifier)):
            if isinstance(token, Function):
                token = IdentifierList([token])
            formatted_query.append(process_select(token, alias_map))
        else:
            formatted_query.append(str(token))

    return " ".join(formatted_query)


def findTableForColumn(data_dict, target_value, relevantTables):
    l = []
    for key, value_list in data_dict.items():
        if key.lower() in relevantTables:
            for sublist in value_list:
                if sublist and sublist[0].lower() == target_value.lower():
                    l.append(key)
    if len(l) == 0:
        for key, value_list in data_dict.items():
            for sublist in value_list:
                if sublist and sublist[0].lower() == target_value.lower():
                    l.append(key)
    return l


def getTableScheme(table_name: str, tableDict: dict):
    tab = tableDict[table_name]

    # Format the schema
    schema = "(" + ",".join([f"{col[0]}:{col[1]}" for col in tab]) + ")"
    return schema

def getCosetteKeyFromFile():
    try:
        with open("cosette_apikey.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "NOKEY"

def buildAndSendCosetteRequest(baseDict, sql, sol):

    err = ""
    for i in range(2):
        try:
            apiKey=getCosetteKeyFromFile()


            schema = ""
            for tab in baseDict.keys():
                schema += f"schema sch{tab}{getTableScheme(tab, baseDict)};\n"
            for tab in baseDict.keys():
                schema += f"table {tab}(sch{tab});\n"

            q1 = "query q1\n`"+sql+"`;\n"
            q2 = "query q2\n`"+sol+"`;\n"

            cosette = "-- random Kommentar\n" + schema + q1 + q2 + "verify q1 q2;\n"
            print(cosette)

            r = requests.post("https://demo.cosette.cs.washington.edu/solve",data={"api_key": apiKey, "query": cosette}, verify=False)

            print(r.text)
            return (r.json()['result'],r.text)
            #return r.json()['result']

        except Exception as e:
            err = str(e)
    return ("ERR", err)


def checkColumns(sqlPath, solPath):
    bd = Ba.getTableDict()
    sql = normalizeSQLQuery(Ba.getSQLFromFile(sqlPath), bd)
    sol = normalizeSQLQuery(Ba.getSQLFromFile(solPath), bd)

    if("SELECT" in sql and "FROM" in sql):
        start = str.find(sql, "SELECT")
        end = str.find(sql, "FROM")
        submission = str.strip(sql[start:end])
        print("'"+submission+"'")

        start = str.find(sol, "SELECT")
        end = str.find(sol, "FROM")
        solution = str.strip(sol[start:end])
        print("'"+solution+"'")

        if submission == solution:
            return ""
    return "Ausgegebene Spalten sind nicht korrekt (oder nicht automatisch überprüfbar)."


def checkTables(sqlPath, solPath):
    bd = Ba.getTableDict()
    sql = normalizeSQLQuery(Ba.getSQLFromFile(sqlPath), bd)
    sol = normalizeSQLQuery(Ba.getSQLFromFile(solPath), bd)

    if("SELECT" in sql and "FROM" in sql):
        endFromKeywords = ["WHERE", "GROUP", "ORDER", "LIMIT", ";"]

        start = str.find(sql, "FROM")
        end = -1


        for keyword in endFromKeywords:
            if(str.find(sql, keyword) != -1):
                end = str.find(sql, keyword)
                break
        if(end == -1):
            end = len(sql)

        submission = str.strip(sql[start:end])
        print("'"+submission+"'")

        start = str.find(sol, "FROM")
        end = -1
        
        for keyword in endFromKeywords:
            if(str.find(sol, keyword) != -1):
                end = str.find(sol, keyword)
                break
        if(end == -1):
            end = len(sol)

        solution = str.strip(sol[start:end])
        print("'"+solution+"'")

        if submission == solution:
            return ""
    return "Verwendete Tabellen sind nicht korrekt (oder nicht automatisch überprüfbar)."


def checkEquality(sqlPath, solPath):
    bd = Ba.getTableDict()
    sql = normalizeSQLQuery(Ba.getSQLFromFile(sqlPath), bd)
    sol = normalizeSQLQuery(Ba.getSQLFromFile(solPath), bd)
    if(sql=='' or sol==''):
        return "\n\nSQL-Datei ist leer. Aufgabe wurde noch nicht bearbeitet."

    if(sql==sol):
        return ""

    result = buildAndSendCosetteRequest(bd, sql, sol)

    if(result[0] == "ERR"):
        return "\n\nFehler bei der automatischen Überprüfung der Abgabe. Es kann keine Aussage über die Korrektheit der Abgabe getroffen werden."
    elif(result[0] != "EQ"):
        return "\n\nDie Abgabe stimmt nicht mit der Musterlösung überein."
    return ""

