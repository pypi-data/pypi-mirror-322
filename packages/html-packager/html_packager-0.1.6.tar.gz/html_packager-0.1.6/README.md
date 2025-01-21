# HTML-Packager

I would like tu distribute my reports in `html` format, but without 
complicate the people I send the documents to reply the directory structure and 
running a local server. 

With this command-line tool, all local references to css, javascript and images, 
are included inside the `html` file and this is the only file needed to renther the report.

## Quickstart

### Install

```bash
$ pip install html-packager
```

This installs a command line tool with the syntax

```bash
$ html-package myfile.html
```

this command creates `myfile_pkg.html` in the same directory. 

All the files included are listed on screen. 

---

## Licence

2025 - Rodolfo Pregliasco MIT Licence.