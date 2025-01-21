"""
Machinery for defining requirements for tests. Tests are submitted in a
separate file using the `optimism` library, and we can require a certain
number of distinct test trials that target specific functions/files, and
require that all of the checks succeed.

The validation machinery runs the submitted tests file in a directory
with the solution code and checks what test trials it checks and whether
those checks succeed. `rubrics.Rubric.validate_tests` can then be used
to generate a report based on all validation goals; the goals in this
file should normally be used as validation goals, not evaluation goals.
"""

from . import rubrics
from . import contexts
from . import context_utils
from . import phrasing
from . import html_tools


#---------------------------------------------------#
# Goal subtypes for checking file-level test trials #
#---------------------------------------------------#

class TrialsTest(rubrics.Goal):
    """
    Runs a function against the auto-context for "validation_test_trials".
    Inherit and override the `check` method with a function that accepts
    a context and returns a goal evaluation result to define your test.

    Note that these can only be used when the 'optimism' module is
    available.
    """
    def check(self, context):
        """
        Not implemented; override to define specific tests.
        """
        raise NotImplementedError(
            "TrialsTest is an abstract class that can't be used"
            " directly."
        )

    def __init__(
        self,
        taskid,
        identifier,
        description=(
            "BLANK EXPECTATIONS TEST",
            "THIS GOAL HAS NOT BEEN DEFINED"
        ),
        goal_type="testing",
        uses_slots=("validation_test_trials",),
        **kwargs
    ):
        """
        In addition to a task ID, an identifier, and a description, a
        goal type may be supplied other than the default "testing".

        The categorizer "tests:" will be prepended to the given
        identifier.

        The slots required should be given as uses_slots, and a relevant
        context will be selected or created as the testing context. By
        default the "validation_test_trials" slot is the only one used.

        Any extra arguments are passed through to the `rubrics.Goal`
        constructor.
        """
        # Auto context dependency based on uses_slots
        depends = contexts.auto(*uses_slots)
        if len(depends) == 1:
            test_context = depends[0]
        else:
            # TODO: De-duplicate stuff where one context actually
            # provides everything needed via inheritance but auto
            # doesn't see that?
            test_context = contexts.Context(
                description=(
                    "Test trials defined by your code",
                    (
                        "The " + phrasing.comma_list(
                            slot.replace("_", " ")
                            for slot in uses_slots
                        )
                      + " of your code."
                    )
                ),
                builder=lambda ctx: ctx,
                depends=depends
            )

        if "test_in" not in kwargs:
            kwargs["test_in"] = {}
        if "contexts" not in kwargs["test_in"]:
            kwargs["test_in"]["contexts"] = [ test_context ]

        # Specified goal type
        if "tags" not in kwargs:
            kwargs["tags"] = {}
        kwargs["tags"]["goal_type"] = goal_type

        # Set up rubrics.Goal stuff
        super().__init__(
            taskid,
            "tests:" + identifier,
            description,
            **kwargs
        )

    # subgoals is inherited (no subgoals)

    # table is inherited

    def evaluate_in_context(self, context=None):
        """
        Runs the checker and returns its result.
        """
        context = context or {}

        try:
            self.result = self.check(context)

            if self.result is None:
                raise ValueError(
                    f"Test trial check for {self.__class__.__name__}"
                    f" returned None!"
                )
        except Exception:
            self.result = {
                "status": "failed",
                "traceback": html_tools.html_traceback(
                    linkable=context_utils.linkmap(context)
                )
            }
            self.set_explanation(
                context,
                status="crash",
                default=html_tools.html_traceback(
                    title="Error while checking your test trials.",
                    linkable=context_utils.linkmap(context)
                )
            )
            return self.result

        self.set_explanation(
            context,
            default=self.result["explanation"]
        )

        return self.result


class DefinesEnoughTests(TrialsTest):
    """
    A test trials checker which ensures that for each of certain listed
    functions (or files), a certain number of distinct test trials are
    established (using the `optimism` module).

    Note that functions are specified by name to be matched against
    __name__ attributes of actual functions checked, so if you're testing
    methods you just use the method name, and testing decorated functions
    may be tricky. (TODO: Check if this plays nicely with spec-specified
    decorations.)

    Test trials are counted as distinct if either their arguments or their
    provided inputs differ.
    """
    def __init__(self, taskid, function_reqs, file_reqs, **kwargs):
        """
        A task ID is required. The other required arguments are two
        dictionaries mapping function name strings and then filename
        strings to integers specifying how many tests are required.

        Other arguments get passed through to `TrialsTest` and
        potentially thence to `rubrics.Goal`.

        The identifier will be "defines_enough".
        """
        self.function_reqs = function_reqs
        self.file_reqs = file_reqs

        # Check types for function requirements keys and values
        for fname in function_reqs:
            if not isinstance(fname, str):
                raise TypeError(
                    (
                        "Each function requirement must be a string."
                        " (You used {} as a key, which is a {})."
                    ).format(
                        repr(fname),
                        type(fname)
                    )
                )

            val = function_reqs[fname]
            if not isinstance(val, int):
                raise TypeError(
                    (
                        "Each function requirement must use an integer"
                        " as the value. (requirement with key {} had"
                        " value {} which is a {})."
                    ).format(
                        repr(fname),
                        repr(val),
                        type(val)
                    )
                )

        # Check types for file requirements keys and values
        for filename in file_reqs:
            if not isinstance(filename, str):
                raise TypeError(
                    (
                        "Each file requirement must be a string."
                        " (You used {} as a key, which is a {})."
                    ).format(
                        repr(filename),
                        type(filename)
                    )
                )

            val = file_reqs[filename]
            if not isinstance(val, int):
                raise TypeError(
                    (
                        "Each file requirement must use an integer as"
                        " the value. (requirement with key {} had"
                        " value {} which is a {})."
                    ).format(
                        repr(filename),
                        repr(val),
                        type(val)
                    )
                )

        # Check if optimism is available
        try:
            import optimism # noqa F401
        except Exception:
            raise NotImplementedError(
                "DefinesEnoughTests cannot be used because the"
                " 'optimism' module cannot be imported."
            )

        # Set automatic description
        if "description" not in kwargs:
            rlist = [
                "Function <code>{}</code>: {} trials".format(
                    fn,
                    required
                )
                for fn, required in self.function_reqs.items()
            ] + [
                "File '{}': {} trials".format(
                    filename,
                    required
                )
                for filename, required in self.file_reqs.items()
            ]
            kwargs["description"] = (
                "Defines required test trials",
                (
                    """\
Your code must use the <code>optimism</code> module to create a certain
number of test trials which use the following functions/files. Test trials
that are the same as each other (same arguments and/or inputs) don't
count. (Each test trial must include at least one check).\n"""
                  + html_tools.build_list(rlist)
                )
            )

        super().__init__(taskid, "defines_enough", **kwargs)

    def check(self, context):
        """
        Looks for an adequate number of established test trials in the
        given context that have recorded checks.
        """
        try:
            import optimism
        except Exception:
            raise NotImplementedError(
                "Cannot check for test trials because optimism cannot be"
                " imported."
            )
        trials = context_utils.extract(context, "validation_test_trials")
        by_fn = {}
        by_file = {}
        for trial in trials:
            # Skip test trials that have not been checked
            if len(trial.outcomes) == 0:
                continue

            # Categorize by function/file tested
            if issubclass(trial.manager.case_type, optimism.FunctionCase):
                fname = trial.manager.target.__name__
                add_to = by_fn.setdefault(fname, [])

                # Don't record duplicate trials
                duplicate = False
                for recorded in add_to:
                    if (
                        trial.args == recorded.args
                    and trial.kwargs == recorded.kwargs
                    and trial.inputs == recorded.inputs
                    ):
                        duplicate = True
                        break

                # Record this trial
                if not duplicate:
                    add_to.append(trial)

            elif issubclass(trial.manager.case_type, optimism.FileCase):
                add_to = by_file.setdefault(trial.manager.target, [])

                # Don't record duplicate trials
                duplicate = False
                for recorded in add_to:
                    if (
                        trial.args == recorded.args
                    and trial.kwargs == recorded.kwargs
                    and trial.inputs == recorded.inputs
                    ):
                        duplicate = True
                        break

                # Record this trial
                if not duplicate:
                    add_to.append(trial)

            # Note that we ignore other kinds of trials including block
            # trials, which would be hard to count/require...

        any_tests = False
        deficient = False
        reports = []
        for req_file, required in self.file_reqs.items():
            trials = by_file.get(req_file, [])
            count = len(trials)

            if count > 0:
                any_tests = True

            if count < required:
                deficient = True
                symbol = '✗'
            else:
                symbol = '✓'

            reports.append(
                f"{symbol} '{req_file}': {count} / {required}"
            )

        for req_fn, required in self.function_reqs.items():
            trials = by_fn.get(req_fn, [])
            count = len(trials)

            if count > 0:
                any_tests = True

            if count < required:
                deficient = True
                symbol = '✗'
            else:
                symbol = '✓'

            reports.append(
                f"{symbol} <code>{req_fn}</code>: {count} / {required}"
            )

        if not any_tests:
            return {
                "status": "failed",
                "explanation": (
                    "Running your module did not establish any test"
                    " trials for required functions or files."
                )
            }
        elif deficient:
            return {
                "status": "partial",
                "explanation": (
                    "Your module did not establish as many test trials as"
                    " were required for all functions/files:\n"
                ) + html_tools.build_list(reports)
            }
        else:
            return {
                "status": "accomplished",
                "explanation": (
                    "Your module established enough test trials for each"
                    " function or file it was required to test."
                )
            }


def list_trial_outcomes(trials):
    """
    Creates an HTML list out of test trial objects.
    """
    items = []
    for trial in trials:
        for (passed, tag, message) in trial.outcomes:
            short_tag = tag.split('/')[-1]
            message = html_tools.escape(message)
            lines = message.splitlines()
            lines[0] = lines[0][:2] + lines[0].split('/')[-1]
            message = html_tools.wrap_text_with_indentation(
                '\n'.join(lines)
            )
            items.append(f"✗ {short_tag}<br><pre>{message}</pre>")
    return html_tools.build_list(items)


class ChecksSucceed(TrialsTest):
    """
    An test trial checker which ensures that each recorded outcome for
    each established test trial in the submitted testing module is a
    success.

    Note that when this goal is checked during validation, tests in the
    "validation_test_trials" slot have been run against the solution
    code, whereas when this goal is used during evaluation, those same
    test trials have been run against the student's submitted code.

    TODO: Manage multi-file submission and/or test file copying so that
    "validation_test_trials" is actually available during evaluation.
    """
    def __init__(self, taskid, **kwargs):
        """
        A task ID is required. Arguments are passed through to
        `TrialsTest`.

        The identifier will be "checks_succeeded".
        """

        try:
            import optimism # noqa F401
        except Exception:
            raise NotImplementedError(
                "ChecksSucceed cannot be used because the 'optimism'"
                " module cannot be imported."
            )

        if "description" not in kwargs:
            kwargs["description"] = (
                (
                    "All checks must succeed"
                ),
                (
                    "Every time your code checks a test trial using the"
                    " <code>optimism</code> module the check must"
                    " succeed."
                )
            )

        super().__init__(taskid, "checks_succeeded", **kwargs)

    def check(self, context):
        """
        Looks for any failed outcomes in test trials within the given
        context.
        """
        trials = context_utils.extract(context, "validation_test_trials")
        any_failed = False
        any_passed = False
        failing = []
        for trial in trials:
            failed_here = False
            for (succeeded, tag, msg) in trial.outcomes:
                if succeeded:
                    any_passed = True
                else:
                    failed_here = True

            if failed_here:
                any_failed = True
                failing.append(trial)

        if any_failed:
            fail_list = list_trial_outcomes(failing)
            if any_passed:
                return {
                    "status": "partial",
                    "explanation": (
                        "Some of your code's checks failed:\n"
                    ) + fail_list
                }
            else:
                return {
                    "status": "failed",
                    "explanation": (
                        "None of your code's checks succeeded:\n"
                    ) + fail_list
                }
        else:
            if any_passed:
                return {
                    "status": "accomplished",
                    "explanation": (
                        "All of your code's checks succeeded."
                    )
                }
            else:
                return {
                    "status": "failed",
                    "explanation": (
                        "Your code did not check any test trials."
                    )
                }


#---------------------------------------------------#
# Harnesses for checking function-level test trials #
#---------------------------------------------------#

def check_tests_harness(
    function,
    *args,
    _req_trials=None,
    _must_pass=True,
    **kwargs
):
    """
    A test harness (to be used with
    `potluck.specifications.test_with_harness`) which will return a
    string reporting on the aggregate behavior of `optimism` tests that
    were defined and checked as a result of running a particular
    function. A minimum number of distinct `optimism` test trials can be
    required for each of certain target functions, and that those test
    trials must pass all checks applied (this second check can be skipped
    by setting `_must_pass` to `False`).

    If `_must_pass` is set to the string "all", then all tests must
    pass, even if more than the required number of tests are defined,
    otherwise enough tests must pass (i.e., have been checked at least
    once and have succeeded on every check applied) to meet the minimum
    requirements, but cases beyond those are allowed to fail. If
    `_must_pass` is set to the string "not all" then at least one test
    must fail, but the specific number of successes/failures is not
    reported.

    Note that this function has a side effect of deleting all
    previously-defined optimism tests.

    The `_req_trials` argument must be a dictionary mapping function names
    to integers specifying how many distinct trials (checks and/or test trials)
    are required for that function. Tests for files can be required by
    prepending 'file:' to the filename to require tests for, and code block
    tests can be required by prepending 'block:' to the exact code block string
    (but that's quite fragile). If `_req_trials` is None (the default) then the
    report will include information on all defined tests.

    As a harness function, most arguments are passed through to whatever
    function is being tested; if that function has arguments named
    `_req_trials` and/or `_must_pass` you'll have to define your own
    custom harness that uses different keyword argument names. Because
    positional arguments are passed through, these two meta-parameters
    must be given as keyword arguments.

    Note that technically, if the solution code has failing test trials,
    when `_must_pass` is set to "all" the reports produced will be the
    same if the submitted code fails the same number of test trials.

    (Note: these docstring paragraphs will be used as the default goal
    description...)
    """
    # Check if optimism is available
    try:
        import optimism # noqa F401
    except Exception:
        raise NotImplementedError(
            "check_tests_harness cannot be used because the"
            " 'optimism' module cannot be imported."
        )

    # First clean up any existing tests
    optimism.deleteAllTestSuites()

    # Run the function, ignoring its result
    function(*args, **kwargs)

    # List all currently defined test trials (i.e., those defined by the
    # function we're looking at)
    defined = optimism.listAllTrials()

    report = ""

    # Check each defined trial and create a map of the number of passing
    # and failing trials for each function/file/block tested; as a side
    # effect add lines to the report detailing any failing trials if
    # _must_pass is set to "all".
    trialMap = {}
    for trial in defined:
        # Figure out the trial ID
        if isinstance(trial.manager, optimism.FunctionManager):
            trial_id = trial.manager.target.__name__
            show_trial_id = "function:" + trial_id
        elif isinstance(trial.manager, optimism.FileManager):
            trial_id = "file:" + trial.manager.target
            show_trial_id = trial_id
        elif isinstance(trial.manager, optimism.BlockManager):
            trial_id = "block:" + trial.manager.target
            show_trial_id = "block:" + repr(trial.manager.target)
        else:
            trial_id = None
            show_trial_id = "unknown"

        trialMap.setdefault(trial_id, [show_trial_id, 0, 0])

        # Go through each outcome
        n_failed = 0
        n_checks = 0
        for passed, _, _ in trial.outcomes:
            n_checks += 1
            if not passed:
                n_failed += 1

        if n_checks > 0 and n_failed == 0:
            # All checks passed, and there was at least one
            # This counts as a passing trial
            trialMap[trial_id][1] += 1

        elif n_failed > 0:
            # some checks failed
            # Record the failure
            trialMap[trial_id][2] += 1
            if _must_pass == "all":
                # Note failure in our report, but don't include specific
                # line numbers, since those might differ between
                # submitted and solution files
                report += (
                    f"{n_failed} checks failed for test(s) of"
                    f" {show_trial_id}\n"
                )

    # Check that the required number trials are present
    if _req_trials is None:
        # Report on every defined test
        for (trial_id, (show_trial_id, succeeded, failed)) in trialMap.items():
            # Skip trials where no checks were performed
            if succeeded + failed == 0:
                continue

            if _must_pass is True and succeeded == 0:
                # if _must_pass is 'all' we've already reported failures
                report += (
                    f"{failed} {phrasing.plural(failed, 'check')} failed"
                    f" for test(s) of {show_trial_id}\n"
                )
            elif _must_pass:
                # report success
                report += (
                    f"At least one check succeeded for test(s) of"
                    f" {show_trial_id}\n"
                )
            else:
                # must_pass must be False, so we just report that checks
                # were defined regardless of success/failure
                report += (
                    f"Performed at least one check for test(s) of"
                    f" {show_trial_id}\n"
                )
    else:
        # Just report on required tests
        for req, threshold in _req_trials.items():
            show_trial_id, succeeded, failed = trialMap.get(
                req,
                [repr(req), 0, 0]
            ) # TODO: More elegant here?
            if _must_pass:
                if succeeded >= threshold:
                    trials_passed = phrasing.plural(
                        threshold,
                        'trial passed',
                        'trials passed'
                    )
                    report += (
                        f"At least {threshold} {trials_passed} for"
                        f" test(s) of {show_trial_id}\n"
                    )
                else:
                    trials_passed = phrasing.plural(
                        succeeded,
                        'trial passed',
                        'trials passed'
                    )
                    total = succeeded + failed
                    if total == succeeded:
                        trials_passed = phrasing.plural(
                            total,
                            'trial was defined',
                            'trials were defined'
                        )
                    only = "Only " if succeeded > 0 else ""
                    out_of = f"/{total}" if total > succeeded else ""
                    report += (
                        f"{only}{succeeded}{out_of} {trials_passed} for"
                        f" test(s) of {show_case_id} ({threshold} were"
                        f" required)\n"
                    )
            else:
                if succeeded + failed >= threshold:
                    trials_were = phrasing.plural(
                        threshold,
                        'trial was',
                        'trials were'
                    )
                    report += (
                        f"At least {threshold} {trials_were} defined"
                        f" for {show_trial_id}\n"
                    )
                else:
                    total = succeeded + failed
                    trials_were = phrasing.plural(
                        total,
                        'trial was',
                        'trials were'
                    )
                    only = "Only " if total > 0 else ""
                    report += (
                        f"{only}{total} {trials_were} defined for"
                        f" {show_trial_id} ({threshold}"
                        f" {phrasing.plural(threshold, 'was', 'were')}"
                        f" required)\n"
                    )

    # We return our report, to be compared with the same report when run
    # against the solution code
    return report


def tests_report_description(target_fn, _req_trials=None, _must_pass=True):
    """
    Returns a goal description tuple suitable for use with
    `specifications.HasGoal.set_goal_description` when
    `test_with_harness` has been used to set up `check_tests_harness` as
    the testing harness. Pass the same target function and keyword
    arguments used with the test harness (i.e., which were included in
    the test trial).

    TODO: Option for generic version when multiple test trials are grouped?
    """
    if _req_trials is None:
        if _must_pass == "all":
            return (
                (
                    "Must define and successfully check"
                    " <code>optimism</code> test trials for the correct"
                    " functions."
                ),
                (
                    "Your code must define and check"
                    " <code>optimism</code> test trials for each"
                    " function, file, or code block that the solution"
                    " code does. The number of test trials that fail at"
                    " least one check must match the solution results"
                    " (usually this means no check should fail)."
                )
            )
        elif _must_pass is True:
            return (
                (
                    "Must define and check <code>optimism</code> test"
                    " trials for the correct functions."
                ),
                (
                    "Your code must define and check"
                    " <code>optimism</code> test trials for each"
                    " function, file, or code block that the solution"
                    " code does. At least one check must succeed for"
                    " each test trial defined by the solution code."
                )
            )
        else:
            return (
                (
                    "Must define and check <code>optimism</code> test"
                    " trials for the correct functions."
                ),
                (
                    "Your code must define and check"
                    " <code>optimism</code> test trials for each"
                    " function, file, or code block that the solution"
                    " code does. It does not matter if the checks"
                    " succeed or fail as long as at least one check is"
                    " performed per test trial."
                )
            )
    else:
        # Build a list of strings describing per-trial-id requirements
        checklist = []
        for req, threshold in _req_trials.items():
            if req.startswith('block:'):
                show_trial = (
                    f"the code block <pre><code>{req[6:]}</code></pre>"
                )
            elif req.startswith('file:'):
                show_trial = f"the file '{req[5:]}'"
            else:
                show_trial = f"the function {req}"

            if _must_pass:
                checklist.append(
                    f"All checks must pass for at least {threshold}"
                    f" test {phrasing.plural(threshold, 'trial')} for"
                    f" {show_trial}."
                )
            else:
                checklist.append(
                    f"At least {threshold} test"
                    f" {phrasing.plural(threshold, 'trial')} for"
                    f" {show_trial} must be defined, and each must"
                    f" include at least one check (which does not have"
                    f" to succeed)."
                )

        # Construct detail text
        details = ""
        if checklist:
            details += (
                f"The following test trial(s) must be established by your"
                f" <code>{target_fn}</code> function and/or must"
                f" succeed:"
            )
            details += html_tools.build_list(checklist)

        elif _must_pass != "all":
            # If there are no listed checks, but _req_trials is not None,
            # you'll need to craft a custom description yourself
            raise ValueError(
                "_req_trials did not include any required test trials. You"
                " should fix that or use a custom description."
            )

        if _must_pass == "all":
            details += (
                "The same number of checks (usually zero) must fail for"
                " the same test trials as the solution code."
            )

        return (
            (
                f"Your <code>{target_fn}</code> function must establish"
                f" the correct test trials."
            ),
            details
        )
