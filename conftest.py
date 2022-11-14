import time
import pytest
import logging
from datetime import datetime

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)
    #
    # outcome = yield
    # report = outcome.get_result()
    #
    # if report.when == "call":
    #
    #     xfail = hasattr(report, "wasxfail")
    #     if (report.skipped and xfail) or (report.failed and not xfail):
    #         logging.info("!!TEST FAILED!!")
    #     else:
    #         logging.info("**TEST SUCCEED**")

@pytest.fixture(scope="class")
def login():
    logging.info("conftest login")
    time.sleep(5)
    yield
    logging.info("conftest login teardown")

@pytest.fixture
def test_logger(request):
    test_name = request.node.name
    node_id = request.node.nodeid
    start_time = datetime.now()
    yield
    logging.info(f"test_name: {test_name}, node_id: {node_id}")

    end_time = datetime.now()
    elapsed_time = str((end_time - start_time).total_seconds())
    logging.info(f"test start_time: {start_time}, end time: {end_time}, elapsed_time: {elapsed_time}")

    if request.node.rep_setup.failed:
        logging.info("test result: failed on setup")
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            logging.info("test result: failed on running")
    if request.node.rep_call.passed:
        logging.info("test result: test passed")

