# `potluck`

TODO: fix exercise solution visibility!

Code for automatically evaluating Python programming tasks, including a
`flask` WSGI server for handling submissions.

Specifications API design by Peter Mawhorter.

Server design by Peter Mawhorter, Scott Anderson, and Franklyn Turbak.

Based on `codder` program by Ben Wood w/ contributions by Franklyn Turbak
and Peter Mawhorter.


## Dependencies

The core evaluation code depends on the `jinja2`, `pygments`, `markdown`,
`importlib_resources`, `beautifulsoup4`, and `python_dateutil` packages.

Optional dependencies (get them using e.g., `python -m pip install
potluck-eval[test]`):

- `[test]`: Tests depend on `pytest`, and you can run them using `tox` if
    you want.
- `[expectations]`: Integration with `optimism` is available to require
    and grade student unit tests.
- `[turtle_capture]`: Full support for capturing `turtle` drawings
    requires the `Pillow` package (version 6.0.0 or later), as well as a
    Ghostscript installation (which is not simply a PyPI package and
    needs to be installed manually). Support for other image-producing
    code is possible, but would also require `Pillow`.
- `[synth]`: Integration with `wavesynth` is available for capturing
    audio produced by that package. Support for other audio libraries
    is not built in but is possible.
- `[server]`: If you want to run the `potluck_server` WSGI app, you'll
    need `flask` and `flask_cas`, as well as `redis`. If you're running
    the WSGI app on a server without a windowing system but still want to
    be able to evaluate submissions that use graphics (notably
    submissions which use the `turtle` module), there is support for
    using `xvfb-run` (which would have to be installed separately as it's
    not a PyPI package).
- `[security]` For full server security, you should also install
    `flask_talisman`, and `flask_seasurf`, but these are not required for
    running the server and won't be used if they're not present (although
    this introduces some extra security vulnerabilities).
- `[https_debug]` If you want to use a self-signed certificate for HTTPS
    while hosting the WSGI server locally for debugging purposes, you'll
    need `pyopenssl`. This is inconvenient, so it's not recommended
    unless you want to develop the server side of things.
- `[formatting]` For better formatting of markdown instructions,
   `pymarkdown-extensions` can be installed; it will be used if present,
   and the most important feature it provides is indented fenced code
   blocks so that they can be placed into list items.


## Installing

To install from PyPI, run the following command on the command-line:

```sh
python3 -m pip install potluck-eval
```

Confirm installation from within Python by running:

```py
>>> import potluck
```

Once that's done, you can perform run the built-in tests on the
command-line:

```sh
python -m potluck.tests
```

Note that if you get a command not found error, the `potluck_eval` script
might not have been installed somewhere that's on your command line's
path, which you'll need to fix to get the tests to run.

If you want to see what evaluation looks like yourself instead of just
running automated tests that clean up after themselves, in your installed
`potluck` directory inside of `site-packages` there's a `testarea`
directory; inside `testarea/test_course/fall2021` you should be able to
run the following commands:

```sh
potluck_eval -t functionsTest --rubric
potluck_eval -t functionsTest --instructions
potluck_eval -t functionsTest -u perfect
potluck_eval -t functionsTest -u imperfect
potluck_eval -t functionsTest --check
```

The first command creates a rubric for the "functionsTest" task in the
`rubrics` directory, and the second creates instructions in the
`instructions` directory. The third and fourth commands will evaluate the
provided test submissions for the same task, creating reports as
`reports/(im)perfect/functionsTest_TIMESTAMP.html` where TIMESTAMP is a
time-stamp based on when you run the command. The fifth command runs the
specification's built-in tests and prints out a report.

If the tests pass and these commands work, then `potluck` is properly
installed and you can start figuring out how to set up your own
evaluation area and define your own tasks. The documentation for the
`potluck.specifications` module describes the task-definition process and
provides a worked example that shows off many of the possibilities; you
can find that example specification at:

`potluck/testarea/test_course/fall2021/specs/functionsTest/spec.py`


## Evaluation Setup

Once `potluck` is installed and working , you'll need to set up your own
folder for evaluating submissions. The `potluck/testarea` folder contains
an example of this, including task specifications and example
submissions (note that it's missing a `submissions` folder because all of
its submissions are examples, as the `potluck_config.py` there notes).
You can test things out there, but eventually you'll want to create your
own evaluation directory, which should have at minimum:

- `tasks.json`: This file specifies which tasks exist and how to load
  their specifications, as well as which submitted files to look for and
  evaluate. You can work from the example in
  `potluck/testarea/test_course/fall2021/tasks.json`.
- A `specs` folder with one or more task sub-folders, named by their task
  IDs. Each task sub-folder should have a `spec.py` file that defines the
  task, as well as `starter/` and `soln/` folders which hold starter and
  solution code. These files and folders need to match what's specified
  in `tasks.json`.
- A `submissions` folder, with per-user submissions folders containing
  per-task folders that have actual submitted files in them. Note that if
  you're going to use the `potluck_server` WSGI app, this can be created
  automatically.

If you're going to use the `potluck_server` WSGI app, your evaluation
directory will also need:

- `potluck-admin.json`: Defines which users have admin privileges and
  allows things like masquerading and time travel. Work from the provided
  example `potluck/testarea/test_course/fall2021/potluck-admin.json`.

Finally, to run automated tests on your specifications (always a good
idea) you will need:

- An `examples` folder with the same structure as the `submissions`
  folder.


## Running `potluck_server`

To set up `potluck_server`, in addition to an evaluation directory set up
as described above, you'll need to create a `ps_config.py` file in a
directory of your choosing (could be the same as the base evaluation
directory if you want); there's a `rundir` directory inside the installed
`potluck_server` directory which has an example of this; in addition to
`ps_config.py`, `secret` and `syncauth` files will be created in the
server run-directory if not present.

For testing purposes, you will not need to change the `ps_config.py` file
from the defaults supplied in `ps_config.py.example`, but you'll want to
edit it extensively before running the server for real. When running in a
real WSGI context, you'll also need the `potluck.wsgi` file that's
present in the `potluck_server/rundir` directory.

Once `ps_config.py` has been created, from the `potluck_server/rundir`
directory (or whatever directory you set up) you should be able to run:

```py
python -m potluck_server.app
```

to run the WSGI app on a local port in debugging mode. It will print
several messages including one or more prompts about running without
authentication, and you'll have to press enter at these prompts to
actually start the server, after which it should provide you with a link
you can use in a browser to access it.

NOTE THAT THE POTLUCK WEB APP ALLOWS AUTHENTICATED USERS TO RUN ARBITRARY
PYTHON CODE ON THE SERVER!

In addition to this, in debugging mode the server has no authentication,
and is only protected by the fact that it's only accessible to localhost.
Accordingly, you will need to set up CAS (Central Authentication Server)
via the values in `ps_config.py` to run the server for real. If you don't
have access to a CAS instance via your company or institution, you can
either set one up yourself, or you'll have to modify the server to use
some other form of authentication. It is also *strongly* recommended that
you install the `flask_talisman` and `flask_seasurf` modules, which will
be used to provide additional security only if they're available. If
`pyopenssl` is installed alongside `flask_talisman`, a self-signed
certificate will be used to provide HTTPS even in debugging mode, mostly
just to maximize similarity between debugging & production environments.

In debugging mode, you will automatically be logged in as the "test"
user, and with the default `potluck-admin.json` file, this will be an
admin account, allowing you to do things like view full feedback before
the submission deadline is past. With the default setup, you should be
able to submit files for the testing tasks, and view the feedback
generated for those files (eventually, you may have to modify the due
dates in the example `tasks.json` for this to work). You can find files
to submit in the `potluck/testarea/test_course/fall2021/submissions`
directory, and you can always try submitting some of the solution files.

See the documentation at the top of `python_server/app.py` for a run-down
of how the server works and what's available.

To actually install the server as a WSGI app, you'll need to follow the
standard procedure for whatever HTTP server you're using. For example,
with Apache, this involves installing mod_wsgi and creating various
configuration files. An example Apache mod_wsgi configuration might look
like this (to be placed in `/etc/httpd/conf.d`):

```cfg
# ================================================================
# Potluck App for code submission & grading (runs potluck_eval)

# the following is now necessary in Apache 2.4; the default seems to be to deny.
<Directory "/home/potluck/private/potluck/potluck_server">
    Require all granted
</Directory>

WSGIDaemonProcess potluck user=potluck processes=5 display-name=httpd-potluck home=/home/potluck/rundir python-home=/home/potluck/potluck-python python-path=/home/potluck/rundir
WSGIScriptAlias /potluck /home/potluck/rundir/potluck.wsgi process-group=potluck
```


## Security

Running the potluck_server WSGI app on a public-facing port represents a
significant security vulnerability, since any authenticated user can
submit tasks, and the evaluation mechanisms currently do not use any
sandboxing, meaning that they RUN UNTRUSTED PYTHON CODE DIRECTLY ON YOUR
SERVER (even if they used sandboxing, which is a target feature for the
future, they would be vulnerable to any means of circumventing the
sandboxing used).

You therefore need to trust that your CAS setup is secure, and trust that
your users will be responsible about submitting files and about keeping
their accounts secure. If you can't depend on these things, DO NOT run
the web app.

Even if you do not run the web app, and instead collect submissions via
some other mechanism, the evaluation machinery still runs submitted code
directly. You will need to trust the users submitting tasks for
evaluation, and watch out for accidental mis-use of resources (e.g.,
creating files in an infinite loop). It's not a bad idea to run the
entire evaluation process in a virtual machine, although the details of
such a setup are beyond this document.


## Documentation

Extracted documentation can be viewed online at:
[https://cs.wellesley.edu/~pmwh/potluck/docs/potluck/](https://cs.wellesley.edu/~pmwh/potluck/docs/potluck/)

You can also read the same documentation in the docstrings of the source
code, or compile it yourself if you've got `make` and `pdoc` installed by
running the `make docs` script on the command-line (note that shenanigans
are necessary to prevent pdoc from trying to import the test
submissions).

## Changelog

- Version 1.2.36 cleans up a few minor things and adds config for
  disabling self-granted extensions at the course level. Also adds
  'pastecanary' CSS support for hidden text that gets 'added in' when
  copy-pasted. This is `potluck` version 1.2.16 and `potluck_server`
  version 1.2.24.
- Version 1.2.35 improves handling of long experience answers in the
  grade sheets, improves sorting when multiple course numbers are present
  in the roster, and makes grades more visible on the dashboard (before
  the due date) and on the evaluation page. It bumps `potluck_server` to
  1.2.23. It also fixes some bugs:
    * A bug with Loop checks that require list comprehensions
      specifically.
    * A bug with harness descriptions that grabs the wrong paragraphs.
  This bumps `potluck` to version 1.2.25.
- Version 1.2.34 disables self-granted extensions, bumping
  `potluck_server` to 1.2.22.
- Version 1.2.33 replaces `AllOnes` with `ManyOnes(1000)` for input when
  importing modules, allowing us to crash earlier when a module requests too
  much input on import (typically none should be requested!). This also bumps
  `potluck` version to 1.1.24
- Version 1.2.32 tweaks `potluck_eval` resource limits to fail more gracefully
  in several cases.
- Version 1.2.31 brings potluck adds resource limits in the `potluck_eval`
  script. These should probably be confiurable, but for now it's all-or-nothing
  based on a switch.
- `potluck_eval` version 1.2.30 adds the missing 'redis' dependency into
  the 'server' extra dependencies, and adds an 'all' extra dependency
  that includes all optional depedencies. It also includes
  `potluck_server` version 1.2.21 which fixes str/bytes flask_seasurf
  issue on Python 3, and specifies utf-8 encoding for file reading in
  `storage.py` to hopefully fix decoding issues with 'ascii' default
  locales. Makes `importlib_resources` import optional on Python versions
  that have `importlib.resources` built-in.
- `potluck_eval` version 1.2.29 is `potluck_server` version 1.2.20 which
  disables authentication for the starter code download route.
- `potluck_eval` version 1.2.28 fixes the CSS highlighting issue in
  exercise extension forms in the extension manager. It also adds support
  for universal tracing. This is `potluck_server` version 1.2.20 and
  `potluck` version 1.2.23.
- `potluck_eval` version 1.2.27 fixes column alignment in copied table
  contents for gradesheets. This is `potluck_server` version 1.2.19.
- `potluck_eval` version 1.2.26 adds grade override mechanisms for
  individual exercises and for exercise groups. This is `potluck_server`
  version 1.2.18.
- `potluck_eval` version 1.2.25 fixes a print formatting bug, and also
  has an ugly patch for the image-tabs-don't-work bug in image comparison
  feedback. It's `potluck` version 1.1.22.
- `potluck_eval` version 1.2.24 fixes a bug in 1.2.23 that prevents
  exercise detail views from working entirely; this is `potluck_server`
  version 1.2.17.
- `potluck_eval` version 1.2.23 adds a chronological list of all exercise
  submissions to the exercise detailed view; this is `potluck_server`
  version 1.2.16.
- `potluck_eval` version 1.2.22 fixes percentage displays on the full
  gradesheet, adds category classes to them for color. Also shortens
  grade item titles to regularize column widths in the full grade table,
  and hides students whose section is set to "__hide__", along with
  exercise groups and/or projects which have "hide" set to true. This is
  `potluck_server` version 1.2.15.
- `potluck_eval` version 1.2.21 fixes some JS issues (like +24h buttons
  not working on evaluation pages) and adds a full-course gradesheet view
  (link is on the dashboard before the quick links for admins). This is
  `potluck_server` version 1.2.14 and `potluck` version 1.1.20.
- `potluck_eval` version 1.2.20 fixes one bug in 1.2.19. It includes
  `potluck_server` version 1.2.13.
- `potluck_eval` version 1.2.19 fixes bugs in 1.2.18. It includes
  `potluck_server` version 1.2.12.
- `potluck_eval` version 1.2.18 fixes bugs in 1.2.17. It includes
  `potluck_server` version 1.2.11.
- `potluck_eval` version 1.2.17 includes `potluck` version 1.1.19 and
  `potluck_server` version 1.2.10 which clarify/simplify the "at
  least N" messages for partial completion language and also show full
  eval info before the initial deadline to get rid of the "at least
  partially complete" confusing language. The new potluck_server version
  also empowers config values, letting them come from per-course task
  info in almost all cases, and in many cases letting them come from
  individual tasks, projects, or exercise groups within a tasks.json
  file. Server config and defaults in the code still provide default
  values.
- `potluck_eval` version 1.2.16 includes `potluck_server.storage` version
  0.3.1 which fixes a bug in v0.3 that always causes an internal server
  error. I need a better testing setup T_T
- `potluck_eval` version 1.2.15 includes `potluck_server.storage` version
  0.3. Turns out I hadn't been version bumping that file for a while even
  though plenty of changes have occurred ^.^; In any case, this fixes a
  bug that resulted in an internal server error when certain None grade
  values were explicit.
- `potluck_eval` version 1.2.14 includes `potluck` version 1.1.18 which
  adds a return to `capture_file_contents` for chaining.
- `potluck_eval` version 1.2.13 includes `potluck_server` version 1.2.9;
  it's a bugfix for issues in 1.2.8.
- `potluck_eval` version 1.2.12 includes `potluck_server` version 1.2.8,
  which fixes exercise deadline handling so that extensions (and other
  deadline adjustments) can retroactively change the lateness of
  particular exercise submissions.
- `potluck_eval` version 1.2.11 fixes a bug where the extension manager
  would show initial extension values from the person viewing the page,
  not from the student whose extensions were being managed (student
  extension values were still saved properly). It also fixes a floating
  point division error for servers running Python 2.7 which causes
  inaccurate pset combined grades to show up in some cases on the
  gradesheet. It also sets the default expectation level in the `meta`
  submodule to 0 to work with the new flat reports that are sortable. It
  also adds sorting functionality to reports instead of just
  instructions/rubrics.
- `potluck_eval` version 1.2.10 makes the `amend_exercises` function more
  robust in the face of missing credit info.
- `potluck_eval` version 1.2.9 ensures that the exercises route displays
  exercises for the target user, not the logged-in user. Also adds a
  mechanism for hiding psets from the dashboard via tasks.json. Also adds
  extension management for exercises, and factors deadlines into points
  calculations for exercises. Also adds exercise IDs to the dashboard.
- `potluck_eval` version 1.2.8 fixes an integer-point division issue in
  computing credit fractions when running the server on Python 2. It also
  adds solution links for exercise groups to be displayed only after the
  deadline to those who have a "complete" or better evaluation. Added
  gradesheet views for exercise groups. Added +/- 24-hour buttons for
  extensions in the extension manager.
- `potluck_eval` version 1.2.7 adds a stderr error message to the
  potluckDelivery output when the server indicates that a submission is
  not complete, and redirects GET requests to `route_deliver` to the
  dashboard. It also adds percentages to the dashboard for exercise
  groups, updates the exercise format within exercise groups in
  tasks.json to a list of dictionaries so that ordering is preserved. The
  former dictionary-of-exercises format won't crash things but isn't
  fully supported any more.
- `potluck_eval` version 1.2.6 fixes a bug in 1.2.5 with safe_join that
  affects older versions of Python/werkzeug/flask. It also pushes
  `potluck` version to 1.1.16, which adds custom categorization to the
  rubric and makes a flat metric the default. This breaks some of the
  prep stuff but we'll fix that later.
- `potluck_eval` version 1.2.5 fixes a bug in 1.2.4 that should have been
  caught by basic testing T_T.
- `potluck_eval` version 1.2.4 disables CSRF for route_deliver and also
  fixes some python2-specific errors with deliver and improves some
  delivery error messages. It also gets rid of outcome-count-checking
  when outcome counts aren't specified in `tasks.json`, and introduces an
  author info timeout for `potluckDelivery`. Plus, `deliverOutcome` will
  now automatically grab code with a mark matching the suite name even if
  `grabCode` isn't specified, as long as `optimism` is available.
  Finally, an attempt was made to improve backward compatibility for
  cases where 'exercises' may not be defined in `tasks.json`, and/or
  where the concepts file is missing.
- `potluck_eval` version 1.2.3 re-fixes the flashes-instead-of-errors idea
  form 1.2.2 that still wasn't implemented correctly. It also introduces
  timeliness overrides and puts timing info below problem set IDs to save
  space on the dashboard.
- `potluck_eval` version 1.2.2 fixes the flashes-instead-of-errors idea
  form 1.2.1 that wasn't implemented correctly.
- `potluck_eval` version 1.2.1 adds a version number to the
  `potluckDelivery` script. It also turns some exceptions into flashes
  for missing concepts in exercise configuration to make typos less
  punishing.
- `potluck_eval` version 1.2 brings things up-to-date with optimism
  2.7.4, and represents a major shakeup to the potluck server's handling
  of grades + feedback, hence the new minor version number. Full feedback
  is now displayed during the initial submission period, and timeliness
  points separate from task points are assigned based on presence/absence
  of an initial submission and an eventual at-least-almost-complete
  revision (or initial submission). It improves display for finalized
  unsubmitted pooled tasks (no longer marked as issues if any task in the
  pool was submitted). It also adds a file `potluckDelivry` for
  delivering exercise results via function call, and a whole exercise
  category on the dashboard w/ details view to collect, store, and
  display those results. Gradesheet for exercises is not present yet, but
  should be coming along soon.
- `potluck` version 1.1.14 makes single-loop dictionary and set
  comprehensions matchable with a default Loop object, and adds set
  comprehensions to the relevant pattern variables.
- `potluck` version 1.1.13 upgrades the `returns_a_new_value` harness to
  match the `report_argument_modifications` harness in reporting
  positions of arguments rather than their names.
- `potluck` version 1.1.12 includes `Try` and `With` `Check` sub-classes
  in `specifications.py` (although these have severe limitations) and
  fixes `validation.py` to be up-to-date with `optimism` version 2.6.4.
  It also sets the default subslip to be equal to the number of
  sub-rules, meaning that by default, any match is considered partial if
  the syntax we're looking for was found. It also adds some tests for
  try/with matching to the `mast` tests, including one that fails for now
  because pattern vars in the 'as -name-' position of an except block
  aren't supported. Try/except matching in general is extremely
  fragile...
- `potluck` version 1.1.11 includes better support for testing optimism
  tests cases defined within specific functions, via a testing harness in
  the `validation` sub-module.
- `potluck` version 1.1.10 includes generator expressions and dictionary
  comprehensions when matching loops generally and comprehensions
  specifically. The wording of rubrics for these is also improved. Also
  sets the default behavior of `DontWasteBoxes` to ignore loop variables.
- Version 1.0/1.1 brings potluck up-to-date with optimism 2.0, and adds a
  validation mode for checking test cases against solution code. Some
  improvements to resubmission and admin-based submission on the server
  are also included.
