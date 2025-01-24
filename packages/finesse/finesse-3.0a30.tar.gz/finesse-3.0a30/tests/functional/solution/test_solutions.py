import finesse


def test_selection():
    model = finesse.script.parse(
        """
        l l1
        pd P l1.p1.o
        pd A l1.p1.o
        """
    )

    sol = model.run('noxaxis(name="A")')
    assert isinstance(sol["A"], float), "Didn't return pd A result"

    model = finesse.script.parse(
        """
        l l1
        pd P l1.p1.o
        """
    )

    sol = model.run('noxaxis(name="A")')
    assert isinstance(
        sol["A"], finesse.solutions.ArraySolution
    ), "Didn't return A solution"
    assert isinstance(
        sol[["A"]], finesse.solutions.ArraySolution
    ), "Didn't return A solution using a list of names"

    model = finesse.script.parse(
        """
        l l1
        pd P l1.p1.o
        pd A l1.p1.o
        """
    )

    sol = model.run('series(noxaxis(name="A"), noxaxis(name="B"))')
    assert isinstance(
        sol["A"], finesse.solutions.ArraySolution
    ), "Didn't return A solution"
