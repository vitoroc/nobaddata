from nobaddata.models.result import CheckResult
from nobaddata.reporting.reporter import Reporter


def test_reporter_basic_output():
    results = [
        CheckResult(
            check_name="null_check_email", status="PASS", severity="WARNING", details={}
        ),
        CheckResult(
            check_name="duplicate_check_user_id",
            status="FAIL",
            severity="WARNING",
            details={"duplicate_count": 2},
        ),
    ]

    reporter = Reporter()

    output = reporter.render(results)

    assert "null_check_email" in output
    assert "duplicate_check_user_id" in output
    assert "✔" in output
    assert "✖" in output


def test_reporter_pass_with_details():
    results = [
        CheckResult(
            check_name="null_check_email",
            status="PASS",
            severity="WARNING",
            details={"null_count": 0},
        )
    ]

    reporter = Reporter(show_details=True)

    output = reporter.render(results)

    assert "null_check_email" in output
    assert "✔" in output
    assert "null_count=0" in output


def test_reporter_fail_without_details():
    results = [
        CheckResult(
            check_name="duplicate_check_user_id",
            status="FAIL",
            severity="WARNING",
            details={},
        )
    ]

    reporter = Reporter(show_details=False)

    output = reporter.render(results)

    assert "duplicate_check_user_id" in output
    assert "✖" in output
    assert "|" not in output


def test_reporter_error_status():
    results = [
        CheckResult(
            check_name="range_check_age", status="ERROR", severity="WARNING", details={}
        )
    ]

    reporter = Reporter()

    output = reporter.render(results)

    assert "range_check_age" in output
    assert "⚠" in output
