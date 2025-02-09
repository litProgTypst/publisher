# Dealing with comments using comentario

We will use [Comentario](https://comentario.app/en/) to collect, vet and
moderate our document comments.

**Pros**

- semi-automatic vetting of comments to help screen out spam

- it looks like we could use Orchid as an Identity Provider using
  Comentario's OIDC provider.

- we seem to be able to prohibit new registrations and only allow comments
  from people with an Orchid account. (This has not yet been verified).

**Cons**

- complex code base 

- for both databases, there is no good way to:

  - version control the comments (as text)

  - recover the database if it gets corrupted

## Integrating comentario comments into documents

A super fancy integration might use split.js to "pop" the comments into a
hide-able side panel associated with a given part of the document.

A simpler integration might be to simply have an "icon" embedded in the
document which is a link to a "comments page" associated with that given
part of the document. A user might be able to use (firefox) side-view (or
Chrome's equivalent) to view the comments at the same time as the relevant
part of the document.

This would work with a PDF as well as the HTML version of the document.

We could use, "[How to make HTML open a hyperlink in another window or
tab? Stack
Overflow](https://stackoverflow.com/questions/2343927/how-to-make-html-open-a-hyperlink-in-another-window-or-tab/2343944#2343944)",
or, "[How to Open a Hyperlink in Another Window or Tab in HTML?
GeeksforGeeks](https://www.geeksforgeeks.org/how-to-open-a-hyperlink-in-another-window-or-tab-in-html/)",
to consistently pop given comments into a named tab/window in the browser.
The user can then decide how they want the main document and the named tab
to be displayed.

To do this we will either need lots of static pages with the "comentario"
embedded tags, OR we need a simple server which serves these pages
semi-automatically (basically avery simple semi-static webserver).

We could base our semi-static webserver on our go-searcher.

## Distinguishing comments across document releases

We need to be able to distinguish comments made before and after a
document (tagged) release.

We could alter comentario to embed the document (released) version into
the comments.

We could embed the release tag into the comment page's url and then have
back references to previous releases. This would require keeping an
ordered list of release tags for each document. These comment release
pages would be served by our semi-static webserver (see above).

However a simpler solution is to post document release comments into each
comment "stream" (page) whenever a particular document has been released.

This suggests we maintain a goLang dictionary whose keys are document-ids
and whose values is a dictionary containing two keys, `releaseTags` and
`references`. The value of the `releaseTags` entry is an ordered array of
release tag (strings). The value of the `references` entry is an ordered
array of reference tags (strings). A comment URL would then be
`/comments/document-id/releaseTag/reference`.

To do this we will post a comment to each page (which has at least one
comment) with the release tag. To do this we need to programmatically
interact with the comentario backend's RestAPI. To do this we need to
review the `comentario/resources/sawgger/swagger.yml` file to find the
entry points and their required parameters.

We will use a simple Python script to implement this automation.

## Building comentario on a Raspberry Pi

The published comentario docker images are NOT built for Arm64 machines.
This means that we need to build our own docker image using a Dockerfile
based upon that in the comentario repository. 

We have attempted to use a (slightly) modified version of the
Dockerfile.build-all script. Unfortunately, due to various IPv6 issues on
our Raspberry PI server, this does not work. We can use the Dockerfile
itself, but to do this we need to install golang and nodejs and build the
backend and frontend comentario servers outside the docker image and copy
them in.

