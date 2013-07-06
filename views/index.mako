<h1>Files</h1>
<ul>
  %for file in files:
    <li>${file['name']}: ${file['lines']} lines</li>
  %endfor
</ul>
