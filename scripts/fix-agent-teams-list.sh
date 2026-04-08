#!/usr/bin/env bash
#
# Fix Agent Teams List - Script Interativo (Bash)
#
# Resolve o problema de agentes não aparecerem na lista "Members with skills"
# da extensão Agent Teams.
#
# Opções:
#   A) Adicionar campo `skills` padrão aos agentes que não têm
#   B) Modificar agent-team.ts para remover o filtro de skills
#   C) Gerar relatório de agentes com/sem skills
#   R) Rollback de backup
#
# Uso: ./scripts/fix-agent-teams-list.sh [A|B|C|R]

set -euo pipefail

# ── Configurações ──────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKUP_DIR="$PROJECT_ROOT/.pi/backups"
REPORT_DIR="$PROJECT_ROOT/.pi/reports"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# ── Cores ───────────────────────────────────────────────────────────────

readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[0;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly BRIGHT='\033[1m'
readonly DIM='\033[2m'
readonly RESET='\033[0m'

# ── Funções de UI ───────────────────────────────────────────────────────

print_header() {
    echo -e "\n${CYAN}════════════════════════════════════════════════════════════${RESET}"
    echo -e "${BRIGHT}  $1${RESET}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════${RESET}\n"
}

print_success() { echo -e "${GREEN}✓ $1${RESET}"; }
print_error() { echo -e "${RED}✗ $1${RESET}"; }
print_warning() { echo -e "${YELLOW}⚠ $1${RESET}"; }
print_info() { echo -e "${BLUE}ℹ $1${RESET}"; }

# ── Funções Auxiliares ────────────────────────────────────────────────────

ensure_dir() {
    local dir="$1"
    [[ ! -d "$dir" ]] && mkdir -p "$dir"
}

create_backup() {
    local file="$1"
    local filename=$(basename "$file")
    local backup_path="$BACKUP_DIR/${filename}_${TIMESTAMP}.bak"

    ensure_dir "$BACKUP_DIR"
    cp "$file" "$backup_path"
    echo "$backup_path"
}

find_agent_files() {
    local agents=()
    local base_dirs=("agents" ".claude/agents" ".pi/agents")

    for dir in "${base_dirs[@]}"; do
        [[ ! -d "$PROJECT_ROOT/$dir" ]] && continue

        while IFS= read -r -d '' file; do
            [[ "$file" =~ \.md$ ]] && agents+=("$file")
        done < <(find "$PROJECT_ROOT/$dir" -type f -name "*.md" -print0 2>/dev/null)
    done

    printf '%s\n' "${agents[@]}"
}

check_has_skills() {
    local file="$1"
    # Check if file has skills field in frontmatter
    awk '/^---$/,/^---$/{if (/skills:/) exit 0} END{exit 1}' "$file" 2>/dev/null
}

get_agent_name() {
    local file="$1"
    awk '/^---$/,/^---$/{if (/name:/) {print; exit}}' "$file" | sed 's/name: *//;s/"//g'
}

get_agent_skills() {
    local file="$1"
    awk '/^---$/,/^---$/{if (/^skills:/ || /^ -/) print}' "$file" | grep '^ -' | sed 's/^ - *//' | tr '\n' ',' | sed 's/,$//;s/^/[/;s/$/]/'
}

# ── Opção A: Adicionar Skills ───────────────────────────────────────────

option_a_add_skills() {
    print_header "Opção A: Adicionar Campo skills"

    local default_skill="${1:-generic}"

    print_info "Default skill to add: ${GREEN}$default_skill${RESET}\n"

    local modified=0
    local skipped=0
    local backups=()

    while IFS= read -r file; do
        [[ ! -f "$file" ]] && continue

        if check_has_skills "$file"; then
            print_info "$(get_agent_name "$file") - already has skills, skipping"
            ((skipped++))
            continue
        fi

        # Backup
        local backup_path=$(create_backup "$file")
        backups+=("$file|$backup_path")

        # Add skills after tools line or before closing ---
        if grep -q "^tools:" "$file"; then
            # Insert after tools line
            sed -i.bak_temp "/^tools:/a skills:\\n - $default_skill" "$file"
            rm -f "${file}.bak_temp"
        else
            # Insert before closing ---
            sed -i.bak_temp "/^---$/i skills:\\n - $default_skill" "$file"
            rm -f "${file}.bak_temp"
        fi

        ((modified++))
        print_success "Updated: $(get_agent_name "$file")"
    done < <(find_agent_files)

    echo -e "\n${CYAN}────────────────────────────────────────────────────────────────────${RESET}"
    print_success "Modified $modified agent file(s)"
    print_info "Skipped $ skipped (already have skills)"
    print_info "Backups saved to: $BACKUP_DIR"

    # Save backup manifest
    local manifest="$BACKUP_DIR/backup-manifest-$TIMESTAMP.json"
    cat > "$manifest" <<EOF
{
  "timestamp": "$(date -Iseconds)",
  "action": "add-skills",
  "defaultSkill": "$default_skill",
  "backups": [
$(for entry in "${backups[@]}"; do
    IFS='|' read -r orig back <<< "$entry"
    echo "    {\"original\": \"$orig\", \"backup\": \"$back\"},"
done | sed '$ s/,$//')
  ]
}
EOF

    print_info "Backup manifest: $manifest"
}

# ── Opção B: Modificar agent-team.ts ───────────────────────────────────

option_b_modify_agent_team() {
    print_header "Opção B: Modificar agent-team.ts"

    local agent_team="$PROJECT_ROOT/extensions/agent-team.ts"

    if [[ ! -f "$agent_team" ]]; then
        print_error "File not found: $agent_team"
        return 1
    fi

    print_info "Target file: $agent_team"

    # Check if already patched
    if grep -q "PATCH: Skills filter removed" "$agent_team"; then
        print_warning "File appears to already be patched!"
        print_info "Use 'R' to rollback if needed"
        return 1
    fi

    # Create backup
    local backup=$(create_backup "$agent_team")
    print_info "Backup created: $backup\n"

    # Apply patches
    local temp_file="$agent_team.tmp"

    # Patch 1: Remove filter from agentCatalog
    awk '
    /\/\/ Build dynamic agent catalog from active team only/ {
        print "// Build dynamic agent catalog from active team only"
        print "\t\t// PATCH: Skills filter removed - show ALL agents in catalog"
        getline
        print "\t\t// Include skills for agents that have them"
        getline
        print "\t\tconst agentCatalog = Array.from(agentStates.values())"
        print "\t\t\t.map(s => {"
        print "\t\t\t\tconst skillInfo = s.def.skills.length > 0"
        print "\t\t\t\t\t? \`\\\\n**Skills:** \${s.def.skills.join(\", \")}\`"
        print "\t\t\t\t\t: \"\";"
        print "\t\t\t\treturn \`### \${displayName(s.def.name)}\\\\n**Dispatch as:** \\\`\${s.def.name}\\\`\\\\n\${s.def.description}\${skillInfo}\`;"
        print "\t\t\t})"
        print "\t\t\t.join(\"\\n\\n\");"
        next
    }
    /const agentsWithSkills = Array\.from\(agentStates\.values\(\)\)\.filter\(s => s\.def\.skills\.length > 0\);/ {
        print "\t\t// PATCH: Show all team members, not just those with skills"
        print "\t\tconst teamMembers = Array.from(agentStates.values()).map(s => displayName(s.def.name)).join(\", \");"
        print "\t\tconst agentsWithSkills = Array.from(agentStates.values()).filter(s => s.def.skills.length > 0);"
        next
    }
    /Members with skills: \$\{teamMembers \|\| "none"\}/ {
        print "\t\tMembers (all): \${teamMembers}"
        next
    }
    { print }
    ' "$agent_team" > "$temp_file"

    if [[ -s "$temp_file" ]]; then
        mv "$temp_file" "$agent_team"
        print_success "Applied patches to agent-team.ts"
        print_info "\nChanges made:"
        print_info "  • Removed skills filter from agent catalog"
        print_info "  • Agent catalog now shows ALL agents"
        print_info "  • Skills are displayed when available"
        print_info "  • 'Members (all)' now shows all team members"
    else
        rm -f "$temp_file"
        print_error "Failed to apply patches"
        return 1
    fi
}

# ── Opção C: Gerar Relatório ───────────────────────────────────────────

option_c_generate_report() {
    print_header "Opção C: Relatório de Skills"

    ensure_dir "$REPORT_DIR"
    local report_file="$REPORT_DIR/agent-skills-report-$TIMESTAMP.txt"

    local total=0
    local with_skills=0
    local without_skills=0

    exec 3> "$report_file"

    echo "Agent Skills Report" >&3
    echo "Generated: $(date -Iseconds)" >&3
    echo "" >&3
    echo "SUMMARY" >&3
    echo "-------" >&3

    while IFS= read -r file; do
        [[ ! -f "$file" ]] && continue
        ((total++))

        local name=$(get_agent_name "$file")
        local has_skills=0

        if check_has_skills "$file"; then
            ((with_skills++))
            has_skills=1
        else
            ((without_skills++))
        fi
    done < <(find_agent_files)

    echo "Total agents: $total" >&3
    echo "With skills: $with_skills" >&3
    echo "Without skills: $without_skills" >&3
    echo "" >&3
    echo "" >&3

    # Detailed report
    echo "AGENTS WITH SKILLS" >&3
    echo "-------------------" >&3

    while IFS= read -r file; do
        [[ ! -f "$file" ]] && continue

        if check_has_skills "$file"; then
            local name=$(get_agent_name "$file")
            echo "" >&3
            echo "$name" >&3
            echo "  File: $file" >&3
            echo "  Skills: $(get_agent_skills "$file")" >&3
        fi
    done < <(find_agent_files)

    echo "" >&3
    echo "" >&3
    echo "AGENTS WITHOUT SKILLS" >&3
    echo "----------------------" >&3

    while IFS= read -r file; do
        [[ ! -f "$file" ]] && continue

        if ! check_has_skills "$file"; then
            local name=$(get_agent_name "$file")
            echo "" >&3
            echo "$name" >&3
            echo "  File: $file" >&3
        fi
    done < <(find_agent_files)

    exec 3>&-

    # Print to console
    echo -e "${CYAN}Total agents found: ${BRIGHT}$total${RESET}\n"

    echo -e "${GREEN}✓ Agents WITH skills ($with_skills):${RESET}"
    while IFS= read -r file; do
        [[ ! -f "$file" ]] && continue
        if check_has_skills "$file"; then
            local name=$(get_agent_name "$file")
            local skills=$(get_agent_skills "$file")
            echo -e "  ${BRIGHT}$name${RESET} ${DIM}[$skills]${RESET}"
        fi
    done < <(find_agent_files)

    echo -e "\n${YELLOW}✗ Agents WITHOUT skills ($without_skills):${RESET}"
    while IFS= read -r file; do
        [[ ! -f "$file" ]] && continue
        if ! check_has_skills "$file"; then
            local name=$(get_agent_name "$file")
            echo -e "  ${BRIGHT}$name${RESET}"
        fi
    done < <(find_agent_files)

    echo -e "\n${CYAN}────────────────────────────────────────────────────────────────────${RESET}"
    print_success "Report saved to: $report_file"
}

# ── Rollback ────────────────────────────────────────────────────────────

rollback_backup() {
    print_header "Rollback from Backup"

    local latest_manifest=$(ls -t "$BACKUP_DIR"/backup-manifest*.json 2>/dev/null | head -1)

    if [[ -z "$latest_manifest" ]]; then
        print_error "No backup manifest found"
        return 1
    fi

    print_info "Found backup: $latest_manifest"

    local restored=0

    # Extract backup paths and restore
    while IFS=':' read -r orig backup; do
        [[ ! -f "$backup" ]] && continue
        cp "$backup" "$orig"
        ((restored++))
        print_success "Restored: $orig"
    done < <(jq -r '.backups[] | "\(.original)|\(.backup)"' "$latest_manifest" 2>/dev/null || \
             grep -oP '"original":\s*"\K[^"]+' "$latest_manifest")

    echo -e "\n${CYAN}────────────────────────────────────────────────────────────────────${RESET}"
    print_success "Restored $restored file(s)"
}

# ── Menu Principal ──────────────────────────────────────────────────────

show_menu() {
    print_header "Agent Teams List - Fix Script"

    echo -e "${BRIGHT}This script fixes the issue where agents don't appear in${RESET}"
    echo -e "${BRIGHT}the 'Members with skills' list.${RESET}\n"

    echo -e "${CYAN}Choose an option:${RESET}"
    echo -e "  ${GREEN}A${RESET} - Add default 'skills' field to agents without it"
    echo -e "  ${GREEN}B${RESET} - Modify agent-team.ts to show ALL agents (remove filter)"
    echo -e "  ${GREEN}C${RESET} - Generate report of agents with/without skills"
    echo -e "  ${YELLOW}R${RESET} - Rollback from backup"
    echo -e "  ${RED}Q${RESET} - Quit\n"
}

# ── Main ───────────────────────────────────────────────────────────────

main() {
    local option="${1:-}"

    # Convert to uppercase
    option=$(echo "$option" | tr '[:lower:]' '[:upper:]')

    case "$option" in
        A)
            option_a_add_skills "${2:-generic}"
            ;;
        B)
            option_b_modify_agent_team
            ;;
        C)
            option_c_generate_report
            ;;
        R)
            rollback_backup
            ;;
        Q)
            echo "Bye!"
            exit 0
            ;;
        *)
            show_menu
            exit 0
            ;;
    esac

    echo -e "\n${CYAN}════════════════════════════════════════════════════════════${RESET}\n"
}

main "$@"
