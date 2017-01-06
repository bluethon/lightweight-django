Cmd Note
=========

### Set envirn

    export DEBUG=on
    unset DEBUG

### use the template with `startproject`

使用自定义模板生成新项目

**注意模板使用{{ secret_key }}**

    django-admin.py startproject <foo> --template=project_name

### use Gunicorn and set output to console

    gunicorn hello --log-file=-
