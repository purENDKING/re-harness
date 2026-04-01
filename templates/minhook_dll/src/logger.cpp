#include <fstream>
#include <string>

static void write_log(const std::string& message) {
    std::ofstream file("runtime.log", std::ios::app);
    file << message << std::endl;
}
