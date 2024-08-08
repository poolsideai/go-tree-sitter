package zig

// #cgo CFLAGS: -std=c11 -fPIC
// #include "parser.h"
//const TSLanguage *tree_sitter_zig();
// // NOTE: if your language has an external scanner, add it here.
import "C"

import (
	"unsafe"

	sitter "github.com/smacker/go-tree-sitter"
)

// Get the tree-sitter Language for this grammar.
func Language() unsafe.Pointer {
	return unsafe.Pointer(C.tree_sitter_zig())
}

// yang: add this to make it work with what forge expects.
func GetLanguage() *sitter.Language {
	return sitter.NewLanguage(Language())
}
