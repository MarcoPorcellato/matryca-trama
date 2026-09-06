"""Fail-closed provenance checks for unpublished Plumber source admission."""

from pathlib import Path
import unittest


REPOSITORY = Path(__file__).resolve().parents[2]
ADMISSION = REPOSITORY / "docs/contracts/PLUMBER_SOURCE_ADMISSION.md"


class PlumberSourceAdmissionTests(unittest.TestCase):
    def test_source_pin_is_static_only_and_release_blocked(self) -> None:
        self.assertTrue(ADMISSION.is_file(), f"missing source admission: {ADMISSION}")
        admission = " ".join(ADMISSION.read_text(encoding="utf-8").split())

        expected = (
            "2606c096e07555b977687299eae71842cb6f021a",
            "a24f949e994454b224fcb0d8e7c271ea5990ccf1",
            "405ec69582b3ca240d4747ef9c89b79e0073b545",
            "67ccefa91f8b4343c2d5821edae37c7c9aacd805",
            "62e1abb6c6177c3063e0dd87c43510190fd9d24a",
            "5ceacf991825334ddeb3d825e72acb5c48f3710c",
            "d0ec4bf4537a642803d42238bacf6b8e0252a61467578091d65586d46eb5cc3a",
            "192f7b6d4719ca5d319ffdeb4e749f4b9551eef1974fd43317c0ec9ee506492c",
            "fc163e8f695821e4a933f6d51dda1eaf29a12bc0d5ca4c3f9adce4e421e63750",
            "250438c57580c811c3e10b2a59089ffbb23ea2f1f66c4c53acc8ace0a9ee8569",
            "613f765376f2091b3dad2569ce19d9931f455b026f5ed495178526e87da1397a",
            "1a3befbaf9d5442dc186963a374628f758714141f807192d2eee0eed5c4f27dc",
            "9c8f0ac2584d89dda396b9830a91094b8d83dc57ae4f23036eec05e868375627",
        )
        for value in expected:
            with self.subTest(value=value):
                self.assertIn(value, admission)

        self.assertIn("static-only-unqualified", admission)
        self.assertIn("not a release artifact", admission)
        self.assertIn("must not create a runtime adapter", admission)
        self.assertIn("does not copy Plumber schema, TCK, profile, or LENS bytes", admission)
        self.assertIn("Parser, Logseq, filesystem, or DB dependency", admission)
        self.assertIn("PolyForm Noncommercial 1.0.0", admission)
        self.assertIn("lawyer-reviewed contributor agreement", admission)
        self.assertIn("source implementation evidence", admission)
        self.assertIn("test-only capability-policy evidence", admission)
        self.assertIn("does not establish a distributable consumer artifact", admission)


if __name__ == "__main__":
    unittest.main()
