<!DOCTYPE html>
<meta charset="utf-8">

<h1>Files</h1>
<ul>
  %for file in files:
    <li>${file['name']}: ${file['lines']} lines</li>
  %endfor
</ul>
