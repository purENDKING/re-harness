#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

// ------------------------------------------------------------
// Mini VM Target - single-file reverse engineering test target
//
// Goals:
// - stable-ish structs with meaningful fields
// - global variables
// - getter / setter / branch helper functions
// - switch-based opcode dispatcher
// - long-running loop for runtime observation
// - enough control flow and constants to be useful in Ghidra / CE
//
// Build (MSVC):
//   cl /std:c++20 /EHsc /Zi sample_vm_target.cpp
//
// Build (g++/clang++):
//   g++ -std=c++20 -O0 -g sample_vm_target.cpp -o sample_vm_target
// ------------------------------------------------------------

namespace mini_vm {

static std::atomic<bool> g_running{true};
static int g_game_phase = 1;
static int g_tick_count = 0;
static uint32_t g_debug_flags = 0x11;
static int g_last_error_code = 0;

constexpr int kMaxLocals = 8;
constexpr int kMaxOpcodeArgs = 3;
constexpr int kOpcodeSleepThreshold = 3;
constexpr int kCriticalHpThreshold = 25;
constexpr int kDebugFlagVerbose = 0x1;
constexpr int kDebugFlagTraceDispatch = 0x10;

struct Actor {
    int id;
    int hp;
    int max_hp;
    int state;
    int flags;
    int timer;
    int target_id;
    int pos_x;
    int pos_y;
};

struct VMState {
    int current_opcode;
    int pc;
    int last_result;
    int error_code;
    int locals[kMaxLocals];
};

enum Opcode : int {
    OP_NOP = 0,
    OP_GET_STATE = 1,
    OP_SET_TIMER = 2,
    OP_APPLY_DAMAGE = 3,
    OP_BRANCH_IF_HP_LOW = 4,
    OP_TOGGLE_FLAG = 5,
    OP_HEAL = 6,
    OP_SET_TARGET = 7,
    OP_ADVANCE_PHASE = 8,
    OP_MOVE_TO = 9,
    OP_FAIL_IF_INVALID_TARGET = 10,
};

struct Instruction {
    int opcode;
    int a0;
    int a1;
    int a2;
};

int GetActorState(const Actor* actor) {
    if (actor == nullptr) {
        g_last_error_code = 0xE001;
        return -1;
    }
    return actor->state;
}

int IsHpCritical(const Actor* actor) {
    if (actor == nullptr) {
        g_last_error_code = 0xE002;
        return 0;
    }
    return actor->hp < kCriticalHpThreshold ? 1 : 0;
}

void SetActorTimer(Actor* actor, int value) {
    if (actor == nullptr) {
        g_last_error_code = 0xE003;
        return;
    }
    actor->timer = value;
}

void ApplyDamage(Actor* actor, int value) {
    if (actor == nullptr) {
        g_last_error_code = 0xE004;
        return;
    }
    actor->hp -= value;
    if (actor->hp < 0) {
        actor->hp = 0;
        actor->state = 4; // dead
    }
}

void HealActor(Actor* actor, int value) {
    if (actor == nullptr) {
        g_last_error_code = 0xE005;
        return;
    }
    actor->hp += value;
    if (actor->hp > actor->max_hp) {
        actor->hp = actor->max_hp;
    }
}

void MoveActorTo(Actor* actor, int x, int y) {
    if (actor == nullptr) {
        g_last_error_code = 0xE006;
        return;
    }
    actor->pos_x = x;
    actor->pos_y = y;
    actor->state = 2; // moving
}

int ValidateTargetId(int target_id) {
    if (target_id < 0 || target_id > 1024) {
        g_last_error_code = 0xE100;
        return 0;
    }
    return 1;
}

void PrintActorCompact(const Actor& actor) {
    std::cout
        << "Actor{id=" << actor.id
        << ", hp=" << actor.hp << "/" << actor.max_hp
        << ", state=" << actor.state
        << ", flags=0x" << std::hex << actor.flags << std::dec
        << ", timer=" << actor.timer
        << ", target=" << actor.target_id
        << ", pos=(" << actor.pos_x << "," << actor.pos_y << ")"
        << "}";
}

std::string OpcodeName(int opcode) {
    switch (opcode) {
        case OP_NOP: return "NOP";
        case OP_GET_STATE: return "GET_STATE";
        case OP_SET_TIMER: return "SET_TIMER";
        case OP_APPLY_DAMAGE: return "APPLY_DAMAGE";
        case OP_BRANCH_IF_HP_LOW: return "BRANCH_IF_HP_LOW";
        case OP_TOGGLE_FLAG: return "TOGGLE_FLAG";
        case OP_HEAL: return "HEAL";
        case OP_SET_TARGET: return "SET_TARGET";
        case OP_ADVANCE_PHASE: return "ADVANCE_PHASE";
        case OP_MOVE_TO: return "MOVE_TO";
        case OP_FAIL_IF_INVALID_TARGET: return "FAIL_IF_INVALID_TARGET";
        default: return "UNKNOWN";
    }
}

int DispatchOpcode(VMState* vm, Actor* actor, const Instruction& ins) {
    if (vm == nullptr || actor == nullptr) {
        g_last_error_code = 0xE200;
        return -1;
    }

    vm->current_opcode = ins.opcode;
    vm->pc += 1;

    if (g_debug_flags & kDebugFlagTraceDispatch) {
        std::cout << "[dispatch] pc=" << vm->pc
                  << " opcode=" << OpcodeName(ins.opcode)
                  << " args=(" << ins.a0 << ", " << ins.a1 << ", " << ins.a2 << ")\n";
    }

    switch (ins.opcode) {
        case OP_NOP:
            vm->last_result = 0;
            return 0;

        case OP_GET_STATE: {
            int value = GetActorState(actor);
            vm->locals[ins.a0 & 7] = value;
            vm->last_result = value;
            return value;
        }

        case OP_SET_TIMER:
            SetActorTimer(actor, ins.a0);
            vm->last_result = actor->timer;
            return actor->timer;

        case OP_APPLY_DAMAGE:
            ApplyDamage(actor, ins.a0);
            vm->last_result = actor->hp;
            return actor->hp;

        case OP_BRANCH_IF_HP_LOW: {
            int critical = IsHpCritical(actor);
            vm->last_result = critical;
            if (critical) {
                actor->state = ins.a0;
                actor->flags |= 0x40;
                return 1;
            }
            return 0;
        }

        case OP_TOGGLE_FLAG:
            actor->flags ^= ins.a0;
            vm->last_result = actor->flags;
            return actor->flags;

        case OP_HEAL:
            HealActor(actor, ins.a0);
            vm->last_result = actor->hp;
            return actor->hp;

        case OP_SET_TARGET:
            actor->target_id = ins.a0;
            vm->last_result = actor->target_id;
            return actor->target_id;

        case OP_ADVANCE_PHASE:
            g_game_phase += ins.a0;
            vm->last_result = g_game_phase;
            return g_game_phase;

        case OP_MOVE_TO:
            MoveActorTo(actor, ins.a0, ins.a1);
            vm->last_result = actor->pos_x ^ actor->pos_y;
            return vm->last_result;

        case OP_FAIL_IF_INVALID_TARGET:
            if (!ValidateTargetId(actor->target_id)) {
                vm->error_code = g_last_error_code;
                vm->last_result = -1;
                return -1;
            }
            vm->last_result = 0;
            return 0;

        default:
            vm->error_code = 0xEFFF;
            g_last_error_code = vm->error_code;
            vm->last_result = -1;
            return -1;
    }
}

std::vector<Instruction> BuildProgram() {
    return {
        {OP_GET_STATE, 0, 0, 0},
        {OP_SET_TIMER, 5, 0, 0},
        {OP_APPLY_DAMAGE, 7, 0, 0},
        {OP_BRANCH_IF_HP_LOW, 3, 0, 0},
        {OP_TOGGLE_FLAG, 0x2, 0, 0},
        {OP_HEAL, 4, 0, 0},
        {OP_SET_TARGET, 10, 0, 0},
        {OP_FAIL_IF_INVALID_TARGET, 0, 0, 0},
        {OP_MOVE_TO, 100, 200, 0},
        {OP_ADVANCE_PHASE, 1, 0, 0},
    };
}

void PrintHelp() {
    std::cout << "Commands:\n"
              << "  step [n]       - execute n instructions (default 1)\n"
              << "  run [ticks]    - run ticks with delay\n"
              << "  show           - print actor/vm/global state\n"
              << "  sethp <v>      - set actor hp\n"
              << "  setstate <v>   - set actor state\n"
              << "  target <v>     - set target id\n"
              << "  flags <hex>    - set actor flags (hex allowed, e.g. 0x20)\n"
              << "  phase <v>      - set global game phase\n"
              << "  verbose <0|1>  - toggle verbose dispatch\n"
              << "  reset          - reset actor/vm/ticks\n"
              << "  help           - print help\n"
              << "  quit           - exit\n";
}

void PrintState(const Actor& actor, const VMState& vm) {
    PrintActorCompact(actor);
    std::cout << "\nVM{pc=" << vm.pc
              << ", opcode=" << OpcodeName(vm.current_opcode)
              << ", last_result=" << vm.last_result
              << ", error_code=0x" << std::hex << vm.error_code << std::dec
              << ", local0=" << vm.locals[0]
              << ", local1=" << vm.locals[1]
              << "}\n"
              << "Globals{phase=" << g_game_phase
              << ", tick=" << g_tick_count
              << ", debug_flags=0x" << std::hex << g_debug_flags << std::dec
              << ", last_error=0x" << std::hex << g_last_error_code << std::dec
              << "}\n";
}

void ResetState(Actor& actor, VMState& vm) {
    actor = Actor{1, 100, 100, 1, 0x1, 0, -1, 0, 0};
    vm = VMState{};
    g_game_phase = 1;
    g_tick_count = 0;
    g_last_error_code = 0;
}

bool ExecuteOne(Actor& actor, VMState& vm, const std::vector<Instruction>& program) {
    if (program.empty()) {
        return false;
    }

    const Instruction& ins = program[static_cast<std::size_t>(g_tick_count % static_cast<int>(program.size()))];
    int result = DispatchOpcode(&vm, &actor, ins);

    if (actor.timer > 0) {
        actor.timer -= 1;
    }
    if (actor.state == 2 && actor.timer < kOpcodeSleepThreshold) {
        actor.state = 1;
    }

    ++g_tick_count;

    if (g_debug_flags & kDebugFlagVerbose) {
        std::cout << "[tick] result=" << result << " ";
        PrintActorCompact(actor);
        std::cout << "\n";
    }
    return true;
}

void RunTicks(Actor& actor, VMState& vm, const std::vector<Instruction>& program, int ticks) {
    for (int i = 0; i < ticks && g_running; ++i) {
        ExecuteOne(actor, vm, program);
        std::this_thread::sleep_for(std::chrono::milliseconds(150));
    }
}

int ParseInt(const std::string& s) {
    return std::stoi(s, nullptr, 0);
}

} // namespace mini_vm

int main() {
    using namespace mini_vm;

    Actor actor{1, 100, 100, 1, 0x1, 0, -1, 0, 0};
    VMState vm{};
    const std::vector<Instruction> program = BuildProgram();

    std::cout << "Mini VM Target started. PID-friendly long-running CLI for RE harness testing.\n";
    PrintHelp();
    PrintState(actor, vm);

    std::string line;
    while (g_running) {
        std::cout << "> ";
        if (!std::getline(std::cin, line)) {
            break;
        }
        if (line.empty()) {
            continue;
        }

        std::istringstream iss(line);
        std::string cmd;
        iss >> cmd;

        try {
            if (cmd == "quit" || cmd == "exit") {
                g_running = false;
            } else if (cmd == "help") {
                PrintHelp();
            } else if (cmd == "show") {
                PrintState(actor, vm);
            } else if (cmd == "step") {
                int n = 1;
                if (iss >> n) {}
                RunTicks(actor, vm, program, n);
            } else if (cmd == "run") {
                int n = 10;
                if (iss >> n) {}
                RunTicks(actor, vm, program, n);
            } else if (cmd == "sethp") {
                int v = 0;
                iss >> v;
                actor.hp = v;
                std::cout << "hp set to " << actor.hp << "\n";
            } else if (cmd == "setstate") {
                int v = 0;
                iss >> v;
                actor.state = v;
                std::cout << "state set to " << actor.state << "\n";
            } else if (cmd == "target") {
                int v = 0;
                iss >> v;
                actor.target_id = v;
                std::cout << "target_id set to " << actor.target_id << "\n";
            } else if (cmd == "flags") {
                std::string s;
                iss >> s;
                actor.flags = ParseInt(s);
                std::cout << "flags set to 0x" << std::hex << actor.flags << std::dec << "\n";
            } else if (cmd == "phase") {
                int v = 0;
                iss >> v;
                g_game_phase = v;
                std::cout << "phase set to " << g_game_phase << "\n";
            } else if (cmd == "verbose") {
                int v = 0;
                iss >> v;
                if (v) {
                    g_debug_flags |= kDebugFlagVerbose;
                } else {
                    g_debug_flags &= ~static_cast<uint32_t>(kDebugFlagVerbose);
                }
                std::cout << "verbose=" << ((g_debug_flags & kDebugFlagVerbose) ? 1 : 0) << "\n";
            } else if (cmd == "reset") {
                ResetState(actor, vm);
                std::cout << "state reset\n";
            } else {
                std::cout << "unknown command: " << cmd << "\n";
                PrintHelp();
            }
        } catch (const std::exception& ex) {
            std::cout << "command error: " << ex.what() << "\n";
        }
    }

    std::cout << "Mini VM Target exiting.\n";
    return 0;
}
