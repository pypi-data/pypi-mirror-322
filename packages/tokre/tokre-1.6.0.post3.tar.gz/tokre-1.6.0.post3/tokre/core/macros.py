"""
This module defines custom Matchers called 'macros' for the tokre pattern matching system.
It includes modules for handling token variants, regular expressions, literal sets, and other pattern matching operations.

These macro `Matcher`s are different from the ones defined in matchers.py because they don't have their own custom syntax.
Instead, to use one, you just use their name given by the DEFINED_MACROS dictionary at the bottom of the page inside square brackets.

Examples
-----------
[BEGIN]
    matches the begin token

[re pattern=`( b).*`]
    matches tokens that start with ` b`

[re `( b).*`]
    equivalent to previous

[pos]
    inserts positional information if you're trying to do feature prediction


These are nice because it's really easy to add new matchers without messing with the parser! It makes tokre more easily extensible.

Supported argument types: ints, strings (surrounded by backticks), bools (True/False), and other matchers/macros.

The documentation for this and the whole library is pretty bad currently.
Please reach out (@NoaNabeshima on twitter) if you have questions or would like to help me document/clean up my research code.
"""

from tokre.core.matchers import (
    Embed,
    Mixer,
    VarRef,
    PartialMatch,
    randstr,
    toks_eq,
    Matcher,
)
from torch import nn
import regex as re
from frozendict import frozendict


def tok_split(s):
    """Split a string into tokens using the tokre tokenizer."""
    tok_ids = tokre.enc(s)
    return [tokre.dec([tok_id]) for tok_id in tok_ids]


def get_literal_variants(tok_literal: list[str]):
    """Get variants of a token literal with and without leading space."""
    literal_str = ("".join(tok_literal)).strip()
    variants = [tok_split(literal_str), tok_split(" " + literal_str)]
    return variants


class BEGIN(Matcher):
    """Module that matches a special [BEGIN] token."""

    def __init__(self):
        super().__init__()
        self.name = f"BEGIN:{randstr()}"

    def get_partial_match_extensions(self, toks, partial, reversed):
        if toks[partial.end] == "[BEGIN]":
            return [
                PartialMatch(
                    name=self.name,
                    start=partial.end,
                    end=partial.end + 1,
                    defns=partial.defns,
                    data=None,
                )
            ]
        else:
            return []


class AbsPos(Matcher):
    """Module that embeds absolute positions in the token sequence."""

    def __init__(self, max_pos_idx=100_000):
        super().__init__()
        self.name = f"pos:{randstr()}"
        self.pos_embed = Embed(max_pos_idx)

    def get_partial_match_extensions(self, toks, partial, reversed):
        return [
            PartialMatch(
                name=self.name,
                start=partial.end,
                end=partial.end,
                defns=partial.defns,
                data=self.pos_embed(partial.end),
            )
        ]


class VarVariant(Matcher):
    """Module that matches variants of a variable reference string."""

    def __init__(self, var_ref):
        super().__init__()
        assert isinstance(var_ref, VarRef), var_ref
        self.name = f"VarVariant:{var_ref}:{randstr()}"
        self.var_name = var_ref.var_name

    def get_partial_match_extensions(self, toks, partial, reversed):
        res = []
        if self.var_name in partial.defns:
            var_toks = partial.defns[self.var_name]
            variants = get_literal_variants(var_toks)
            for variant in variants:
                if toks_eq(toks[partial.end : partial.end + len(variant)], variant):
                    res.append(
                        PartialMatch(
                            name=self.name,
                            start=partial.end,
                            end=partial.end + len(variant),
                            defns=partial.defns,
                            data=None,
                        )
                    )
        return res


class VarVariantPrefix(Matcher):
    """Module that matches prefixes of variable reference variants."""

    def __init__(self, var_ref, max_len=128):
        super().__init__()
        assert isinstance(var_ref, VarRef) or isinstance(var_ref, str), var_ref
        self.name = f"VarVariantPrefix:{str(var_ref)}:{randstr()}"

        self.var_name = str(var_ref) if isinstance(var_ref, str) else var_ref.var_name
        self.var_len_and_prefix_idx = Embed((max_len + 1, max_len + 1))
        self.max_len = max_len

    def get_partial_match_extensions(self, toks, partial, reversed):
        res = []
        if self.var_name in partial.defns:
            var_toks = partial.defns[self.var_name]
            variants = get_literal_variants(var_toks)
            assert all([len(variant) <= self.max_len for variant in variants]), variants
            for variant in variants:
                for prefix_len in range(1, len(variant) + 1):
                    if toks_eq(
                        toks[partial.end : partial.end + prefix_len],
                        variant[:prefix_len],
                    ):
                        res.append(
                            PartialMatch(
                                name=self.name,
                                start=partial.end,
                                end=partial.end + prefix_len,
                                defns=partial.defns,
                                data=self.var_len_and_prefix_idx(
                                    len(variant), prefix_len
                                ),
                            )
                        )
        return res


class TokRegex(Matcher):
    """Module that matches individual tokens using regular expressions."""

    def __init__(self, pattern, search=False):
        super().__init__()
        self.name = f"TokRegex:{pattern}:{randstr()}"
        self.pattern = pattern
        self.search = search

    def get_partial_match_extensions(self, toks, partial, reversed):
        if partial.end == len(toks):
            return []

        tok = toks[partial.end]

        if (self.search and re.search(self.pattern, tok)) or re.fullmatch(
            self.pattern, tok
        ):
            return [
                PartialMatch(
                    name=self.name,
                    start=partial.end,
                    end=partial.end + 1,
                    defns=partial.defns,
                    data=None,
                )
            ]
        else:
            return []


class FlexRegex(Matcher):
    """Module that matches tokens using regular expressions with flexible spacing and capitalization."""

    def __init__(self, pattern, search=False):
        super().__init__()
        self.name = f"FlexRegex:{pattern}:{randstr()}"
        self.pattern = pattern
        self.search = search
        self.spacing = Embed(2)
        self.capitalization = Embed(6)
        self.mixer = Mixer(2, linear=True, bilinear=True)

    def get_partial_match_extensions(self, toks, partial, reversed):
        if partial.end == len(toks):
            return []

        tok = toks[partial.end]

        stripped_tok = tok.strip()
        normalized_tok = stripped_tok.lower()

        if (self.search and re.search(self.pattern, normalized_tok)) or re.fullmatch(
            self.pattern, normalized_tok
        ):
            capitalization = (
                0
                if len(stripped_tok) == 0
                else (
                    1
                    if stripped_tok.islower()
                    else (
                        2
                        if stripped_tok.isupper()
                        else (
                            3
                            if (
                                stripped_tok[0].isupper()
                                and len(stripped_tok) > 1
                                and stripped_tok[1:].islower()
                            )
                            else 4 if stripped_tok[0].isupper() else 5
                        )
                    )
                )
            )
            return [
                PartialMatch(
                    name=self.name,
                    start=partial.end,
                    end=partial.end + 1,
                    defns=partial.defns,
                    data=[
                        self.spacing(int(tok[0] == " ")),
                        self.capitalization(capitalization),
                    ],
                )
            ]
        else:
            return []


class TokRegexSet(Matcher):
    """Module that matches tokens from a pre-computed set of tokens matching a regex pattern."""

    def __init__(self, pattern, search=False):
        super().__init__()
        self.name = f"TokRegexSet:{pattern}:{randstr()}"
        self.pattern = pattern
        self.search = search

        if search is True:
            self.toks = {
                tok for tok in tokre.get_all_toks() if re.search(self.pattern, tok)
            }
        else:
            self.toks = {
                tok for tok in tokre.get_all_toks() if re.fullmatch(self.pattern, tok)
            }

    def get_partial_match_extensions(self, toks, partial, reversed):
        if partial.end == len(toks) and not reversed:
            return []

        if partial.end == len(toks) and reversed:
            return []

        tok = toks[partial.end]

        if tok in self.toks:
            return [
                PartialMatch(
                    name=self.name,
                    start=partial.end,
                    end=partial.end + 1,
                    defns=partial.defns,
                    data=None,
                )
            ]
        else:
            return []


class Prefix(Matcher):
    """Module that matches prefixes of another module's matches. This is a bit artificial because it requires looking to the future."""

    def __init__(self, child_module, max_len=10):
        super().__init__()
        self.name = f"Prefix:{randstr()}"
        self.child_module = child_module
        self.max_len = max_len
        self.match_len_and_prefix_len = Embed((max_len, max_len))
        self.mixer = Mixer(2, linear=True, bilinear=True)

    def get_partial_match_extensions(self, toks, partial, reversed):
        matches = self.child_module.get_partial_match_extensions(
            toks, partial, reversed
        )
        res = []
        for match in matches:
            for prefix_end in range(match.start + 1, match.end + 1):
                res.append(
                    PartialMatch(
                        name=self.name,
                        start=match.start,
                        end=prefix_end,
                        defns=match.defns,
                        data=[
                            match,
                            self.match_len_and_prefix_len(
                                match.end - match.start, prefix_end - match.start
                            ),
                        ],
                    )
                )
        return res


import tokre
import json

import torch
from tokre.core.matchers import PartialMatch


class TrieNode:
    """Node in a trie data structure."""

    def __init__(self):
        self.children = {}
        self.is_end = False
        self.value = None


class Trie:
    """Trie data structure for efficient prefix matching."""

    def __init__(self, literals, values=None):
        self.root = TrieNode()
        if values is None:
            values = literals
        for literal, value in zip(literals, values):
            self.insert(literal, value)

    def insert(self, literal, value):
        node = self.root
        for tok_string in literal:
            if tok_string not in node.children:
                node.children[tok_string] = TrieNode()
            node = node.children[tok_string]
        node.is_end = True
        node.value = value

    def prefixes(self, token_strs):
        result = []
        node = self.root
        for i, tok_string in enumerate(token_strs):
            if tok_string not in node.children:
                break
            node = node.children[tok_string]
            if node.is_end:
                result.append(node.value)
        return result


class LiteralSet(Matcher):
    """Module that matches literals from a pre-defined set loaded from a JSON file."""

    def __init__(self, literal_name):
        super().__init__()
        self.name = f"Literalset:{literal_name}:{randstr()}"

        with open(tokre.get_workspace() / (literal_name + ".json")) as f:
            data = json.load(f)
        assert isinstance(data, dict)
        assert "literal_toks" in data

        self.literal_set = [tuple(it) for it in data["literal_toks"]]
        self.trie = Trie(self.literal_set)

        self.reversed_trie = Trie([toks[::-1] for toks in self.literal_set])

        self.literal_idx = Embed(len(self.literal_set))

        self.mixer = Mixer(1, linear=True)

    def get_partial_match_extensions(self, toks, partial, reversed):
        trie = self.trie if reversed is False else self.reversed_trie

        res = []
        forward_toks = toks[partial.end :]

        matching_prefixes = trie.prefixes(forward_toks)
        for prefix in matching_prefixes:
            prefix = prefix if reversed is False else prefix[::-1]
            res.append(
                PartialMatch(
                    name=self.name,
                    start=partial.end,
                    end=partial.end + len(prefix),
                    defns=partial.defns,
                    data=[self.literal_idx(self.literal_set.index(prefix))],
                )
            )

        return res


class Redefine(Matcher):
    """Module that redefines a variable under a new name."""

    def __init__(
        self,
        var_name: str,
        new_var_name: str,
    ):
        self.name = f"Redefine:{randstr()}"
        self.var_name = var_name
        self.new_var_name = new_var_name

    def get_partial_match_extensions(self, toks, partial, reversed):
        if self.var_name in partial.defns:
            new_defns = {k: v for (k, v) in partial.defns.items() if k != self.var_name}
            new_defns[self.new_var_name] = partial.defns[self.var_name]
            return [
                PartialMatch(
                    name=self.name,
                    start=partial.end,
                    end=partial.end,
                    defns=frozendict(new_defns),
                    data=None,
                )
            ]
        else:
            return [
                PartialMatch(
                    name=self.name,
                    start=partial.end,
                    end=partial.end,
                    defns=partial.defns,
                    data=None,
                )
            ]


# Dictionary mapping macro names to their implementing classes
DEFINED_MACROS = {
    "var_variant_prefix": VarVariantPrefix,
    "re": TokRegex,
    "re_tok_set": TokRegexSet,
    "literal_set": LiteralSet,
    "literals": LiteralSet,
    "prefix": Prefix,
    "var_variant": VarVariant,
    "BEGIN": BEGIN,
    "redefine": Redefine,
    "pos": AbsPos,
    "flex": FlexRegex,
}
