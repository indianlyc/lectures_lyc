from unittest import TestCase, main
from ..tools import (
    search_duplicates,
    filter,
    get_ext,
    get_list_names,
    FakeFileSystem,
)

class TestSearchDuplicates(TestCase):
    def test_search_duplicates(self):
        list1 = [("/p1/f1.mov", "a"), ("/p1/f2.jpg", "a"), ("/p1/f3.jpg", "b")]
        res = search_duplicates((list1))
        self.assertEquals(res, {"a": ["/p1/f1.mov", "/p1/f2.jpg"], "b": ["/p1/f3.jpg"]})


class TestFilter(TestCase):
    def test_filter(self):
        list1 = [("/p1/f1.mov", "a"), ("/p1/f2.jpg", "a"), ("/p1/f3.jpg", "b")]
        res = filter(list1, ["jpg", "png"])
        self.assertEquals(res, [("/p1/f2.jpg", "a"), ("/p1/f3.jpg", "b")])


class TestGetExt(TestCase):
    def test_get_ext(self):
        s = "/p1/f1.mov"
        res = get_ext(s)
        self.assertEquals(res, "mov")

class TestGetListNames(TestCase):
    def test_get_list_names(self):
        s = [{"b": [{"a.jpg": "a"}, {"b.jpg":"b"}, {"c": [{"d.mov":"d"}, {"e": [{"f.pdf": "f"}]}]}]}]
        res = get_list_names(FakeFileSystem(s))
        self.assertEquals(res, [
                                ("b/a.jpg", "a"),
                                ("b/b.jpg", "b"),
                                ("b/c/d.mov", "d"),
                                ("b/c/e/f.pdf", "f"),
                                ])

if __name__ == "__main__":
    main()