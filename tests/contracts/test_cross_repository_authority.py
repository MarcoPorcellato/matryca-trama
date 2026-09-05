"""Policy tests for the published Trama-to-Plumber architecture boundary."""

from pathlib import Path
import unittest


REPOSITORY = Path(__file__).resolve().parents[2]
DELIVERY_PROGRAM = REPOSITORY / "docs/specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md"
ARCHITECTURE = REPOSITORY / "docs/ARCHITECTURE.md"
ROADMAP = REPOSITORY / "docs/ROADMAP.md"
README = REPOSITORY / "README.md"
DECISION_INDEX = REPOSITORY / "docs/decisions/README.md"
ADOPTION_ADR = REPOSITORY / "docs/decisions/ADR-0006-PLUMBER-GATEWAY-ADOPTION.md"
PRODUCT_BOUNDARY_ADR = REPOSITORY / "docs/decisions/ADR-0002-TRAMA_BRAIN_PRODUCT_BOUNDARY.md"
ARCHITECTURE_STANDARD = REPOSITORY / "docs/standards/CLEAN_ARCHITECTURE.md"
ENFORCEMENT_SPEC = (
    REPOSITORY / "docs/superpowers/specs/2026-09-05-clean-code-clean-architecture.md"
)
DEVELOPMENT_SKILL = REPOSITORY / ".agents/skills/trama-development/SKILL.md"
ECOSYSTEM_HISTORY = (
    REPOSITORY / "docs/contracts/ECOSYSTEM_RESPONSIBILITY_AND_CHANGE_CONTRACT.md"
)
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

    def test_accepted_adoption_pins_plumber_authority_without_runtime_claim(self) -> None:
        adoption = self.read(ADOPTION_ADR)
        index = self.read(DECISION_INDEX)

        self.assertIn("Status: Accepted", adoption)
        self.assertIn("0646f349572d9a5dfaf37e936f5162b6212dc194", adoption)
        self.assertIn("Matryca Plumber is the sole Logseq gateway", adoption)
        self.assertIn("OG Markdown -> Parser -> Plumber -> Trama / Brain", adoption)
        self.assertIn("Logseq DB official host -> Plumber -> Trama / Brain", adoption)
        self.assertIn("`og_markdown`", adoption)
        self.assertIn("D1 outcome `supported`", adoption)
        self.assertIn("no runtime feature", adoption)
        self.assertIn("ADR-0006: Plumber gateway adoption", index)

    def test_accepted_policy_redirects_old_trama_gateway_authority(self) -> None:
        ecosystem = self.read(ECOSYSTEM_HISTORY)
        product_boundary = self.read(PRODUCT_BOUNDARY_ADR)
        standard = self.read(ARCHITECTURE_STANDARD)
        enforcement = self.read(ENFORCEMENT_SPEC)

        self.assertIn("Historical authority redirect", ecosystem)
        self.assertIn("ADR-0006", ecosystem)
        self.assertIn("Superseded in part by: ADR-0006", product_boundary)
        self.assertIn("Plumber owns the future `plumber.*`", standard)
        self.assertIn("Plumber owns the future `plumber.*`", enforcement)
        self.assertNotIn("Trama owns the `trama.logseq.read/v1` envelope", standard)
        self.assertNotIn("Trama owns the `trama.logseq.read/v1` envelope", enforcement)

    def test_development_skill_routes_to_accepted_owner_without_runtime_claim(self) -> None:
        skill = self.read(DEVELOPMENT_SKILL)

        self.assertIn("accepted [Plumber gateway adoption]", skill)
        self.assertIn("not a runtime, package, canonical contract artifact, or consumer-profile claim", skill)
        self.assertNotIn("current [Plumber gateway proposal]", skill)

    def test_public_entrypoint_marks_historical_trama_contract_non_authoritative(self) -> None:
        readme = self.read(README)

        self.assertIn("Plumber authority decision", readme)
        self.assertIn("`trama.logseq.read/v1`", readme)
        self.assertIn("historical experimental", readme)


if __name__ == "__main__":
    unittest.main()
