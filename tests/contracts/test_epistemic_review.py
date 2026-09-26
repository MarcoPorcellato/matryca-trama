"""Contract tests for private experimental epistemic-review vocabulary."""

import ast
import dataclasses
import hashlib
import inspect
from pathlib import Path
from typing import Literal, get_type_hints
import unittest

import trama_contracts
import trama_contracts._epistemic_review as epistemic_review
from trama_contracts._epistemic_review import (
    Finding,
    FindingKind,
    ReviewDecision,
    ReviewOutcome,
    ReviewProposal,
    ReviewReceipt,
    ReviewScope,
    decide,
)


class EpistemicReviewTests(unittest.TestCase):
    prohibited_api_terms = (
        "apply",
        "write",
        "save",
        "persist",
        "graph_mutation",
        "truth",
        "verified_truth",
        "editor_document_json",
        "file_path",
        "database_handle",
        "network_endpoint",
    )

    def setUp(self) -> None:
        self.scope = ReviewScope(
            ("requirement-1", "context-1", "selected-only"),
            True,
            ("requirement-1",),
            ("context-1",),
        )
        self.claim = Finding(
            FindingKind.SOURCE_CLAIM,
            ("evidence-1",),
            ("requirement-1",),
            "Source says this.",
            "source_attribution_only",
        )
        self.gap = Finding(
            FindingKind.VERIFICATION_GAP,
            ("evidence-2",),
            ("requirement-1",),
            "Evidence remains missing.",
            "not_established_in_selected_scope",
        )

    def _assert_required_ids_rejected(self, constructor: object) -> None:
        for value in ([], {"id"}, "id", (), ("",), ("   ",), ("id", 1)):
            with self.subTest(value=value):
                with self.assertRaises((TypeError, ValueError)):
                    constructor(value)  # type: ignore[operator]

    def _assert_optional_ids_contract(self, constructor: object) -> None:
        constructor(())  # type: ignore[operator]
        for value in ([], {"id"}, "id", ("",), ("   ",), ("id", 1)):
            with self.subTest(value=value):
                with self.assertRaises((TypeError, ValueError)):
                    constructor(value)  # type: ignore[operator]

    def _assert_no_prohibited_terms(self, *surfaces: object) -> None:
        for surface in surfaces:
            text = str(surface).lower()
            for term in self.prohibited_api_terms:
                self.assertNotIn(term, text)

    def _assert_callable_surface_is_private(self, callable_value: object) -> None:
        signature = inspect.signature(callable_value)  # type: ignore[arg-type]
        self._assert_no_prohibited_terms(
            getattr(callable_value, "__name__", ""),
            *(parameter.name for parameter in signature.parameters.values()),
            *(parameter.annotation for parameter in signature.parameters.values() if parameter.annotation is not inspect.Signature.empty),
            signature.return_annotation if signature.return_annotation is not inspect.Signature.empty else "",
        )

    def _is_self_attribute_chain(self, node: ast.AST) -> bool:
        while isinstance(node, ast.Attribute):
            node = node.value
        return isinstance(node, ast.Name) and node.id == "self"

    def _module_scope_nodes(self, node: ast.AST):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            return
        yield node
        for child in ast.iter_child_nodes(node):
            yield from self._module_scope_nodes(child)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        source_path = Path(epistemic_review.__file__)
        source_bytes = source_path.read_bytes()
        cls.canonical_source = source_bytes.decode("utf-8")
        if hashlib.sha256(source_bytes).hexdigest() != (
            "0bfbe20e7eeb318d4da847e51584cce3e80967f09061653ee08bf0cad91f1d41"
        ):
            raise AssertionError("canonical source SHA-256 mismatch")
        cls.canonical_tree = ast.parse(cls.canonical_source, feature_version=(3, 12))
        cls.canonical_dump = ast.dump(cls.canonical_tree, include_attributes=False)
        cls.direct_root_names = (
            ("Expr", None), ("ImportFrom", "dataclasses.dataclass"),
            ("ImportFrom", "enum.StrEnum"), ("ImportFrom", "typing.Literal"),
            ("FunctionDef", "_require_text"), ("FunctionDef", "_require_ids"),
            ("FunctionDef", "_is_subset"), ("FunctionDef", "_require_findings"),
            ("ClassDef", "FindingKind"), ("ClassDef", "ReviewOutcome"),
            ("ClassDef", "ReviewScope"), ("ClassDef", "Finding"),
            ("ClassDef", "ReviewProposal"), ("ClassDef", "ReviewDecision"),
            ("FunctionDef", "decide"), ("ClassDef", "ReviewReceipt"),
        )
        cls.canonical_exceptions = {}
        for node in cls.canonical_tree.body:
            if isinstance(node, ast.ImportFrom):
                alias = node.names[0]
                cls.canonical_exceptions[f"import:{node.module}.{alias.name}"] = ast.dump(
                    node, include_attributes=False
                )
            elif isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in {
                "_require_text", "_require_ids", "_is_subset", "_require_findings", "ReviewDecision"
            }:
                cls.canonical_exceptions[node.name] = ast.dump(node, include_attributes=False)
        cls.protected_names = {
            node.func.id
            for node in ast.walk(cls.canonical_tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        cls.call_shapes = set()
        for node in ast.walk(cls.canonical_tree):
            if isinstance(node, ast.Call):
                shape = cls._call_shape(node)
                if shape is not None:
                    cls.call_shapes.add(shape)

    @staticmethod
    def _call_shape(node: ast.Call):
        func = node.func
        if isinstance(func, ast.Name):
            callee = ("name", func.id)
            receiver = None
        elif isinstance(func, ast.Attribute):
            callee = ("attribute", func.attr)
            receiver_node = func.value
            if isinstance(receiver_node, ast.Name):
                receiver = "name"
            elif (
                isinstance(receiver_node, ast.Attribute)
                and isinstance(receiver_node.value, ast.Name)
                and receiver_node.value.id == "self"
            ):
                receiver = f"self.{receiver_node.attr}"
            else:
                return None
        else:
            return None
        return (
            callee, receiver, len(node.args),
            tuple(keyword.arg for keyword in node.keywords),
        )

    @classmethod
    def _root_name(cls, node: ast.AST):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            return ("Expr", None)
        if isinstance(node, ast.ImportFrom):
            alias = node.names[0] if len(node.names) == 1 else None
            name = f"{node.module}.{alias.name}" if alias is not None else None
            return ("ImportFrom", name)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            return (type(node).__name__, node.name)
        return (type(node).__name__, None)

    @classmethod
    def _direct_root_exception_counts(cls, tree: ast.Module):
        counts = {name: 0 for name in cls.canonical_exceptions}
        for node in tree.body:
            dump = ast.dump(node, include_attributes=False)
            for name, canonical_dump in cls.canonical_exceptions.items():
                if dump == canonical_dump:
                    counts[name] += 1
        return counts

    @classmethod
    def _binding_events(cls, tree: ast.Module):
        parents = {
            child: parent
            for parent in ast.walk(tree)
            for child in ast.iter_child_nodes(parent)
        }

        def owner(node):
            current = node
            while current in parents and parents[current] is not tree:
                current = parents[current]
            return current if parents.get(current) is tree else None

        events = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                events.append((node.name, node, owner(node)))
            elif isinstance(node, ast.arg):
                events.append((node.arg, node, owner(node)))
            elif isinstance(node, ast.alias):
                bound = node.asname or node.name.split(".")[0]
                events.append((bound, node, owner(node)))
            elif isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
                events.append((node.id, node, owner(node)))
            elif isinstance(node, (ast.Global, ast.Nonlocal)):
                events.extend((name, node, owner(node)) for name in node.names)
            elif isinstance(node, ast.ExceptHandler) and node.name:
                events.append((node.name, node, owner(node)))
            elif isinstance(node, (ast.MatchAs, ast.MatchStar)) and node.name:
                events.append((node.name, node, owner(node)))
            elif isinstance(node, ast.MatchMapping) and node.rest:
                events.append((node.rest, node, owner(node)))
            elif type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}:
                bound = getattr(node, "name", None)
                if isinstance(bound, str):
                    events.append((bound, node, owner(node)))
        return events

    @classmethod
    def _policy_error(cls, source: str, require_canonical_exceptions: bool = False):
        try:
            tree = ast.parse(source, feature_version=(3, 12))
        except SyntaxError as error:
            return ("syntax", str(error))

        allowed_imports = {
            ("dataclasses", "dataclass"),
            ("enum", "StrEnum"),
            ("typing", "Literal"),
        }
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                return ("import", "direct imports are forbidden")
            if isinstance(node, ast.ImportFrom):
                if (
                    node not in tree.body
                    or node.level != 0
                    or len(node.names) != 1
                    or node.names[0].asname is not None
                    or (node.module, node.names[0].name) not in allowed_imports
                ):
                    return ("import", "import is outside finite direct-root allowlist")
            if getattr(node, "type_params", ()):
                return ("type-parameter", "generic type parameters are outside finite grammar")
            if type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}:
                bound = getattr(node, "name", None)
                if bound in cls.protected_names:
                    return ("protected-binding", f"protected name {bound!r} is a type-parameter binding")
                return ("type-parameter", "generic type parameters are outside finite grammar")

        for node in ast.walk(tree):
            if isinstance(node, ast.NamedExpr):
                return ("binding", "named-expression binding is forbidden")

        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id in {"globals", "locals", "vars"}:
                return ("namespace", f"namespace name {node.id!r} is forbidden")
            if isinstance(node, ast.Attribute) and node.attr == "__globals__":
                return ("namespace", "function namespace access is forbidden")

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                return ("import", "direct imports are forbidden")
            if isinstance(node, ast.ImportFrom):
                if (
                    node not in tree.body
                    or node.level != 0
                    or len(node.names) != 1
                    or node.names[0].asname is not None
                    or (node.module, node.names[0].name) not in allowed_imports
                ):
                    return ("import", "import is outside finite direct-root allowlist")
            if isinstance(node, ast.NamedExpr):
                return ("binding", "named-expression binding is forbidden")
            if getattr(node, "type_params", ()):
                return ("type-parameter", "generic type parameters are outside finite grammar")
            if type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}:
                bound = getattr(node, "name", None)
                if bound in cls.protected_names:
                    return ("protected-binding", f"protected name {bound!r} is a type-parameter binding")
                return ("type-parameter", "generic type parameters are outside finite grammar")
            if isinstance(node, ast.Name) and node.id in {"globals", "locals", "vars"}:
                return ("namespace", f"namespace name {node.id!r} is forbidden")
            if isinstance(node, ast.Attribute) and node.attr == "__globals__":
                return ("namespace", "function namespace access is forbidden")
            if isinstance(node, (ast.Attribute, ast.Subscript)) and isinstance(node.ctx, (ast.Store, ast.Del)):
                return ("store-target", "attribute and subscript stores/deletes are forbidden")
            if isinstance(node, ast.Call):
                shape = cls._call_shape(node)
                if shape is None or shape not in cls.call_shapes:
                    callee = node.func.id if isinstance(node.func, ast.Name) else getattr(node.func, "attr", "dynamic")
                    category = "side-effect" if callee in {
                        "exec", "eval", "__import__", "import_module", "open", "print",
                        "setattr", "delattr", "getattr",
                    } else "call"
                    return (category, f"call form {callee!r} is outside canonical call inventory")

        if require_canonical_exceptions:
            counts = cls._direct_root_exception_counts(tree)
            if any(count != 1 for count in counts.values()):
                return ("canonical-exception", f"expected one direct-root copy of each exception, got {counts}")

        parents = {
            child: parent
            for parent in ast.walk(tree)
            for child in ast.iter_child_nodes(parent)
        }

        def direct_root_owner(node):
            current = node
            while current in parents and parents[current] is not tree:
                current = parents[current]
            return current if parents.get(current) is tree else None

        root_dumps = {
            name: dump for name, dump in cls.canonical_exceptions.items()
        }
        for name, binding_node, root in cls._binding_events(tree):
            if name not in cls.protected_names:
                continue
            permitted = False
            if isinstance(binding_node, ast.alias) and isinstance(root, ast.ImportFrom):
                permitted = ast.dump(root, include_attributes=False) in root_dumps.values()
            elif isinstance(root, (ast.FunctionDef, ast.ClassDef)):
                key = root.name
                permitted = (
                    root in tree.body
                    and key in root_dumps
                    and ast.dump(root, include_attributes=False) == root_dumps[key]
                )
            if not permitted:
                return ("protected-binding", f"protected name {name!r} is rebound")

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = node.func.id if isinstance(node.func, ast.Name) else None
                if name in {"exec", "eval", "__import__", "import_module", "open", "print", "setattr", "delattr", "getattr"}:
                    return ("side-effect", f"side-effect primitive {name!r} is forbidden")
        return None

    @classmethod
    def _assert_policy_allows(cls, source: str) -> None:
        error = cls._policy_error(source)
        if error is not None:
            raise AssertionError(f"{error[0]}: {error[1]}")

    @classmethod
    def _assert_policy_rejects(
        cls,
        source: str,
        expected_category: str,
        *,
        require_canonical_exceptions: bool = False,
    ) -> None:
        error = cls._policy_error(
            source, require_canonical_exceptions=require_canonical_exceptions
        )
        if error is None:
            raise AssertionError(f"candidate unexpectedly passed policy; expected {expected_category}")
        if error[0] != expected_category:
            raise AssertionError(f"expected {expected_category}, got {error[0]}: {error[1]}")

    @classmethod
    def _assert_ast_is_inert(cls, source: str) -> None:
        error = cls._policy_error(source, require_canonical_exceptions=True)
        if error is not None:
            raise AssertionError(f"{error[0]}: {error[1]}")
        tree = ast.parse(source, feature_version=(3, 12))
        if tuple(cls._root_name(node) for node in tree.body) != cls.direct_root_names:
            raise AssertionError("direct-root-sequence: candidate root sequence differs from canonical sequence")
        if ast.dump(tree, include_attributes=False) != cls.canonical_dump:
            raise AssertionError("canonical-mismatch: candidate AST differs from trusted canonical AST")
    def test_all_experimental_symbols_remain_private_at_package_root(self) -> None:
        symbols = (
            "FindingKind", "ReviewOutcome", "ReviewScope", "Finding", "ReviewProposal",
            "ReviewDecision", "ReviewReceipt", "decide",
        )
        for symbol in symbols:
            with self.subTest(symbol=symbol):
                self.assertNotIn(symbol, trama_contracts.__all__)
                self.assertNotIn(symbol, vars(trama_contracts))
                self.assertFalse(hasattr(trama_contracts, symbol))
        self.assertIs(epistemic_review.ReviewScope, ReviewScope)

    def test_private_enums_have_exact_closed_values(self) -> None:
        self.assertEqual(
            tuple(member.value for member in FindingKind),
            ("source_claim", "hypothesis", "possible_contradiction", "verification_gap"),
        )
        self.assertEqual(
            tuple(member.value for member in ReviewOutcome),
            ("complete_for_selected_scope", "incomplete", "unknown"),
        )

    def test_every_identifier_collection_has_full_type_and_blank_matrix(self) -> None:
        self._assert_required_ids_rejected(lambda value: ReviewScope(value, True))
        self._assert_optional_ids_contract(
            lambda value: ReviewScope(("requirement-1", "context-1"), True, value, ("context-1",))
        )
        self._assert_optional_ids_contract(
            lambda value: ReviewScope(("requirement-1", "context-1"), True, ("requirement-1",), value)
        )
        self._assert_required_ids_rejected(
            lambda value: Finding(FindingKind.SOURCE_CLAIM, value, ("requirement-1",), "Rationale.", "source_attribution_only")
        )
        self._assert_required_ids_rejected(
            lambda value: Finding(FindingKind.SOURCE_CLAIM, ("evidence-1",), value, "Rationale.", "source_attribution_only")
        )
        self._assert_required_ids_rejected(
            lambda value: ReviewReceipt("fixture-digest", value, "engine-1", "proposal-digest", ReviewOutcome.UNKNOWN)
        )

    def test_scope_exact_bool_optional_empty_and_subset_contract(self) -> None:
        self.assertEqual(self.scope.requirement_ids, ("requirement-1",))
        self.assertEqual(self.scope.context_ids, ("context-1",))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            self.scope.scope_complete = False  # type: ignore[misc]
        for invalid_complete in (1, 0, "true", None):
            with self.subTest(invalid_complete=invalid_complete):
                with self.assertRaises(TypeError):
                    ReviewScope(("requirement-1",), invalid_complete)
        with self.assertRaises(ValueError):
            ReviewScope(("requirement-1",), True, ("foreign",), ())
        with self.assertRaises(ValueError):
            ReviewScope(("context-1",), True, (), ("foreign",))

    def test_finding_requires_exact_label_and_immutable_typed_values(self) -> None:
        self.assertEqual(
            tuple(field.name for field in dataclasses.fields(Finding)),
            ("kind", "evidence_ids", "selected_scope_ids", "rationale", "confidence_label"),
        )
        labels = (
            (FindingKind.SOURCE_CLAIM, "source_attribution_only"),
            (FindingKind.HYPOTHESIS, "unverified_hypothesis"),
            (FindingKind.POSSIBLE_CONTRADICTION, "comparison_rule_match"),
            (FindingKind.VERIFICATION_GAP, "not_established_in_selected_scope"),
        )
        for kind, label in labels:
            with self.subTest(kind=kind):
                finding = Finding(kind, ("evidence-1",), ("requirement-1",), "Rationale.", label)
                self.assertEqual(finding.confidence_label, label)
                with self.assertRaises(dataclasses.FrozenInstanceError):
                    finding.rationale = "Changed."  # type: ignore[misc]
                with self.assertRaises(ValueError):
                    Finding(kind, ("evidence-1",), ("requirement-1",), "Rationale.", "wrong")

    def test_valid_complete_and_incomplete_gap_proposals_construct(self) -> None:
        complete = ReviewProposal(
            self.scope, ReviewOutcome.COMPLETE_FOR_SELECTED_SCOPE, (self.claim,), "",
            "fixture-revision-1", "raw-digest-1", "canonical-digest-1",
        )
        incomplete = ReviewProposal(
            self.scope, ReviewOutcome.INCOMPLETE, (self.gap,), "",
            "fixture-revision-2", "raw-digest-2", "canonical-digest-2",
        )
        self.assertEqual(complete.findings, (self.claim,))
        self.assertEqual(incomplete.findings, (self.gap,))

    def test_proposal_rejects_foreign_subset_mixed_gap_and_independent_invalid_cases(self) -> None:
        foreign_claim = Finding(
            FindingKind.SOURCE_CLAIM, ("evidence-3",), ("foreign",), "Outside selected scope.", "source_attribution_only"
        )
        mixed_gap = Finding(
            FindingKind.VERIFICATION_GAP, ("evidence-4",), ("requirement-1", "selected-only"),
            "Partly undeclared gap.", "not_established_in_selected_scope",
        )
        incomplete_scope = ReviewScope(("requirement-1",), False, ("requirement-1",), ())
        cases = (
            (self.scope, ReviewOutcome.INCOMPLETE, ("not-a-finding",), "reason", "rev-1", "raw-1", "canonical-1", TypeError),
            (self.scope, ReviewOutcome.INCOMPLETE, [], "reason", "rev-1", "raw-1", "canonical-1", TypeError),
            (self.scope, ReviewOutcome.INCOMPLETE, (foreign_claim,), "reason", "rev-1", "raw-1", "canonical-1", ValueError),
            (self.scope, ReviewOutcome.INCOMPLETE, (mixed_gap,), "reason", "rev-1", "raw-1", "canonical-1", ValueError),
            (incomplete_scope, ReviewOutcome.COMPLETE_FOR_SELECTED_SCOPE, (self.claim,), "", "rev-1", "raw-1", "canonical-1", ValueError),
            (self.scope, ReviewOutcome.COMPLETE_FOR_SELECTED_SCOPE, (self.gap,), "", "rev-1", "raw-1", "canonical-1", ValueError),
            (self.scope, ReviewOutcome.COMPLETE_FOR_SELECTED_SCOPE, (), "", "rev-1", "raw-1", "canonical-1", ValueError),
            (self.scope, ReviewOutcome.INCOMPLETE, (), "", "rev-1", "raw-1", "canonical-1", ValueError),
            (self.scope, ReviewOutcome.UNKNOWN, (), "", "rev-1", "raw-1", "canonical-1", ValueError),
            (self.scope, ReviewOutcome.INCOMPLETE, (self.claim,), "reason", "same", "same", "canonical-1", ValueError),
            (self.scope, ReviewOutcome.INCOMPLETE, (self.claim,), "reason", "same", "raw-1", "same", ValueError),
            (self.scope, ReviewOutcome.INCOMPLETE, (self.claim,), "reason", "rev-1", "same", "same", ValueError),
        )
        for scope, outcome, findings, reason, revision, raw, canonical, error in cases:
            with self.subTest(scope=scope, outcome=outcome, findings=findings):
                with self.assertRaises(error):
                    ReviewProposal(scope, outcome, findings, reason, revision, raw, canonical)

    def test_decide_has_exact_signature_literal_and_runtime_dispositions(self) -> None:
        signature = inspect.signature(decide)
        self.assertEqual(tuple(signature.parameters), ("proposal_digest", "disposition", "session_token"))
        self.assertEqual(signature.parameters["proposal_digest"].annotation, str)
        self.assertEqual(signature.parameters["disposition"].annotation, Literal["acknowledge", "reject", "defer"])
        self.assertEqual(signature.parameters["session_token"].annotation, str)
        self.assertIs(signature.return_annotation, ReviewDecision)
        hints = get_type_hints(decide)
        self.assertEqual(hints, {
            "proposal_digest": str,
            "disposition": Literal["acknowledge", "reject", "defer"],
            "session_token": str,
            "return": ReviewDecision,
        })
        self.assertEqual(
            get_type_hints(ReviewDecision)["disposition"], Literal["acknowledge", "reject", "defer"]
        )
        for disposition in ("acknowledge", "reject", "defer"):
            with self.subTest(disposition=disposition):
                direct = ReviewDecision("proposal-digest", disposition, "session-token")
                returned = decide("proposal-digest", disposition, "session-token")
                self.assertEqual(direct, returned)
                with self.assertRaises(dataclasses.FrozenInstanceError):
                    returned.disposition = "reject"  # type: ignore[misc]
        for proposal_digest, disposition, session_token in (
            ("", "acknowledge", "session-token"),
            (None, "acknowledge", "session-token"),
            ("proposal-digest", "apply", "session-token"),
            ("proposal-digest", None, "session-token"),
            ("proposal-digest", "acknowledge", ""),
            ("proposal-digest", "acknowledge", None),
        ):
            with self.subTest(proposal_digest=proposal_digest, disposition=disposition, session_token=session_token):
                with self.assertRaises((TypeError, ValueError)):
                    ReviewDecision(proposal_digest, disposition, session_token)
                with self.assertRaises((TypeError, ValueError)):
                    decide(proposal_digest, disposition, session_token)

    def test_receipt_validates_every_field_and_stays_frozen(self) -> None:
        receipt = ReviewReceipt("fixture-digest", ("requirement-1",), "engine-1", "proposal-digest", ReviewOutcome.UNKNOWN)
        self.assertEqual(
            tuple(field.name for field in dataclasses.fields(receipt)),
            ("source_fixture_digest", "selected_scope", "engine_version", "proposal_digest", "outcome"),
        )
        with self.assertRaises(dataclasses.FrozenInstanceError):
            receipt.outcome = ReviewOutcome.INCOMPLETE  # type: ignore[misc]
        for source_digest, scope, engine_version, proposal_digest, outcome in (
            ("", ("requirement-1",), "engine-1", "proposal-digest", ReviewOutcome.UNKNOWN),
            (None, ("requirement-1",), "engine-1", "proposal-digest", ReviewOutcome.UNKNOWN),
            ("fixture-digest", ("requirement-1",), "", "proposal-digest", ReviewOutcome.UNKNOWN),
            ("fixture-digest", ("requirement-1",), None, "proposal-digest", ReviewOutcome.UNKNOWN),
            ("fixture-digest", ("requirement-1",), "engine-1", "", ReviewOutcome.UNKNOWN),
            ("fixture-digest", ("requirement-1",), "engine-1", None, ReviewOutcome.UNKNOWN),
            ("fixture-digest", ("requirement-1",), "engine-1", "proposal-digest", "unknown"),
        ):
            with self.subTest(source_digest=source_digest, scope=scope, engine_version=engine_version, proposal_digest=proposal_digest, outcome=outcome):
                with self.assertRaises((TypeError, ValueError)):
                    ReviewReceipt(source_digest, scope, engine_version, proposal_digest, outcome)

    def test_all_dto_and_module_callable_surfaces_exclude_prohibited_api_terms(self) -> None:
        dto_types = (ReviewScope, Finding, ReviewProposal, ReviewDecision, ReviewReceipt)
        for dto_type in dto_types:
            with self.subTest(dto_type=dto_type.__name__):
                self._assert_no_prohibited_terms(
                    dto_type.__name__, *(field.name for field in dataclasses.fields(dto_type)),
                    *get_type_hints(dto_type).values(),
                )
                for name, value in dto_type.__dict__.items():
                    if inspect.isfunction(value):
                        self._assert_no_prohibited_terms(name)
                        self._assert_callable_surface_is_private(value)
        module_callables = {
            name: value
            for name, value in vars(epistemic_review).items()
            if inspect.isfunction(value) and value.__module__ == epistemic_review.__name__
        }
        self.assertEqual(
            tuple(sorted(module_callables)),
            ("_is_subset", "_require_findings", "_require_ids", "_require_text", "decide"),
        )
        for name, value in module_callables.items():
            with self.subTest(callable=name):
                self._assert_no_prohibited_terms(name)
                self._assert_callable_surface_is_private(value)

    def test_closed_ast_allowlist_rejects_synthetics_before_accepting_private_module(self) -> None:
        accepted_sources = (
            "from dataclasses import dataclass\n",
            "from enum import StrEnum\n",
            "from typing import Literal\n",
            "isinstance(value, str)\n",
            "TypeError('bad')\n",
            "ValueError('bad')\n",
            "any(item for item in values)\n",
            "all(item for item in values)\n",
            "dataclass(frozen=True)\n",
            "type(value)\n",
            "_require_ids(value, 'value')\n",
            "_require_ids(value, 'value', allow_empty=True)\n",
            "_is_subset(value, allowed)\n",
            "_require_text(value, 'value')\n",
            "_require_findings(value)\n",
            "ReviewDecision(proposal_digest, disposition, session_token)\n",
            "value.strip()\n",
            "item.strip()\n",
            "self.reason.strip()\n",
        )
        for source in accepted_sources:
            with self.subTest(accepted_source=source):
                self._assert_policy_allows(source)

        rejected_sources = (
            "import os\n",
            "from pathlib import Path\n",
            "from dataclasses import dataclass as alias\n",
            "(registry := {})\n",
            "eval('import os')\n",
            "exec('import os')\n",
            "globals().update({})\n",
            "locals().update({})\n",
            "vars().update({})\n",
            "print('output')\n",
            "def any(items):\n    return True\nany(())\n",
            "logger.info('output')\n",
            "__import__('os')\n",
            "import_module('os')\n",
            "importlib.import_module('os')\n",
            "builtins.__import__('os')\n",
            "getattr(importlib, 'import_module')('os')\n",
            "importlib['import_module']('os')\n",
            "open('x')\n",
            "Path('x').write_text('x')\n",
            "subprocess.run(['x'])\n",
            "socket.socket()\n",
            "urllib.request.urlopen('x')\n",
            "json.dumps({})\n",
            "pickle.dump({}, target)\n",
            "getattr(Path('x'), 'write_text')('x')\n",
            "subprocess['run'](['x'])\n",
            "registry = {}\n",
            "cache: dict = {}\n",
            "registry += []\n",
            "if True:\n    registry = {}\n",
            "try:\n    cache = {}\nexcept Exception:\n    pass\n",
            "for value in ():\n    registry = {}\n",
            "with context:\n    cache = {}\n",
            "match value:\n    case _:\n        registry = {}\n",
            "def load():\n    loader = __import__\n    return loader('os')\n",
            "def load():\n    loader = importlib.import_module\n    return loader('os')\n",
            "def output():\n    writer = print\n    writer('output')\n",
            "def typed[T](value: T) -> T:\n    return value\n",
            "def mutate():\n    namespace = mutate.__globals__\n    namespace['registry'] = {}\n",
        )
        for source in rejected_sources:
            with self.subTest(rejected_source=source):
                with self.assertRaises(AssertionError):
                    self._assert_ast_is_inert(source)

        generic_sources = (
            ("function TypeVar", "def generic[T](value: T) -> T:\n    return value\n", "TypeVar"),
            ("function ParamSpec", "def generic[**P](*args: P.args, **kwargs: P.kwargs):\n    return args\n", "ParamSpec"),
            ("function TypeVarTuple", "def generic[*Ts](*args: *Ts):\n    return args\n", "TypeVarTuple"),
            ("class TypeVar", "class Generic[T]:\n    value: T\n", "TypeVar"),
            ("type alias TypeVar", "type Alias[T] = list[T]\n", "TypeVar"),
            ("binder shadows allowed call", "def generic[print]():\n    print('output')\n", "TypeVar"),
            ("binder shadows forbidden name", "def generic[eval](value: eval):\n    return value\n", "TypeVar"),
        )
        for label, source, parameter_node in generic_sources:
            with self.subTest(generic_source=label):
                tree = ast.parse(source, feature_version=(3, 12))
                self.assertTrue(any(type(node).__name__ == parameter_node for node in ast.walk(tree)))
                self.assertTrue(
                    any(getattr(node, "type_params", ()) for node in ast.walk(tree))
                )
                with self.assertRaises(AssertionError):
                    self._assert_ast_is_inert(source)

        indirect_namespace_mutations = (
            "_require_text.__globals__['any'] = print\n",
            "del _require_text.__globals__['any']\n",
            "globals()['any'] = print\n",
            "locals()['any'] = print\n",
            "vars()['any'] = print\n",
            "_require_text.__globals__.update({})\n",
            "def mutate():\n    _require_text.__globals__['any'] = print\n",
            "class Mutator:\n    _require_text.__globals__['any'] = print\n",
            "def mutate():\n    for item in ():\n        globals()['any'] = print\n",
            "def mutate():\n    try:\n        pass\n    except Exception:\n        locals()['any'] = print\n",
            "def mutate():\n    match value:\n        case _:\n            vars()['any'] = print\n",
            "def mutate():\n    return [globals().update({}) for item in ()]\n",
            "def mutate():\n    return (lambda: _require_text.__globals__.update({}))()\n",
            "setattr(_require_text.__globals__, 'any', print)\n",
        )
        for source in indirect_namespace_mutations:
            with self.subTest(indirect_namespace_mutation=source):
                ast.parse(source, feature_version=(3, 12))
                with self.assertRaises(AssertionError):
                    self._assert_ast_is_inert(source)

        path = Path(epistemic_review.__file__)
        self._assert_ast_is_inert(path.read_text(encoding="utf-8"))
        runtime_globals = (
            value for name, value in vars(epistemic_review).items() if not name.startswith("__")
        )
        self.assertFalse(any(isinstance(value, (dict, list, set)) for value in runtime_globals))


    def test_structural_verifier_reports_binding_store_and_canonical_categories(self) -> None:
        self._assert_ast_is_inert(self.canonical_source)

        for name in sorted(self.protected_names):
            cases = (
                (f"{name} = value\n", "protected-binding"),
                (f"def {name}():\n    return None\n", "protected-binding"),
                (f"def helper({name}):\n    return None\n", "protected-binding"),
                (f"def helper():\n    global {name}\n", "protected-binding"),
                (f"({name} := value)\n", "binding"),
            )
            for source, category in cases:
                with self.subTest(protected_name=name, category=category):
                    self._assert_policy_rejects(source, category)

        for source, category in (
            ("for item[0] in ():\n    pass\n", "store-target"),
            ("item.value = value\n", "store-target"),
            ("del item[0]\n", "store-target"),
            ("_require_text.__globals__['any'] = print\n", "namespace"),
            ("globals().update({})\n", "namespace"),
            ("print('output')\n", "side-effect"),
            ("from os import system\n", "import"),
        ):
            with self.subTest(source=source):
                self._assert_policy_rejects(source, category)

        duplicate = self.canonical_source + "\n" + ast.get_source_segment(
            self.canonical_source,
            next(node for node in self.canonical_tree.body if isinstance(node, ast.FunctionDef) and node.name == "_require_text"),
        )
        self._assert_policy_rejects(
            duplicate, "canonical-exception", require_canonical_exceptions=True
        )

        missing_tree = ast.parse(self.canonical_source, feature_version=(3, 12))
        missing_tree.body = [
            node for node in missing_tree.body
            if not (isinstance(node, ast.ImportFrom) and node.module == "typing")
        ]
        missing = ast.unparse(missing_tree)
        self._assert_policy_rejects(
            missing, "canonical-exception", require_canonical_exceptions=True
        )

        nested_fn = ast.get_source_segment(
            self.canonical_source,
            next(node for node in self.canonical_tree.body if isinstance(node, ast.FunctionDef) and node.name == "_require_text"),
        )
        nested = self.canonical_source + "\nif True:\n" + "\n".join("    " + line for line in nested_fn.splitlines())
        self._assert_policy_rejects(nested, "protected-binding")

        altered_tree = ast.parse(self.canonical_source, feature_version=(3, 12))
        altered_tree.body[0].value.value += " altered"
        with self.assertRaisesRegex(AssertionError, "canonical-mismatch"):
            self._assert_ast_is_inert(ast.unparse(altered_tree))

        extra_root = self.canonical_source + "\npass\n"
        with self.assertRaisesRegex(AssertionError, "direct-root-sequence"):
            self._assert_ast_is_inert(extra_root)

if __name__ == "__main__":
    unittest.main()
