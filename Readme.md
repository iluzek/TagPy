# TagPy

## Synopsis
TagPy is a python script which scans contents of text based files for key words within dictionaries saved by user and outputs results as CSV file as well and HTML page with sortable table.

Data is sorted by:
    -Dictionary name
    -Searched Item (Word/String)
    -Line Number
    -Line Contents
    -File Name

## Ouput Examples
Results on HTML page are highlighted based on Searched Items(case insensitive) within the Line Contents to allow user easier identification of useful results from those that are not of use.

Searched word or string will be highlighted part of each string found, which makes searching a bit easier.

Example 1:
Searched Item = port
Results = [<b><mark>port</b></mark>, <b><mark>Port</b></mark>, <b><mark>PORT</b></mark>, im<b><mark>port</b></mark>, Unsup<b><mark>port</b></mark>ed, sup<b><mark>port</b></mark>, get<b><mark>Port</b></mark>, DataTrans<b><mark>port</b></mark>KEY]

Example 2:

<table class="sortable">
    <thead>
        <tr><th>Dictionary</th><th>Searched</th><th>Line</th><th>Line Contents</th><th>File Name</th></tr>
    </thead>
    <tbody>
        <tr><td>lorem</td><td>ac</td><td>4</td><td>Nam a l<b><mark>ac</mark></b>us vitae lorem auctor dictum in id augue.</td><td>lorem_ipsum.txt</td></tr>
        <tr><td>lorem</td><td>ac</td><td>7</td><td>Vivamus <b><mark>ac</mark></b>cumsan magna id l<b><mark>ac</mark></b>inia consequat.</td><td>lorem_ipsum.txt</td></tr>
        <tr><td>lorem</td><td>ac</td><td>10</td><td>Fusce <b><mark>ac</mark></b> nulla sit amet risus efficitur convallis sit amet et dui.</td><td>lorem_ipsum.txt</td></tr>
        <tr><td>lorem</td><td>ac</td><td>11</td><td>Mauris pellentesque ex et odio f<b><mark>ac</mark></b>ilisis, eget dictum urna ultrices.</td><td>lorem_ipsum.txt</td></tr>
        <tr><td>lorem</td><td>ac</td><td>13</td><td>Proin rhoncus sapien pl<b><mark>ac</mark></b>erat nisi efficitur efficitur.</td><td>lorem_ipsum.txt</td></tr>
        <tr><td>lorem</td><td>ac</td><td>20</td><td>In tincidunt leo <b><mark>ac</mark></b> fermentum fermentum.</td><td>lorem_ipsum.txt</td></tr>
        <tr><td>lorem</td><td>ac</td><td>22</td><td>Nullam a lorem euismod, bibendum l<b><mark>ac</mark></b>us porta, consectetur dolor.</td><td>lorem_ipsum.txt</td></tr>
        <tr><td>lorem</td><td>ac</td><td>23</td><td>Integer vel magna egestas, convallis leo <b><mark>ac</mark></b>, scelerisque eros.</td><td>lorem_ipsum.txt</td></tr>
        <tr><td>lorem</td><td>amet</td><td>1</td><td>Lorem ipsum dolor sit <b><mark>amet</mark></b>, consectetur adipiscing elit.</td><td>lorem_ipsum.txt</td></tr>
        <tr><td>lorem</td><td>amet</td><td>10</td><td>Fusce ac nulla sit <b><mark>amet</mark></b> risus efficitur convallis sit <b><mark>amet</mark></b> et dui.</td><td>lorem_ipsum.txt</td></tr>
        <tr><td>lorem</td><td>amet</td><td>14</td><td>Nunc sit <b><mark>amet</mark></b> neque id nunc ornare luctus.</td><td>lorem_ipsum.txt</td></tr>
        <tr><td>lorem</td><td>amet</td><td>24</td><td>Etiam pretium dolor sit <b><mark>amet</mark></b> vulputate semper.</td><td>lorem_ipsum.txt</td></tr>
        <tr><td>lorem</td><td>lorem</td><td>1</td><td><b><mark>Lorem</mark></b> ipsum dolor sit amet, consectetur adipiscing elit.</td><td>lorem_ipsum.txt</td></tr>
        <tr><td>lorem</td><td>lorem</td><td>4</td><td>Nam a lacus vitae <b><mark>lorem</mark></b> auctor dictum in id augue.</td><td>lorem_ipsum.txt</td></tr>
        <tr><td>lorem</td><td>lorem</td><td>22</td><td>Nullam a <b><mark>lorem</mark></b> euismod, bibendum lacus porta, consectetur dolor.</td><td>lorem_ipsum.txt</td></tr>
        <tr><td>lorem</td><td>sem</td><td>24</td><td>Etiam pretium dolor sit amet vulputate <b><mark>sem</mark></b>per.</td><td>lorem_ipsum.txt</td></tr>
    </tbody>
</table>

## Code Example
Script requires a path to scan.

    python tagpy.py "path to directory"

Example:

    python tagpy.py "C:\ProjectToScan"

NOTE:   Do not add &quot;/&quot; or &quot;\\&quot; at the end of the path - Bug will cause the path to be unrecognized - Will be fixing it soon.

## Motivation

TagPy started as quick script to find "words of interest" and line numbers within source code of large applications and mainly Android APK source code.
The aim was to identify code that might be useful during pen-testing project by finding strings like: "http", "address", "pass", "user". etc

That worked relatively well, however output in .txt file looked atrocious.

While searching for a better method to display content, an idea to use HTML with javascript to sort table was suggested and it looked pretty good.

Many hours later..after completely breaking code and pretty much rewriting it from scratch, output to csv file and HTML page was implemented.
Additionally use of HTML allowed for applying &lt;mark&gt;&lt;/mark&gt; tags within the table contents to quickly identify searched word within line of code.


## Installation and Use

Requirements: Python 3


1. Download Project as a ZIP
2. Extract the ZIP
3. No installation
4. Run it from console - python tagpy.py "path to scan"
NOTE:   Do not add &quot;/&quot; or &quot;\\&quot; at the end of the path - Bug will cause the path to be unrecognized - Will be fixing it soon.
5. Open directory results
6. Open newly created directory - Directory_Date@Time
7. Use results.csv or open sortable_results.html
8. HTML - Wait for page to load
9. Click on column names to sort results by that category

## Editing and Adding Dictionaries

Dictionaries are located in

    resources/dictionaries/

Directory "allowed_dictionaries" contains dictionary files. Name of the file will become name of the dictionary.


Directory "banned_dictionaries" contains banned dictionary files. Those files will apply only to the allowed_dictionaries results
to ignore specific line of code if word from "allowed_dictionaries" is found.


Example:
authentication dictionary would have found a word 'password' within the line of text, however that line also contains
"import java.net" string which was determined to be of no consequence for the search.
That way that particular line of text will not be checked for all other searches and will never show up in end results.

Use banned_dictionaries to narrow your results, which can be very effective if syntax or structure of files canned can be
predicted. Working on banned_dictionaries can reduce meaningless results significantly.

To add words/phrases or strings into specific dictionary simply add new content on next line within the file.
Feel free to remove current dictionaries and add your own.

## Further Development

I have plans to work on the project in future.
I have some ideas on what could be added to the project, however at the time of writing (01 September 2016), there is not much time that I can allocate to the project  and as such it might not find any updates for a while.

This project is pretty specific and I cannot say I found a similar program or script that would do what this python script does, so hopefully this helps someone.