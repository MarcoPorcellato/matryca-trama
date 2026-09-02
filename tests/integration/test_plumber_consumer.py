"""Consumer admission tests for public Plumber compatibility boundary."""

from pathlib import Path
import unittest

from trama_contracts import Outcome, Provenance, ReadRequest, ReadResult
from trama_plumber_bridge import accept_for_plumber


PLAN_PATH = Path("docs/superpowers/plans/2026-09-01-python-first-read-contract-implementation.md")
CONTRACT_ID = "trama.logseq.read/v1"
OPERATION = "graph.identify"
PRODUCER = "trama-logseq-og-adapter 1.0.0"
_DEFAULT_PROVENANCE = object()


class PlumberConsumerTests(unittest.TestCase):
    """Only complete, stable public envelopes may cross this boundary."""

    def success_result(self) -> ReadResult:
        request = ReadRequest(
            contract_id=CONTRACT_ID,
            accepted_contract_major=1,
            operation=OPERATION,
            request_id="r1",
            graph_selector="fixture:og-minimal",
        )
        return ReadResult.success(
            request=request,
            contract_version="1.0.0",
            graph_binding="fixture-digest:og-minimal",
            producer=PRODUCER,
            capabilities=(OPERATION,),
            payload={"operation": OPERATION},
            provenance=self.complete_provenance(),
        )

    def complete_provenance(
        self,
        *,
        source_mode: str = "og_markdown",
        authority: str = "logseq_og_markdown",
        source_reference: str = "fixture:og-minimal",
        evidence_digest: str = "a" * 64,
        producer: str = PRODUCER,
        exercised_capabilities: tuple[str, ...] = (OPERATION,),
    ) -> Provenance:
        return Provenance(
            source_mode=source_mode,  # type: ignore[arg-type]
            authority=authority,  # type: ignore[arg-type]
            source_reference=source_reference,
            evidence_digest=evidence_digest,
            producer=producer,
            exercised_capabilities=exercised_capabilities,
        )

    def direct_result(
        self,
        *,
        contract_id: object = CONTRACT_ID,
        contract_version: object = "1.0.0",
        operation: object = OPERATION,
        request_id: object = "r1",
        payload: object = None,
        outcome: object = Outcome.SUCCESS,
        graph_binding: object = "fixture-digest:og-minimal",
        producer: object = PRODUCER,
        capabilities: object = (OPERATION,),
        provenance: object = _DEFAULT_PROVENANCE,
    ) -> ReadResult:
        if payload is None:
            payload = {"operation": OPERATION}
        if provenance is _DEFAULT_PROVENANCE:
            provenance = self.complete_provenance()
        return ReadResult(
            contract_id=contract_id,  # type: ignore[arg-type]
            contract_version=contract_version,  # type: ignore[arg-type]
            operation=operation,  # type: ignore[arg-type]
            request_id=request_id,  # type: ignore[arg-type]
            payload=payload,  # type: ignore[arg-type]
            outcome=outcome,  # type: ignore[arg-type]
            graph_binding=graph_binding,  # type: ignore[arg-type]
            producer=producer,  # type: ignore[arg-type]
            capabilities=capabilities,  # type: ignore[arg-type]
            provenance=provenance,  # type: ignore[arg-type]
        )

    def test_accepts_success_og_envelope(self) -> None:
        payload = accept_for_plumber(self.success_result(), "1.7.1", "2.0.0")

        self.assertEqual(payload, {"operation": OPERATION})

    def test_rejects_non_success(self) -> None:
        request = ReadRequest(CONTRACT_ID, 1, OPERATION, "r1", "fixture:og-minimal")
        result = ReadResult.failure(
            Outcome.NOT_FOUND,
            request=request,
            contract_version="1.0.0",
            graph_binding="x",
            producer="p",
            capabilities=(OPERATION,),
            payload={},
        )

        with self.assertRaisesRegex(ValueError, "not_found"):
            accept_for_plumber(result, "1.8.0", "2.0.0")

    def test_rejects_non_og_authority(self) -> None:
        result = self.direct_result(
            provenance=self.complete_provenance(
                source_mode="db_native",
                authority="logseq_db_native",
            ),
        )

        with self.assertRaisesRegex(ValueError, "OG-native"):
            accept_for_plumber(result, "1.8.0", "2.0.0")

    def test_rejects_versions_outside_contract(self) -> None:
        for parser_version in ("1.7.0", "2.0.0", "garbage", "1.7"):
            with self.subTest(parser_version=parser_version):
                with self.assertRaisesRegex(ValueError, "incompatible"):
                    accept_for_plumber(self.success_result(), parser_version, "2.0.0")
        for plumber_version in ("1.9.9", "2.0.1", "garbage", "2"):
            with self.subTest(plumber_version=plumber_version):
                with self.assertRaisesRegex(ValueError, "incompatible"):
                    accept_for_plumber(self.success_result(), "1.8.0", plumber_version)

    def test_rejects_forged_direct_success_envelopes(self) -> None:
        cases: tuple[tuple[str, object], ...] = (
            ("wrong result type", object()),
            ("wrong outcome type", self.direct_result(outcome="success")),
            ("non-success outcome", self.direct_result(outcome=Outcome.NOT_FOUND)),
            ("wrong contract id", self.direct_result(contract_id="trama.logseq.read/v999")),
            ("wrong contract major", self.direct_result(contract_version="2.0.0")),
            ("unsupported operation", self.direct_result(operation="page.write", capabilities=("page.write",))),
            ("empty request id", self.direct_result(request_id="")),
            ("non-mapping payload", self.direct_result(payload=())),
            ("empty graph binding", self.direct_result(graph_binding="")),
            ("empty producer", self.direct_result(producer="")),
            ("empty capabilities", self.direct_result(capabilities=())),
            ("operation outside capabilities", self.direct_result(capabilities=("page.read",))),
            ("missing provenance", self.direct_result(provenance=None)),
            ("wrong provenance type", self.direct_result(provenance=object())),
            ("empty source reference", self.direct_result(provenance=self.complete_provenance(source_reference=""))),
            ("malformed evidence digest", self.direct_result(provenance=self.complete_provenance(evidence_digest="digest"))),
            ("provenance producer mismatch", self.direct_result(provenance=self.complete_provenance(producer="other"))),
            ("empty exercised capabilities", self.direct_result(provenance=self.complete_provenance(exercised_capabilities=()))),
            ("exercised capability outside envelope", self.direct_result(provenance=self.complete_provenance(exercised_capabilities=("page.read",)))),
            (
                "exercised capabilities exclude operation",
                self.direct_result(
                    capabilities=(OPERATION, "page.read"),
                    provenance=self.complete_provenance(
                        exercised_capabilities=("page.read",),
                    ),
                ),
            ),
        )

        for label, result in cases:
            with self.subTest(label=label):
                with self.assertRaises(ValueError):
                    accept_for_plumber(result, "1.8.0", "2.0.0")

    def test_rejects_prerelease_build_and_malformed_versions(self) -> None:
        for parser_version in (
            "1.7.1-alpha",
            "1.7.1+build.1",
            "01.7.1",
            "1.07.1",
            "1.7.01",
            "1.7.1.0",
        ):
            with self.subTest(parser_version=parser_version):
                with self.assertRaisesRegex(ValueError, "incompatible parser version"):
                    accept_for_plumber(self.success_result(), parser_version, "2.0.0")
        for plumber_version in (
            "2.0.0-rc.1",
            "2.0.0+build.1",
            "02.0.0",
            "2.00.0",
            "2.0.00",
        ):
            with self.subTest(plumber_version=plumber_version):
                with self.assertRaisesRegex(ValueError, "incompatible plumber version"):
                    accept_for_plumber(self.success_result(), "1.8.0", plumber_version)
        for contract_version in (
            "1.0.0-alpha",
            "1.0.0+build.1",
            "01.0.0",
            "1.00.0",
            "1.0.00",
            "malformed",
        ):
            with self.subTest(contract_version=contract_version):
                with self.assertRaisesRegex(ValueError, "incompatible contract version"):
                    accept_for_plumber(
                        self.direct_result(contract_version=contract_version),
                        "1.8.0",
                        "2.0.0",
                    )

    def test_plan_requires_explicit_complete_suite_coverage(self) -> None:
        plan = PLAN_PATH.read_text(encoding="utf-8")
        _, task_six_and_after = plan.split("## Task 6:", maxsplit=1)
        task_six, task_seven = task_six_and_after.split("## Task 7:", maxsplit=1)
        expected_commands = (
            "python -m unittest discover -s tests/contracts -v",
            "python -m unittest discover -s tests/containment -v",
            "python -m unittest tests.integration.test_plumber_consumer -v",
            "python -m unittest tests.test_foundation_validator -v",
        )

        for command in expected_commands:
            with self.subTest(task="six", command=command):
                self.assertIn(command, task_six)
            with self.subTest(task="seven", command=command):
                self.assertIn(command, task_seven)
        standalone_command = (
            "uv run --all-packages python -m unittest discover -s tests -v"
        )
        self.assertNotIn(f"Run: `{standalone_command}`", task_six)
        self.assertNotIn(f"Run: `{standalone_command}`", task_seven)
        self.assertNotIn(f"- run: {standalone_command}", task_seven)


if __name__ == "__main__":
    unittest.main()
