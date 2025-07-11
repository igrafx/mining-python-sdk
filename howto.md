<h1 align="center"> How to use the SDK </h1>

This document encompasses the installation and basic uses of the **iGrafx P360 Live Mining SDK**. It also contains SQL and Pandas examples.

The **iGrafx P360 Live Mining SDK** is an open source application that can be used to manage your mining projects.
It is a python implementation of the iGrafx P360 Live Mining API.

With this SDK, you will be able to create and manipulate workgroups, projects, datasources and graphs 
(and graph instances). You will also be able to create and add a column mapping.

Please note that you must have an iGrafx account in order to be able to use the SDK properly. 
Please contact us to create an account.

You may find the github of the iGrafx Mining SDK [here](https://github.com/igrafx/mining-python-sdk).

***
## Table of Contents

1. [Installing](#installing)
2. [Requirements](#requirements)
3. [Getting Started](#getting-started)
4. [Workgroups and Projects](#workgroups-and-projects)
5. [Sending Data (File Structure and Column Mapping)](#sending-data)
6. [Graphs](#graphs)
7. [Graph Instances](#graph-instances)
8. [Datasources](#datasources)
9. [Using Pandas methods](#using-pandas-methods)
10. [Using Druid SQL Queries](#using-druid-sql-queries)
11. [Using the public API](#using-the-public-api)
12. [Generating the Documentation with SphinxDocs](#generating-the-documentation-with-sphinxdocs)
13. [Further Documentation](#further-documentation)


## Installing

### With pip:
To install the current release of the iGrafx P360 Live Mining SDK with pip, simply navigate to the console 
and type the following command: 
````shell
pip install igrafx_mining_sdk
````


## Requirements

This package requires python 3.10 or above. Get the latest version of [Python](https://www.python.org/).

The requirements of this SDK work with [Poetry](https://python-poetry.org/docs/).
Please install it before proceeding further. Eventually, specify ``poetry env`` if you handle multiple python versions. The following commands could help you :
```sh
which python
poetry env use ~/.pyenv/pyenv-win/versions/your/version
```

You must also make sure you add Poetry to your ``PATH``.

Afterward, you can install the dependencies in the `.venv` virtual environment.
This command produces a [poetry.lock](https://github.com/igrafx/mining-python-sdk/blob/dev/poetry.lock) file that is not versioned to Git.
````sh
poetry update
poetry lock
````
The following command installs the dependencies:
```sh
poetry install
```

The [pyproject.toml](https://github.com/igrafx/mining-python-sdk/blob/dev/pyproject.toml) contains the projects details and all the necessary dependencies.
If you wish, you can see the versions of the packages used in it.

Furthermore, make sure you have `JAVA` installed on your machine.
If it is not installed, you can download and install it from [Oracle's Java](https://www.oracle.com/java/technologies/downloads/#java11?er=221886) website or [AdoptOpenJDK](https://adoptium.net/).

After having installed Java, you need to set the `JAVA_HOME` environment variable to point to the directory where it is installed.

If you're using **Windows**:

1. Go to `Control Panel -> System and Security -> System -> Advanced system settings`.
2. Click on `Environment Variables`.
3. Under `System Variables`, click `New` and add the following:
   - Variable name: `JAVA_HOME`
   - Variable value: The path to your Java installation, for example: `C:\Program Files\Java\jdk-11.0.11` or `C:\Program Files\OpenJDK\jdk-8.0.332.09-hotspot`

4. After that, update the `Path variable` to include **the Java bin directory**:
   - Find the `Path variable ` in the System Variables section and click `Edit`.
   - Add a new entry: `%JAVA_HOME%\bin`.

Now that the `JAVA_HOME` variable is set, you can verify the JAVA installation:
 - Open a new **command prompt** (important, as it needs to pick up the updated `JAVA_HOME` variable).
 - Run the following command to check if Java is correctly installed:
````shell
java -version
````
This command should print the version of Java you have installed.

You will need Java to be able to get and query datasources.

This project includes jar from Apache Calcite Avatica
(https://mvnrepository.com/artifact/org.apache.calcite.avatica/avatica),
which is licensed under the Apache License, Version 2.0.

The original Apache License can be found in LICENSES/Apache-2.0.txt.

### Reinstall python and poetry procedure:

If you are encountering issues, you may wish to reinstall both Python and Poetry from scratch.  
Follow these steps in the project directory:
1. Delete .venv file in your project
2. Delete Python interpreter from your IDE Settings
3. Delete poetry.lock file
4. Run command `curl -sSL https://install.python-poetry.org | python3 - --uninstall`
5. Run command `pyenv uninstall <version_number>`
6. Run command `pyenv install --skip-existing $(cat .python-version)`
7. Run command `curl -sSL https://install.python-poetry.org | python3 -`
8. Run command `poetry lock`. You should end up with a new poetry.lock file and a new .venv directory.
9. Create Python Poetry interpreter from your IDE Settings, pointing to the created .venv directory.
10. Run command `poetry install`

## Getting Started

First, open up **Process Explorer 360**, and go to your 
[Workgroup](https://github.com/igrafx/mining-python-sdk/wiki/4.-Workgroups-and-Projects) settings. 
In the settings page, go to the **Public API** tab. There, you should see your **Workgroup's ID**, **Workgroup secret key**,
**Mining Platform API URL**, **Mining Platform Auth URL** and **JDBC URL**. 

These are the credentials that will be used by the SDK to log in to the **iGrafx P360 Live Mining API**.

![settings](https://github.com/igrafx/mining-python-sdk/blob/dev/imgs/settings.PNG)


### To begin:
Go ahead and **import** the package:
```python
import igrafx_mining_sdk as igx   # the 'as igx' is entirely optional, but it will make the rest of our code much more readable
```
## Workgroups and Projects

The first step of using the iGrafx P360 Live Mining SDK will be to **create a workgroup**, 
using the credentials you copied from **Process Explorer 360**:
```python
w_id = "<Your Workgroup ID>"
w_key = "<Your Workgroup KEY>"
api_url = "<Your Mining Platform API URL>"
auth_url = "<Your Mining Platform Auth URL>"
jdbc_url = "<Your JDBC URL>"
wg = igx.Workgroup(w_id, w_key, api_url, auth_url, jdbc_url)
```
The **JDBC URL** is used to connect to the database and do queries and operations on datasources.

Once the workgroup is created, you can access the list of 
[projects](https://github.com/igrafx/mining-python-sdk/wiki/4.-Workgroups-and-Projects) associated 
with the workgroup through the ``get_project_list()`` method:
```python    
project_list = wg.get_project_list()
```
The list of project IDs associated with the workgroup can be accessed with:
```python
project_id_list = [p.id for p in project_list]
```

A specific project ID can be accessed from the list by specifying its index:
```python
project_id_list[0]
```

The project ID can also be found in the URL:
```URL
https://<Mining Platform URL>/workgroups/<Workgroup ID>/projects/<Project ID>/data
```

On top of that, if you already know the ID of the project you want to work with you can use:
```python
my_project = wg.project_from_id("<Your Project ID>")
```

Please note that for a given **Workgroup** it is possible to retrieve its metadata which includes its name, its creation date and expiration date and finally its data version.
To retrieve the metadata of a Workgroup, you can use the following method:
````python
wg_metadata = wg.get_workgroup_metadata
````

To retrieve the name, creation or expiration dates of the workgroup specifically, you may do as follows:
````python
wg_metadata = wg.get_workgroup_metadata.get("name")
wg_metadata = wg.get_workgroup_metadata.get("creationDate")
wg_metadata = wg.get_workgroup_metadata.get("expirationDate")
````
Moreover, to retrieve the data version of the Workgroup, you may do as follows:
````python
wg_data_version = wg.get_workgroup_data_version
````

Once you have the project you want to use, several actions can be taken.

You can check if the project ``exists``and get its ``name``:
````python
my_project.exists
my_project.get_project_name()
````

Furthermore, the `column mapping` of a project can be retrieved:
````python
my_project.get_column_mapping()
````
This method returns the entirety of the column mapping of a project in a **JSON format** (as shown directly below).
This JSON can directly be used to add a column mapping, and thus to add a file.
For more details on how to add a column mapping using a JSON, view the next section.
````JSON
{
"col1": {"name": "case_id", "columnIndex": "0", "columnType": "CASE_ID"},
"col2": {"name": "task_name", "columnIndex": "1", "columnType": "TASK_NAME"},
"col3": {"name": "time", "columnIndex": "2", "columnType": "TIME", "format": "yyyy-MM-dd'T'HH:mm"}
}
````

More precisely, the `mapping infos` of the project can be retrieved:
````python
my_project.get_mapping_infos()
````

The list of available **lookups** for the project can also be retrieved:
````python
my_project.get_project_lookups()
````
An example of what will be returned is the following:
````JSON
[
  {
    "name": "be755cbe-1c70-46b7-ac60-f09478a122e6_excluded_cases",
    "description": "string",
    "usage": "SELECT LOOKUP(graphkey, 'be755cbe-1c70-46b7-ac60-f09478a122e6_variants') from \"be755cbe-1c70-46b7-ac60-f09478a122e6\""
  }
]
````

You may then use the **lookups** as you desire.

The project can also be ``deleted``:
````python
my_project.delete_project()
````

Its ``variants`` and ``completed cases`` can also be retrieved:
````python
my_project.get_project_variants(<Page Index>, <Limit>, "<Search>" ) 
my_project.get_project_completed_cases(<Page Index>, <Limit>, "<Search Case ID>")
````
Where `Page Index` is the page index for pagination, `Limit` is the maximum number of items to return per page,
`Search` is the search query to filter variants by name (optional) and `Search Case ID` is the search
query to filter cases by ID (also optional).


Moreover, you can ``reset`` the project if needed:
````python
my_project.reset
````
Alternatively, if you wish to create your own project, you can do so as follows:
````python
w = Workgroup(w_id, w_key, api_url, auth_url, jdbc_url)
project_name = "<Your Project name>"
project_description = "<Your Project description>"
created_project = w.create_project(project_name, project_description)
````
Note that the description is optional. If not needed, you can do the following:
```python
created_project = w.create_project(project_name)
```

## Sending Data

To be able to add data, you must create a 
[file structure](https://github.com/igrafx/mining-python-sdk/wiki/5.-Sending-Data#filestructure) and add a 
[column mapping](https://github.com/igrafx/mining-python-sdk/wiki/5.-Sending-Data#column-mapping).
A column mapping is a list of columns describing a document(.CSV, .XLSX, .XLS).

To add a column mapping, you must first define the file structure:

````python
filestructure = FileStructure(
    file_type=FileType.XLSX,
    charset="UTF-8",
    delimiter=",",
    quote_char='"',
    escape_char='\\',
    eol_char="\\r\\n",
    comment_char="#",
    header=True,
    sheet_name="Sheet1"
)
````
It is important to note that aside from the ```file_type```(which can be set to CSV, XLSX or XLS) and 
the ```sheet_name```(which is optional), the attributes above are set by default.
That means that unless the value of your attribute is different, you do not need to set it.

Now, a column mapping can be created:
```` python
column_list = [
            Column('<Column name>', <Column index>, <Column Type>),
            Column('<Column name>', <Column index>, <Column Type>),
            Column('<Column name>', <Column index>, <Column Type>, time_format='<Your time format>')
        ]
        column_mapping = ColumnMapping(column_list)
````
- ``Column name`` is the name of the column.
- ``Column index`` is the index of the column of your file. Note that the **column index** starts at **0**.
- ``Colulmn Type`` is the type of the column. It can be ``CASE_ID``, ``TASK_NAME``, ``TIME``, ``METRIC``
(a numeric value) or ``DIMENSION``(can be a string).

Please note that your **time format** must use the [Java SimpleDateFormat format](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html).

This means you must mark the date by using the following letters (according to your date format):

![date_format](https://github.com/igrafx/mining-python-sdk/blob/feat/PROC-3134_modify_date_format_in_doc/imgs/date_format.png)

For example, your date format may look like this:
````
yyyy-MM-dd HH:mm:ss.SSSSSS
````

In the following examples, do not forget to change the `time_format` before using the code.


It is also possible to check whether a column mapping exists or not:
```python
my_project.column_mapping_exists
```
Furthermore, a column can also be created from a JSON.
```python
json_str = '{"name": "test", "columnIndex": "1", "columnType": "CASE_ID"}'
column = Column.from_json(json_str)
```
Therefore, a Column Mapping can also be created from a JSON column dictionary. For example:
```python
column_dict = '''{
"col1": {"name": "case_id", "columnIndex": "0", "columnType": "CASE_ID"},
"col2": {"name": "task_name", "columnIndex": "1", "columnType": "TASK_NAME"},
"col3": {"name": "time", "columnIndex": "2", "columnType": "TIME", "format": "yyyy-MM-dd'T'HH:mm"}
}'''
column_mapping = ColumnMapping.from_json(column_dict)
```

The Column Mapping can also be created from a JSON column list.
The major difference between the list and the dictionary is that in the dictionary you have to enunciate the column number before giving the other information. 
```python
column_list = '''[
{"name": "case_id", "columnIndex": "0", "columnType": "CASE_ID"},
{"name": "task_name", "columnIndex": "1", "columnType": "TASK_NAME"},
{"name": "time", "columnIndex": "2", "columnType": "TIME", "format": "yyyy-MM-dd'T'HH:mm"}
]'''
column_mapping = ColumnMapping.from_json(column_list)
```
Moreover, it is possible to return the JSON dictionary format of the Column with the `to_dict()` method.
By doing that, we can then create a Column Mapping with the `from_json()` method.
The `json.dumps()` function will convert a subset of Python objects into a JSON string.

```python
column_list = [
    Column('case_id', 0, ColumnType.CASE_ID),
    Column('task_name', 1, ColumnType.TASK_NAME),
    Column('time', 2, ColumnType.TIME, time_format="yyy-MM-dd'T'HH:mm")
]
column_mapping = ColumnMapping(column_list)
json_str = json.dumps(column_mapping.to_dict())
column_mapping = ColumnMapping.from_json(json_str)
```

After creating it, the column mapping can be added:
```` python
my_project.add_column_mapping(filestructure, column_mapping)
````

Finally, you can add CSV, XLSX or XLS files:
```` python
wg = Workgroup(w_id, w_key, api_url, auth_url, jdbc_url)
p = Project("<Your Project ID>", wg.api_connector)

filestructure = FileStructure(
    file_type=FileType.xlsx,
    sheet_name="Sheet1"
)
column_list = [
    Column('Case ID', 0, ColumnType.CASE_ID),
    Column('Start Timestamp', 1, ColumnType.TIME, time_format="yyyy-MM-dd'T'HH:mm"),
    Column('Complete Timestamp', 2, ColumnType.TIME, time_format="yyyy-MM-dd'T'HH:mm"),
    Column('Activity', 3, ColumnType.TASK_NAME),
    Column('Ressource', 4, ColumnType.DIMENSION),
]
column_mapping = ColumnMapping(column_list)
p.add_column_mapping(filestructure, column_mapping)
p.add_file("ExcelExample.xlsx")
````
The ``add_file`` method returns information about the added file in JSON format such as the file ID,
the file name and the status.
````json
{
  "creationDate": "2024-08-05T09:52:00.761Z",
  "id": "b8d5324b-c812-4ba3-ac9d-187cff04337a",
  "name": "p2pShortExcel.xlsx",
  "status": {
    "progress": 0,
    "status": "PROCESSING"
  }
}
````

Note that a **zip** file can also be sent. To do so, in the file structure,
the declared file type should be the final format of the file within the zip (e.g., .csv, .xlsx, .xls).
And when giving the file path in the ``add_file`` method, give the zip name.

Additionally, the status of the added file(s) can be checked by using the following method:

````python
p.get_project_files_metadata( < Page
Index >, < Limit >, < Sort
Order >)
````
Note that the `Sort Order` is set to `ASC` by default. You can also set it to `DESC`.

Here is what this method returns:
```json
{
  "totalItems": 1,
  "files": [
    {
      "id": "d93812db-648d-41ef-bf59-732570e89388",
      "name": "testdata.csv",
      "status": "PROCESSING",
      "creationDate": "2024-07-23T14:00:34.462Z",
      "ingestionStatus": "STARTED"
    }
  ]
}
```

You can also check the metadata of a specific file by doing this:
```python
p.get_file_metadata(file_id)
```
You can get the file_id by using the ``add_file`` method.

The status of a specific file ID can also be checked by using the following method:

```python
p.get_file_ingestion_status(file_id)
```
Furthermore, grouped tasks can also be declared if needed.
If a grouped task is created in a column, there must be grouped tasks declared in other columns as well as they cannot function individually:
```` python
column_list = [
    Column('case_id', 0, ColumnType.CASE_ID),
    Column('time', 1, ColumnType.TIME, time_format="yyyy-MM-dd'T'HH:mm"),
    Column('task_name', 2, ColumnType.TASK_NAME, grouped_tasks_columns=[1, 3]),
    Column('country', 3, ColumnType.METRIC, grouped_tasks_aggregation=MetricAggregation.FIRST),
    Column('price', 4, ColumnType.DIMENSION, grouped_tasks_aggregation=GroupedTasksDimensionAggregation.FIRST)
]
column_mapping = ColumnMapping(column_list)
````
The `grouped_tasks_columns` represent the list of column indices that must be grouped.
If `grouped_tasks_columns` is declared, it has to at least have the index of a column of type `TASK_NAME`
and the index of a column of type `METRIC`, `DIMENSION` or `TIME`. It must not have the index of a column of type `CASE_ID`.

The `grouped_tasks_aggregation` represents the aggregation of the grouped tasks.

Moreover, if a grouped task aggregation's column type is `METRIC`, then the grouped task's type must be of `MetricAggregation` type.
Similarly, if a grouped task aggregation's column type is `DIMENSION`, then the grouped task's type must be of `GroupedTasksDimensionAggregation` type.
Finally, if `grouped_tasks_columns` is declared, the column's type must be `TASK_NAME`.


## Graphs


Additionally, you can access the project components: the model 
[Graph](https://github.com/igrafx/mining-python-sdk/wiki/6.-Graphs-and-Graph-Instances), 
the [Graph Instances](https://github.com/igrafx/mining-python-sdk/wiki/6.-Graphs-and-Graph-Instances), 
and the [datasources](https://github.com/igrafx/mining-python-sdk/wiki/7.-Datasources).

The model graph is accessed through the `.graph()` function:
```python
my_project = wg.project_from_id("<Your Project ID>")
g = my_project.graph()
```
The Graph class inherits from the [NetworkX library](https://networkx.org/documentation/stable/index.html#).
This means that it is possible to create a display method according to your liking in the Graph class:
````python
import matplotlib.pyplot as plt

"""Displays the graph using NetworkX library"""
# Using the kamada kawai layout algorithm
pos = nx.kamada_kawai_layout(g)
# Set the START node to green and the END node to red
color_mapper = {"START": "green", "END": "red"}
labels = {n: g.nodes[n]["name"] for n in g.nodes} # Use name as label
colors = [color_mapper.get(g.nodes[n]["name"], 'blue') for n in g.nodes] # Set nodes colors (default to blue)

# Draw and show the graph
nx.draw(g, pos=pos, labels=labels, node_color=colors, node_size=1000, connectionstyle='arc3,rad=0.2')
plt.show()
````

It will give us a graph similar to the subsequent one:
![Graph_for_howto.png](https://github.com/igrafx/mining-python-sdk/blob/dev/imgs/Graph_for_howto.png)

The graph can then be saved as GEXF:
```python
nx.write_gexf(g, 'graph_name.gexf')
```
It can also be saved as GML:
```python
nx.write_gml(g, 'graph_name.gml')
```

## Graph Instances


Moreover, the graph instances can be accessed as a list with:
```python
my_project = wg.project_from_id("<Your Project ID>")
graph_instance_list = my_project.get_graph_instances()
```

It is possible to set a ``limit`` to ```get_graph_instances()```. 
This allows us to only load a given number of graph instances.
```python
graph_instance_list = my_project.get_graph_instances(limit=3)
```

It is also possible to set a ``shuffle`` option to ```get_graph_instances()```.
If set to ``True``, the list of graph instances returned is shuffled. 
If set to ``False``, the list of graph instances returned is not shuffled.
```python
graph_instance_list = my_project.get_graph_instances(limit=5, shuffle=True)
```

The process keys can also be accessed as a list with:
```python
my_project = wg.project_from_id("<Your Project ID>")
process_key_list = my_project.process_keys
```

A graph instance can directly be requested by using one of the project's process keys:
```python
pk = process_key_list[0]
gi = my_project.graph_instance_from_key(pk)
```
## Datasources


Each project is linked to **datasources**. Those datasources have 3 types: `vertex`, `simplifiedEdge` and `cases`. 
The datasources will be accessed using the **JDBC URL** that was given when creating a workgroup.

To access those we can do:
```python
db1 = my_project.nodes_datasource # For vertex
db2 = my_project.edges_datasource # For simplifiedEdge
db3 = my_project.cases_datasource # For cases
```
Those datasources are Python objects that can be used to facilitate access to corresponding data.
Once created, they are empty and need to be requested so that data can be fetched.

The easiest way to do this is to use the `.load_dataframe()` method, 
which is equivalent to a ``SELECT * FROM [datasource]`` request.
Optionally, the ``load_limit`` parameter can be used to fetch a subset of the dataframe.
This method returns a **Pandas 
[Dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)** object.
````python
df = db1.load_dataframe(load_limit=10) # load 10 rows of nodes_datasource

````

You can also retrieve the columns of the datasource:
```python
cols = db2.columns
```

Moreover , it is possible to de a specific query on the datasource. By doing this you may access the database via Druid SQL queries.
This uses the JDBC connection.
```python
simple_sql = f'SELECT * FROM "{ds.name}" LIMIT 1'
df = db3.request(simple_sql)
```
You may find more details using queries in the section [Using Druid SQL Queries](#using-druid-sql-queries).

You can also return a list of all datasources associated with the workgroup.
Note that in that case, all types of datasources are returned in the same list:
````python
datasources_list = wg.datasources
````

If there are open connections, they can be closed if necessary:

```python
wg = Workgroup(w_id, w_key, api_url, auth_url, jdbc_url)
ds = Datasource("<Your Datasource Name>", "<Your Datasource Type>")
ds.close_ds_connection()
```

## Using Pandas methods


The **[Pandas](https://pandas.pydata.org/docs/)** methods is the simplest option when it comes to handling your dataset 
(compared to [SQL queries](https://github.com/igrafx/mining-python-sdk/blob/dev/howto.md#using-sql-queries)) but may be less performant.
Pandas can also be used to easily plot graphs.

If you want to see the structure of the datasource, you can use the `.columns` method:
```python
df = my_project.edges_datasource.load_dataframe(load_limit=1000)
print(df.columns)
```

Operations can be done on dataframe. For example, we can calculate the mean value of the `duration` column:
```python
duration_mean = df['duration'].to_numpy().mean()
```

We can also get the maximum or minimum of the `enddate` column:
```python
enddate_max = df['enddate'].max()
enddate_min = df['enddate'].min()
```

Moreover, in the next example, we group the dataframe by `case ID`:
```python
by_caseid = df.groupby('caseid')
```

Furthermore, the Pandas `.describe()` method can be applied to our dataframe:
```python
stats_summary = df.describe()
```

This method returns a statistics summary of the dataframe provided. It does the following operations for each column:

* count the number of not-empty values
* calculate the mean (average) value
* calculate the standard deviation
* get the minimum value
* calculate the 25% percentile
* calculate the 50% percentile
* calculate the 75% percentile
* get the maximum value

It then stores the result of all previous operations in a new dataframe (here, `stats_summary`).

If need be, you can directly use the datasource's `connection` and `cursor` methods, 
which can be used as specified in the [Python Database API](https://peps.python.org/pep-0249/):
```python
ds = my_project.edges_datasource
ds.connection
ds.cursor
```

## Using Druid SQL Queries


In the last section, it was shown how to load the entire dataframe and do operations with **Pandas**. 
With **SQL** you can load the dataframe and do the operations in the same query, hence why it is faster.
Those requests are often more powerful and performant than the **[Pandas](#using-pandas-methods)** methods 
presented above.
However, the Pandas methods are simpler to use and understand.

In those requests, the name of the table is accessible through the `name` attribute and must be given 
in between double quotes.  The use of [f-strings](https://realpython.com/python-f-strings/) is highly recommended.

A description of the tables is available [here](https://en.help.logpickr.com/api/Description_Datasources_V1/).
It contains a glossary and descriptions of the different elements in a table.

Therefore, the following request returns all the columns of the given datasource for the specified process key.
```python
ds = my_project.edges_datasource
edges_filtered = ds.request(f'SELECT * FROM \"{ds.name}\" WHERE "processkey" = \'<Your Process Key>\'')
```

We can also calculate the mean value of the `duration` column. For example:
```python
edge_duration_mean = ds.request(f'SELECT AVG(duration) FROM \"{ds.name}\"')
```

In a similar manner, the subsequent requests return respectively the minimum and the maximum value of the 
`enddate` column:
```python
edge_enddate_min = ds.request(f'SELECT MIN(enddate) FROM \"{ds.name}\"')
edge_enddate_max = ds.request(f'SELECT MAX(enddate) FROM \"{ds.name}\"')
```

Finally, the following SQL statement lists the number of `cases` by `detail destination`, sorted high to low:
```python
count = ds.request(f'SELECT COUNT(caseid), detail_7_lpkr_destination FROM \"{ds.name}\" GROUP BY detail_7_lpkr_destination ORDER BY COUNT(caseid) DESC')
```

## Using the public API


**Workgroups and projects** can also be accessed with the **public API**. The documentation for the 
*iGrafx P360 Live Mining API* can be found  [here](https://public-api.logpickr.com).

To do so, we use ``curl``.

First of all, we must retrieve a token else we will not be able to do the desired requests.
Please note that these tokens have a time limit and so, if you notice that the requests 
are not working anymore, simply regenerate the tokens.
````commandline
curl -X POST   <Your authentication URL>/protocol/openid-connect/token   --data "grant_type=client_credentials"   --data "client_id=<Your workgroup ID>"   --data "client_secret=<Your workgroup Key>" | jq
````

Note that the `| jq ` is optional, but it will be easier to read the result if you include it.

Then, we can use the `GET` HTTP method to access the list of available projects. Don't forget to use the token:
````commandline
curl -X "GET" "https://<Your API URL>/pub/projects" -H "accept: application/json" -H "Authorization: Bearer <Your generated Token>"
````

With the same method, we can **access** a project graph model:
````commandline
curl -X GET "https://<Your API URL>/pub/project/<Your Project ID>/graph?mode=gateways" -H "accept: application/json" -H "Authorization: Bearer <Your generated Token>"
````

In a similar manner, the projects' **datasources** are returned by:
````commandline
curl -X GET "https://<Your API URL>/pub/datasources?id=<Your Project ID>" -H "accept: application/json" -H "Authorization: Bearer <Your generated Token>"
````

Furthermore, with the HTTP method `POST`, several actions can be done.

You can create a project:
````commandline
curl -X POST "https://<Your API URL>/pub/project?name=<Your project name>&workgroupId=<Your Workgroup ID>" -H "accept: application/json" -H "Authorization: Bearer <Your generated Token>" -d ""
````

The project's **column mapping** can be posted:
````commandline
curl -X POST "https://<Your API URL>/pub/project/<Your Project ID>/column-mapping" -H "accept: */*" -H "Authorization: Bearer <Your generated Token>" -H "Content-Type: application/json" -d '{\"fileStructure\":{\"charset\":\"UTF-8\",\"delimiter\":\";\",\"quoteChar\":\"\\\"\",\"escapeChar\":\"\\\\\",\"eolChar\":\"\\\\",\"header\":true,\"commentChar\":\"#\",\"fileType\":\"csv\",\"sheetName\":\"string\"},\"columnMapping\":{\"caseIdMapping\":{\"columnIndex\":0},\"activityMapping\":{\"columnIndex\":0},\"timeMappings\":[{\"columnIndex\":0,\"format\":\"string\"}],\"dimensionsMappings\":[{\"name\":\"Activity\",\"columnIndex\":0,\"isCaseScope\":true,\"aggregation\":\"FIRST\"}],\"metricsMappings\":[{\"name\":\"Activity\",\"columnIndex\":0,\"unit\":\"string\",\"isCaseScope\":true,\"aggregation\":\"FIRST\"}]}}'
````

A file can then be added: 
````commandline
curl -X POST "https://<Your API URL>/pub/project/<Your Project ID>/file?teamId=<Your Workgroup ID>" -H "accept: application/json" -H "Authorization: Bearer <Your generated Token>" -H "Content-Type: multipart/form-data" -F "file=@output.csv;type=text/csv"
````

Additionally, to **reset** all project data except it's name, description and user rights, we can use the subsequent `curl` command:
````commandline
curl -X POST "https://<Your API URL>/pub/project/<Your Project ID>/reset" -H "accept: */*" -H "Authorization: Bearer <Your generated Token>"
````
Finally, `DELETE` methods can be used.

For instance, we can use that method to **stop** the train task for a project:
````commandline
curl -X DELETE "https://<Your API URL>/pub/train/<Your Project ID>" -H "accept: */*" -H "Authorization: Bearer <Your generated Token>"
````

## Generating the Documentation with SphinxDocs

You may generate documentation from the code using [Sphinx](https://www.sphinx-doc.org/en/master/index.html).

To do this you must first install Sphinx by using the following command:
````shell
pip install -U sphinx
````
Afterward, go to the `sphinx_docs` directory by doing:
````shell
cd sphinx_docs/
````
Now you can generate the documentation as follows:
````shell
make html
````
If you wish to clean the `build` directory, you may use this command:
````shell
make clean
````

The documentation has now been generated. To open it, go to the `build directory`, then into the `html` directory.
Double-click on the ``index.html`` to open it. Else, right click and click *open with* and pick a browser to open it with. 

## Further documentation

In this section, documentation can be found for further reading.

Support is available at the following address: [support@igrafx.com](mailto:support@igrafx.com)


* [iGrafx Help](https://doc.igrafxcloud.com/mining/en/index.html)
* [Druid SQL API](https://druid.apache.org/docs/latest/querying/sql-api.html)
* [iGrafx P360 Live Mining API](https://doc.igrafxcloud.com/mining/api/index.html)



