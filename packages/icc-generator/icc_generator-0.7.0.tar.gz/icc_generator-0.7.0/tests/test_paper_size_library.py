# -*- coding: utf-8 -*-
"""Tests for the PaperSizeLibrary class."""

import pytest

from icc_generator.api import PaperSizeLibrary, PaperSize


def test_paper_size_library_meant_to_be_used_as_a_storage():
    """Instantiating PaperSizeLibrary raise RuntimeError."""
    with pytest.raises(RuntimeError) as cm:
        PaperSizeLibrary()

    assert str(cm.value) == (
        "PaperSizeLibrary is meant to be used as a storage class. "
        "Do not instantiate it."
    )


@pytest.mark.parametrize(
    "paper_name,paper_size",
    [
        ["4x6", PaperSize(name="4x6", width=101.6, height=152.4)],
        ["11x17", PaperSize(name="11x17", width=279.4, height=431.8)],
        ["A2", PaperSize(name="A2", width=420.0, height=594.0)],
        ["A2R", PaperSize(name="A2R", width=594.0, height=420.0)],
        ["A3", PaperSize(name="A3", width=297.0, height=420.0)],
        ["A3R", PaperSize(name="A3R", width=420.0, height=297.0)],
        ["A3P", PaperSize(name="A3_Plus", width=329.0, height=483.0)],
        ["A3PR", PaperSize(name="A3_Plus_Landscape", width=483.0, height=329.0)],
        ["A4", PaperSize(name="A4", width=210.0, height=297.0)],
        ["A4R", PaperSize(name="A4R", width=297.0, height=210.0)],
        ["Legal", PaperSize(name="Legal", width=215.9, height=355.6)],
        ["LegalR", PaperSize(name="Legal", width=355.6, height=215.9)],
        ["Letter", PaperSize(name="Letter", width=215.9, height=279.4)],
        ["LetterR", PaperSize(name="LetterR", width=279.4, height=215.9)],
    ],
)
def test_paper_size_library_data(paper_name, paper_size):
    """PaperSizeLibrary contains predefined PaperSizes."""
    assert paper_name in PaperSizeLibrary.paper_sizes
    assert paper_size == PaperSizeLibrary.paper_sizes[paper_name]


@pytest.mark.parametrize(
    "paper_name, key_name",
    [
        ["p4x6", "4x6"],
        ["p11x17", "11x17"],
        ["A2", "A2"],
        ["A2R", "A2R"],
        ["A3", "A3"],
        ["A3R", "A3R"],
        ["A3P", "A3P"],
        ["A3PR", "A3PR"],
        ["A4", "A4"],
        ["A4R", "A4R"],
        ["Legal", "Legal"],
        ["LegalR", "LegalR"],
        ["Letter", "Letter"],
        ["LetterR", "LetterR"],
    ],
)
def test_paper_size_library_paper_names(paper_name, key_name):
    """PaperSizeLibrary contains predefined PaperSize names."""
    assert (
        getattr(PaperSizeLibrary, paper_name) == PaperSizeLibrary.paper_sizes[key_name]
    )


@pytest.mark.parametrize(
    "paper_size_name",
    [
        "4x6",
        "11x17",
        "A2",
        "A2R",
        "A3",
        "A3R",
        "A4",
        "A4R",
        "Legal",
        "LegalR",
        "Letter",
        "LetterR",
    ],
)
def test_get_paper_size_is_working_okay(paper_size_name):
    """get_paper_size() returns PaperSize with name."""
    expected_value = PaperSizeLibrary.paper_sizes[paper_size_name]
    assert expected_value == PaperSizeLibrary.get_paper_size(paper_size_name)


def test_get_paper_size_paper_size_name_is_not_a_str():
    """get_paper_size() raises a TypeError if the given paper_size_name is not a str."""
    with pytest.raises(TypeError) as cm:
        _ = PaperSizeLibrary.get_paper_size(2314)

    assert str(cm.value) == "paper_size_name should be a str, not int"


def test_get_paper_size_paper_size_name_does_not_exist_in_the_library():
    """get_paper_size() paper_size_name doesn't exist in the library returns None."""
    assert PaperSizeLibrary.get_paper_size("my special paper name") is None
