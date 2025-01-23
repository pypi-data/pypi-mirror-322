module main

import os
import regex as re

// Removes pub, mut, unneeded code, etc.
fn cleaner(code string) string {
	lines := code.split_into_lines()
	mut processed_lines := []string{}
	mut in_function := false
	mut in_struct_or_enum := false

	for line in lines {
		line = line.replace('\t', '    ')
		stripped_line := line.trim_space()

		// Skip lines starting with 'pub mut:'
		if stripped_line.starts_with('pub mut:') {
			continue
		}

		// Remove 'pub ' at the start of struct and function lines
		if stripped_line.starts_with('pub ') {
			line = line.trim_left()[4..] // Remove leading spaces and 'pub '
		}

		// Check if we're entering or exiting a struct or enum
		mut r := re.regex_opt(r'(struct|enum)\s+\w+\s*{') or { panic(err) }
		if r.matches_string(stripped_line) {
			in_struct_or_enum = true
			processed_lines << line
		} else if in_struct_or_enum && '}' in stripped_line {
			in_struct_or_enum = false
			processed_lines << line
		} else if in_struct_or_enum {
			// Ensure consistent indentation within structs and enums
			processed_lines << line
		} else {
			// Handle function declarations
			r = re.regex_opt(r'fn\s+\w+') or { panic(err) }
			if r.matches_string(stripped_line) {
				if '{' in stripped_line {
					// Function declaration and opening brace on the same line
					in_function = true
					processed_lines << line
				} else {
					return error('accolade needs to be in fn line.\n${line}')
				}
			} else if in_function {
				if stripped_line == '}' {
					// Closing brace of the function
					in_function = false
					processed_lines << '}'
				}
				// Skip all other lines inside the function
			} else {
				processed_lines << line
			}
		}
	}

	return processed_lines.join('\n')
}

fn load(path string) !string {
	// Walk over directory, find all .v files recursively.
	// Ignore all imports (import at start of line)
	// Ignore all module ... (module at start of line)
	path = os.expand_env(path)
	if !os.exists(path) {
		panic('The path "${path}" does not exist.')
	}
	// Walk over directory recursively
	os.walk_ext(path, '.v', fn (path string, _ []os.FileInfo) {
		t+=process_file(path)!
}

fn process_file(file_path string) !string {
	lines := os.read_lines(file_path) or { return err }
	// Filter out import and module lines
	filtered_lines := lines.filter(it !in ['import', 'module'].map(it.trim_space()))

	return filtered_lines.join('\n')
}

fn main() {
	// from heroserver.openrpc.parser.example import load_example
	code := load('~/code/git.ourworld.tf/hero/hero_server/lib/openrpclib/parser/examples')
	// Parse the code
	code = cleaner(code)!
	println(code)
}
