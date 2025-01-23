// Copyright (c) 2025 Marcin Zdun
// This code is licensed under MIT license (see LICENSE for details)

#include <fmt/format.h>
#include <args/parser.hpp>
#include <wall/version.hpp>

int main(int argc, char* argv[]) {
	std::string path;
	bool verbose{false};
	long counter{};

	args::null_translator tr{};
	args::parser parser{"",
	                    args::from_main(argc, argv), &tr};

	parser.arg(path, "path").meta("<file>").help("sets the path of foobar");
	parser.set<std::true_type>(verbose, "v")
	    .help("sets the output to be more verbose")
	    .opt();
	parser.arg(counter).meta("N").help(
	    "sets the argument for the plural string");
	parser.parse();

	auto msg = std::string_view{counter == 1 ? "you have one foobar"
	                                         : "you have {0} foobars"};
	fmt::print(fmt::runtime(msg), counter);
	fputc('\n', stdout);
}
