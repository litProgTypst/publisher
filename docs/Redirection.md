# How to redirect html

[How to redirect one HTML page to another on load - Stack
Overflow](https://stackoverflow.com/questions/5411538/how-to-redirect-one-html-page-to-another-on-load)

From Billy Moon's answer (https://stackoverflow.com/a/5411601/3035752) :

```
<!--
Source - https://stackoverflow.com/a/5411601
Posted by Billy Moon, modified by community. See post 'Timeline' for change history
Retrieved 2025-11-26, License - CC BY-SA 3.0
-->

<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="0; url=http://example.com">
        <script type="text/javascript">
            window.location.href = "http://example.com"
        </script>
        <title>Page Redirection</title>
    </head>
    <body>
        <!-- Note: don't tell people to `click` the link, just tell them that it is a link. -->
        If you are not redirected automatically, follow this <a href='http://example.com'>link to example</a>.
    </body>
</html>

```

