
# Table of Contents

1.  [Starting the server:](#orga70671f)
2.  [Starting the client:](#orgc0702ff)
    1.  [Using the client:](#org524267f)


<a id="orga70671f"></a>


# Starting the server:

    
    pip install -r requirenments.txt
    
    uvicorn main:app --host 0.0.0.0 --port 8000


<a id="orgc0702ff"></a>

# Starting the client:

    
    pip install -r ./client/requirenments.txt
    
    python ./client/main.py

If your on windows install extra:

    
    pip install windows-curses


<a id="org524267f"></a>

## Using the client:

Key inputs:

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<tbody>
<tr>
<td class="org-left">get:</td>
<td class="org-left">get the list of all uploaded files between two users</td>
</tr>


<tr>
<td class="org-left">get:$FILENAME</td>
<td class="org-left">download the uploaded file to $PATH_TO_CLIENT/static/$FILENAME</td>
</tr>


<tr>
<td class="org-left">put:$FILEPATH</td>
<td class="org-left">upload a file using an absolute path</td>
</tr>


<tr>
<td class="org-left">clear:</td>
<td class="org-left">return from get: to the main chat</td>
</tr>
</tbody>
</table>

