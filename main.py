"""
main.py - Resume Keyword Analyzer (Interactive CLI Application)
================================================================
A command-line tool that compares resume text with a job description,
extracts technical skills, calculates match percentage, and generates
a personalized skill improvement roadmap.

Usage:
    python main.py                  # Launches interactive CLI menu
    python main.py --sample         # Runs immediate test with sample data
    python main.py --resume <file> --job <file> [--output <file>]
"""

import os
import sys
import argparse
from typing import Tuple, List, Dict, Any

# Ensure stdout handles UTF-8 gracefully across different Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from skill_extractor import (
    extract_skills,
    calculate_match,
    get_all_skills_by_category,
    SKILL_DICTIONARY,
)
from roadmap import generate_roadmap, RoadmapPlan


SAMPLE_RESUME_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "samples", "sample_resume.txt"
)
SAMPLE_JOB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "samples", "sample_job_description.txt"
)


# =====================================================================
# Terminal UI Formatting Helpers
# =====================================================================

def print_divider(char: str = "=", length: int = 76) -> None:
    """Prints a styled divider line."""
    print(char * length)


def print_header(title: str) -> None:
    """Prints a stylized header section."""
    print_divider("=")
    print(f" {title.center(74)} ")
    print_divider("=")


def print_subheader(title: str) -> None:
    """Prints a minor section header."""
    print(f"\n--- {title} " + "-" * max(2, (70 - len(title))))


def make_progress_bar(percentage: float, width: int = 30) -> str:
    """Returns a visual progress bar representation."""
    clamped = max(0.0, min(100.0, percentage))
    filled_length = int(round(width * clamped / 100))
    bar = "█" * filled_length + "░" * (width - filled_length)
    return f"[{bar}] {percentage:.1f}%"


def load_file_text(filepath: str) -> Tuple[bool, str]:
    """Safely loads text from a file with utf-8 encoding."""
    if not os.path.isfile(filepath):
        return False, f"File not found: {filepath}"
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        if not content.strip():
            return False, f"File is empty: {filepath}"
        return True, content
    except Exception as err:
        return False, f"Error reading file '{filepath}': {err}"


def prompt_multiline_input(prompt_title: str) -> str:
    """
    Allows user to paste multiple lines of text in terminal.
    Terminates when user inputs 'DONE' on a blank line or submits two consecutive blank lines.
    """
    print_divider("-")
    print(f" {prompt_title}")
    print(" (Paste your text below. Type 'DONE' on a new line and press Enter to finish)")
    print_divider("-")

    lines: List[str] = []
    consecutive_empty = 0

    while True:
        try:
            line = input()
        except EOFError:
            break

        if line.strip().upper() == "DONE":
            break

        if line.strip() == "":
            consecutive_empty += 1
            if consecutive_empty >= 2 and len(lines) > 0:
                # Two consecutive empty lines trigger completion
                break
        else:
            consecutive_empty = 0

        lines.append(line)

    return "\n".join(lines).strip()


# =====================================================================
# Core Analysis & Report Generation
# =====================================================================

def format_box_line(left: str, right: str = "", width: int = 74) -> str:
    """Formats a single row within an ASCII summary box with strict width alignment."""
    inner_width = width - 4  # accounted for '|  ' and '  |'
    if right:
        spacing = inner_width - len(left) - len(right)
        if spacing < 1:
            spacing = 1
        content = f"{left}{' ' * spacing}{right}"
    else:
        content = left
    return f"|  {content:<{inner_width}}  |"


def analyze_texts(
    resume_text: str, job_text: str
) -> Tuple[Dict[str, Any], RoadmapPlan, str]:
    """
    Executes the full pipeline:
    1. Extracts skills from resume & job description
    2. Computes keyword match score
    3. Builds the prioritized learning roadmap
    4. Formats a complete human-readable report string
    """
    resume_skills_dict = extract_skills(resume_text)
    job_skills_dict = extract_skills(job_text)

    resume_skill_set = set(resume_skills_dict.keys())
    job_skill_set = set(job_skills_dict.keys())

    match_stats = calculate_match(resume_skill_set, job_skill_set)
    roadmap = generate_roadmap(
        missing_skills=match_stats["missing_skills"],
        matched_skills=match_stats["matched_skills"],
        candidate_skills=list(resume_skill_set),
        match_percentage=match_stats["match_percentage"],
    )

    report_lines: List[str] = []

    def log(line: str = ""):
        report_lines.append(line)

    log("=" * 76)
    log("                   RESUME KEYWORD ANALYSIS REPORT                   ")
    log("=" * 76)
    log()

    # Executive Summary Box
    log("+" + "-" * 74 + "+")
    log(f"| {'EXECUTIVE MATCH SUMMARY':^74} |")
    log("+" + "-" * 74 + "+")
    log(format_box_line("Overall Match Score:", f"{match_stats['match_percentage']:.1f}%"))
    log(format_box_line("Progress:", make_progress_bar(match_stats['match_percentage'], 24)))
    log(format_box_line(f"Candidate Assessment:"))
    log(format_box_line(f"  {roadmap.get_summary_level()}"))
    log(format_box_line(""))
    log(format_box_line("• Unique Skills in Job Description:", str(match_stats['total_job_skills'])))
    log(format_box_line("• Unique Skills Detected in Resume:", str(match_stats['total_resume_skills'])))
    log(format_box_line("• Matched Required Skills:", str(match_stats['match_count'])))
    log(format_box_line("• Missing Required Skills:", str(match_stats['missing_count'])))
    log(format_box_line("• Additional Skills in Resume (Bonus):", str(len(match_stats['bonus_skills']))))
    log("+" + "-" * 74 + "+")
    log()

    # Handling No Job Skills Case
    if not match_stats["has_job_skills"]:
        log("⚠️  NOTICE: NO MATCHABLE TECHNICAL SKILLS DETECTED IN JOB DESCRIPTION")
        log("-" * 76)
        log("The provided job description did not contain any recognized keywords from")
        log("the skill dictionary. Please verify that the job description contains")
        log("technical role requirements, or consider expanding the dictionary in")
        log("skill_extractor.py to include custom company-specific terms.")
        log()
        return match_stats, roadmap, "\n".join(report_lines)

    # Matched Skills Section
    log("✔  MATCHED SKILLS (" + str(match_stats["match_count"]) + ")")
    log("-" * 76)
    if match_stats["matched_skills"]:
        # Group matched skills by category
        matched_by_cat: Dict[str, List[str]] = {}
        for skill_name in match_stats["matched_skills"]:
            cat = SKILL_DICTIONARY[skill_name].category
            matched_by_cat.setdefault(cat, []).append(skill_name)

        for cat, skills in sorted(matched_by_cat.items()):
            log(f"  • {cat}:")
            for s in sorted(skills):
                log(f"      [✓] {s}")
    else:
        log("  (None of the required skills in the job description were found in the resume)")
    log()

    # Missing Skills Section
    log("✖  MISSING SKILLS (" + str(match_stats["missing_count"]) + ")")
    log("-" * 76)
    if match_stats["missing_skills"]:
        missing_by_cat: Dict[str, List[str]] = {}
        for skill_name in match_stats["missing_skills"]:
            cat = SKILL_DICTIONARY[skill_name].category
            missing_by_cat.setdefault(cat, []).append(skill_name)

        for cat, skills in sorted(missing_by_cat.items()):
            log(f"  • {cat}:")
            for s in sorted(skills):
                s_def = SKILL_DICTIONARY.get(s)
                tier_badge = (
                    "Tier 1 [Foundational]"
                    if s_def.tier == 1
                    else "Tier 2 [Core Tech]"
                    if s_def.tier == 2
                    else "Tier 3 [Advanced/Cloud]"
                )
                log(f"      [!] {s:<20} ({tier_badge})")
    else:
        log("  🎉 Phenomenal! 100% of required job skills are present in your resume.")
    log()

    # Bonus Skills Section
    if match_stats["bonus_skills"]:
        log("★  ADDITIONAL RESUME SKILLS (Not required by job, but valuable bonus)")
        log("-" * 76)
        bonus_names = ", ".join(match_stats["bonus_skills"])
        log(f"  {bonus_names}")
        log()

    # ATS Transparency Disclaimer
    log("=" * 76)
    log("⚠️  IMPORTANT ATS DISCLAIMER & METHODOLOGY NOTE")
    log("-" * 76)
    log("• This score is a keyword-based heuristic estimate based on detected skills.")
    log("• It is NOT an official Applicant Tracking System (ATS) score.")
    log("• Real commercial ATS platforms (Workday, Greenhouse, Taleo) and recruiters")
    log("  evaluate years of professional experience, job titles, educational degree,")
    log("  measurable impact (STAR method), and contextual semantic relevance.")
    log("• Use this score as a tactical checklist to identify blind spots and tailor")
    log("  your resume's technical keywords to the job description.")
    log("=" * 76)
    log()

    # Personalized Improvement Roadmap
    if match_stats["missing_skills"]:
        log("🚀  PERSONALIZED IMPROVEMENT ROADMAP & LEARNING PLAN")
        log("=" * 76)
        log(f"Estimated Dedicated Study Duration: ~{roadmap.total_estimated_weeks} weeks")
        log("The missing skills are sequenced below in order of prerequisites & priority:\n")

        for phase_name, skill_cards in roadmap.phases.items():
            log("+" + "=" * 74 + "+")
            log(f"| {phase_name.upper():<72} |")
            log("+" + "=" * 74 + "+")

            for card in skill_cards:
                log(f"\n  ▶ Skill: {card['name']} [{card['category']}]")
                log(f"    Priority:        {card['priority']}")
                log(f"    Est. Learning:   {card['estimated_weeks']} week(s)")
                log(f"    About:           {card['description']}")

                if card["unmet_prerequisites"]:
                    unmet_str = ", ".join(card["unmet_prerequisites"])
                    log(f"    ⚠️ Note:         Recommended prerequisite to cover first: {unmet_str}")

                if card["key_topics"]:
                    topics_str = ", ".join(card["key_topics"])
                    log(f"    Core Topics:     {topics_str}")

                if card["project_idea"]:
                    log(f"    Portfolio Proj:  {card['project_idea']}")

            log()

        # Strategic Resume Tips
        log("\n💡  STRATEGIC RESUME OPTIMIZATION TIPS")
        log("-" * 76)
        for i, tip in enumerate(roadmap.get_actionable_tips(), 1):
            log(f"  {i}. {tip}")
        log()

    log("=" * 76)
    log("                         END OF REPORT                             ")
    log("=" * 76)

    return match_stats, roadmap, "\n".join(report_lines)


# =====================================================================
# Interactive CLI Handlers
# =====================================================================

def run_sample_analysis(export_path: str = None) -> None:
    """Runs instant analysis using provided sample files."""
    print("\n[Loading built-in sample resume & job description...]")
    ok_res, res_text = load_file_text(SAMPLE_RESUME_PATH)
    if not ok_res:
        print(f"Error: {res_text}")
        return

    ok_job, job_text = load_file_text(SAMPLE_JOB_PATH)
    if not ok_job:
        print(f"Error: {job_text}")
        return

    _, _, report = analyze_texts(res_text, job_text)
    print("\n" + report)

    if export_path:
        _save_report(report, export_path)
    else:
        _prompt_export_option(report)


def run_file_analysis(export_path: str = None) -> None:
    """Prompts user for resume and job description file paths."""
    print("\n--- Analyze From Text Files ---")

    while True:
        resume_path = input("Enter the file path for your RESUME (.txt): ").strip()
        if not resume_path:
            print("Path cannot be empty. Please try again.")
            continue
        # Support dragged-and-dropped file quotes in terminal
        resume_path = resume_path.strip("\"'")
        ok, res_text = load_file_text(resume_path)
        if ok:
            break
        print(f"  [!] {res_text}")
        retry = input("  Try another path? (y/n): ").strip().lower()
        if retry != "y":
            return

    while True:
        job_path = input("Enter the file path for the JOB DESCRIPTION (.txt): ").strip()
        if not job_path:
            print("Path cannot be empty. Please try again.")
            continue
        job_path = job_path.strip("\"'")
        ok, job_text = load_file_text(job_path)
        if ok:
            break
        print(f"  [!] {job_text}")
        retry = input("  Try another path? (y/n): ").strip().lower()
        if retry != "y":
            return

    print("\n[Analyzing texts...]")
    _, _, report = analyze_texts(res_text, job_text)
    print("\n" + report)

    if export_path:
        _save_report(report, export_path)
    else:
        _prompt_export_option(report)


def run_pasted_text_analysis(export_path: str = None) -> None:
    """Prompts user to paste resume and job description text into the console."""
    print("\n--- Analyze From Pasted Text ---")

    while True:
        resume_text = prompt_multiline_input("PASTE RESUME TEXT")
        if resume_text.strip():
            break
        print("  [!] Resume text cannot be empty.")
        retry = input("  Try again? (y/n): ").strip().lower()
        if retry != "y":
            return

    while True:
        job_text = prompt_multiline_input("PASTE JOB DESCRIPTION TEXT")
        if job_text.strip():
            break
        print("  [!] Job description text cannot be empty.")
        retry = input("  Try again? (y/n): ").strip().lower()
        if retry != "y":
            return

    print("\n[Analyzing texts...]")
    _, _, report = analyze_texts(resume_text, job_text)
    print("\n" + report)

    if export_path:
        _save_report(report, export_path)
    else:
        _prompt_export_option(report)


def display_supported_skills() -> None:
    """Displays all skills supported by the system categorized."""
    print_header("SUPPORTED SKILL DICTIONARY")
    categories = get_all_skills_by_category()
    total_skills = len(SKILL_DICTIONARY)
    print(f"\nTotal Tracked Skills: {total_skills} across {len(categories)} categories\n")

    for cat_name, skill_list in sorted(categories.items()):
        print(f"▶ {cat_name} ({len(skill_list)} skills):")
        print("   " + ", ".join(skill_list))
        print()

    print_divider("-")
    print("Tip: You can easily add more skills to skill_extractor.py")
    try:
        if sys.stdin.isatty():
            input("\nPress Enter to return to main menu...")
    except (EOFError, KeyboardInterrupt):
        pass


def _prompt_export_option(report_content: str) -> None:
    """Asks the user if they'd like to export the report to a file if in interactive mode."""
    if not sys.stdin.isatty():
        return
    try:
        choice = input("\nWould you like to export this report to a text file? (y/n): ").strip().lower()
        if choice == "y":
            filename = input("Enter output filename (default: analysis_report.txt): ").strip()
            if not filename:
                filename = "analysis_report.txt"
            _save_report(report_content, filename)
    except (EOFError, KeyboardInterrupt):
        pass


def _save_report(report_content: str, filepath: str) -> None:
    """Saves the report content to the designated filepath."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"✔ Successfully saved report to: {os.path.abspath(filepath)}")
    except Exception as err:
        print(f"✖ Failed to save report: {err}")


def interactive_menu() -> None:
    """Main CLI Menu Loop."""
    while True:
        print()
        print_header("RESUME KEYWORD ANALYZER")
        print(" NLP-Based Skill Matching, Gap Analysis & Upskilling Roadmap")
        print_divider("=")
        print(" [1] Quick Test (Run analysis on built-in sample resume & job description)")
        print(" [2] Analyze Custom Files (Provide paths to resume & job files)")
        print(" [3] Paste Raw Text (Paste resume & job description into terminal)")
        print(" [4] View Supported Skills Dictionary & Categories")
        print(" [5] Exit")
        print_divider("-")

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            run_sample_analysis()
        elif choice == "2":
            run_file_analysis()
        elif choice == "3":
            run_pasted_text_analysis()
        elif choice == "4":
            display_supported_skills()
        elif choice == "5":
            print("\nThank you for using Resume Keyword Analyzer. Best of luck with your applications!\n")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.")


# =====================================================================
# Program Entry Point & CLI Arguments
# =====================================================================

def parse_arguments() -> argparse.Namespace:
    """Configures and parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Resume Keyword Analyzer: Compare resume with job description and generate improvement roadmap."
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Run analysis using the bundled sample resume and job description.",
    )
    parser.add_argument(
        "--resume",
        type=str,
        help="Path to resume text file.",
    )
    parser.add_argument(
        "--job",
        type=str,
        help="Path to job description text file.",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to save the generated analysis report text file.",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point for the application."""
    args = parse_arguments()

    if args.sample:
        run_sample_analysis(export_path=args.output)
    elif args.resume and args.job:
        ok_res, res_text = load_file_text(args.resume)
        if not ok_res:
            print(f"Error: {res_text}")
            sys.exit(1)

        ok_job, job_text = load_file_text(args.job)
        if not ok_job:
            print(f"Error: {job_text}")
            sys.exit(1)

        _, _, report = analyze_texts(res_text, job_text)
        print("\n" + report)

        if args.output:
            _save_report(report, args.output)
    elif args.resume or args.job:
        print("Error: Both --resume and --job must be specified together.")
        sys.exit(1)
    else:
        # Default interactive mode
        interactive_menu()


if __name__ == "__main__":
    main()
