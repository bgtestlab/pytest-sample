import time
import pytest
import logging

@pytest.fixture
def prepare():
    logging.info("called")
    yield
    logging.info("teardown")

@pytest.mark.usefixtures("test_logger")
class TestSample:
    @pytest.fixture(scope="class")
    def class_scope(self):
        logging.info("called")
        yield
        logging.info("teardown")

    @pytest.fixture
    def module_scope(self):
        logging.info("called")
        yield
        logging.info("teardown")

    @pytest.fixture
    def module_test_to_fail(self):
        logging.info("called")
        raise AssertionError
        yield
        logging.info("teardonw")

    @pytest.mark.usefixtures("class_scope", "module_scope")
    def test_first(self):
        logging.info("[test_first]")
        time.sleep(5)

    @pytest.mark.usefixtures("class_scope", "module_scope")
    def test_second(self):
        logging.info("[test_second]")
        time.sleep(5)

    @pytest.mark.usefixtures("class_scope", "module_scope", "module_test_to_fail")
    def test_thrid(self):
        logging.info("[test_third]")
        time.sleep(5)

    @pytest.mark.usefixtures("class_scope", "module_scope")
    def test_fourth(self):
        logging.info("[test_fourth]")
        test_list = ["111"]
        time.sleep(5)
        assert len(test_list) == 0

    @pytest.mark.usefixtures("class_scope", "module_scope")
    @pytest.mark.parametrize(
        "test_input, expected",
        [
            ("correct@gmail.com", True),
            ("another.correct@custom.fr", True),
            ("and-another@custom.org", True),
            ("inavlid.com", False),
            ("veryb@d@.com", False),
            ("domain@too.long", False)
        ]
    )
    def test_is_valid_email_address(self, test_input, expected):
        logging.info(test_input)
        time.sleep(5)
