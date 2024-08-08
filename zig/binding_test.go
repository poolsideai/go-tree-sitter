package zig_test

import (
	"testing"

	tree_sitter "github.com/smacker/go-tree-sitter"
	"github.com/smacker/go-tree-sitter/zig"
)

func TestCanLoadZigGrammar(t *testing.T) {
	language := tree_sitter.NewLanguage(zig.Language())
	if language == nil {
		t.Errorf("Error loading Zig grammar")
	}
}
