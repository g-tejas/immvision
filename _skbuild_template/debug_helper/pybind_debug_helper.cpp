#include <pybind11/embed.h>
#include <iostream>
#include <filesystem>
namespace py = pybind11;


std::string string_replace(const std::string& src, const std::string& target, const std::string& repl)
{
    if (src.empty() || target.empty())
        return src;

    std::string result = src;
    size_t idx = 0;
    while(true)
    {
        idx = result.find( target, idx);
        if (idx == std::string::npos)
            break;
        result.replace(idx, target.length(), repl);
        idx += repl.length();
    }
    return result;
}

int main()
{
    std::string THIS_DIR = std::filesystem::path(__FILE__).parent_path().string();

    py::scoped_interpreter guard{};

    std::string cmd = R"(
import sys
sys.argv = [sys.argv[0], '-dev']
sys.path.append("THIS_DIR")
import pybind_debug_helper
    )";
    cmd = string_replace(cmd, "THIS_DIR", THIS_DIR);
    py::exec(cmd);
}
