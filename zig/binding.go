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
func GetLanguage() *sitter.Language {
	ptr := unsafe.Pointer(C.tree_sitter_zig())
	return sitter.NewLanguage(ptr)
}
