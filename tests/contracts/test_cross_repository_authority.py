"""Policy tests for the published Trama-to-Plumber architecture boundary."""

from pathlib import Path
import unittest


REPOSITORY = Path(__file__).resolve().parents[2]
DELIVERY_PROGRAM = REPOSITORY / "docs/specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md"
ARCHITECTURE = REPOSITORY / "docs/ARCHITECTURE.md"
ROADMAP = REPOSITORY / "docs/ROADMAP.md"
SUPERSEDED_PLAN = (
    REPOSITORY / "docs/superpowers/plans/2026-09-01-logseq-read-contract-and-adapter.md"
)


class CrossRepositoryAuthorityTests(unittest.TestCase):
    def read(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing canonical surface: {path}")
        return " ".join(path.read_text(encoding="utf-8").split())

    def test_canonical_delivery_program_assigns_future_gateway_to_plumber(self) -> None:
        delivery = self.read(DELIVERY_PROGRAM)

        self.assertIn(
            "Matryca Plumber is the sole future Logseq gateway and canonical public-contract owner.",
            delivery,
        )
        self.assertIn(
            "Trama is a future Plumber consumer; it does not own future source adapters or Logseq wire contracts.",
            delivery,
        )
        self.assertIn("Historical experimental Trama adapters remain evidence only", delivery)
        self.assertNotIn("Trama owns host acquisition and provenance", delivery)
        self.assertNotIn("Plumber as consumer of validated public Trama envelopes", delivery)

    def test_architecture_maps_only_plumber_between_sources_and_products(self) -> None:
        architecture = self.read(ARCHITECTURE)

        self.assertIn("OG Markdown -> Parser -> Plumber -> Trama / Brain", architecture)
        self.assertIn("Logseq DB official host -> Plumber -> Trama / Brain", architecture)
        self.assertIn("historical experimental implementation", architecture)

    def test_roadmap_does_not_couple_og_consumer_to_db_decision(self) -> None:
        roadmap = self.read(ROADMAP)

        self.assertIn(
            "A qualified `og_markdown` Plumber profile may support the Trama consumer independently of D1.",
            roadmap,
        )
        self.assertIn(
            "A `db_native` consumer profile requires D1 outcome `supported`.",
            roadmap,
        )
        self.assertNotIn(
            "After Plumber publishes the contract and D1 has a supported outcome",
            roadmap,
        )

    def test_reversed_adapter_plan_is_explicitly_nonoperative_history(self) -> None:
        plan = self.read(SUPERSEDED_PLAN)

        self.assertIn("Status: Superseded / Historical / Non-operative.", plan)
        self.assertIn("not executable authority", plan)


if __name__ == "__main__":
    unittest.main()
