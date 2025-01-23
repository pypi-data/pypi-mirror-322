A library that normalizes simple SQL queries and compares them first by equality of the normalized string and then using the cosette API. 


### [Beta in Development!]
 [![Build and Test](https://github.com/ValentinHerrmann/sql_testing_tools/actions/workflows/python-build.yml/badge.svg)](https://github.com/ValentinHerrmann/sql_testing_tools/actions/workflows/python-build.yml)
 [![Build and Test](https://github.com/ValentinHerrmann/sql_testing_tools/actions/workflows/python-unittests.yml/badge.svg)](https://github.com/ValentinHerrmann/sql_testing_tools/actions/workflows/python-unittests.yml)

### V 0.1.9
- Support GROUP BY

### V 0.1.8
- Fixed linebreak problems: Linebreaks are now converted into whitespaces before parsing where tokens

### V 0.1.6 + V 0.1.7
- Fixed import error to ensure imports working in different environemnts

### V 0.1.4 + V 0.1.5
- V0.1.5 is just a reupload of V 0.1.4
- Chained conditions (with AND,OR and Paranthesises) in WHERE statement

### V 0.1.3
- SELECT: columns with our without table prefix
- FROM: one or more table from DB; no queries as tables!
- WHERE: single conditions; no Paranthesises!
- GROUP BY one or more columns