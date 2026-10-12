"""
roadmap.py - Personalized Skill Learning Roadmap Generator
==========================================================
Generates a structured, prioritized learning roadmap and strategic
upskilling recommendations for skills missing from a candidate's resume.
"""

from typing import List, Dict, Any
from skill_extractor import SKILL_DICTIONARY, SkillDefinition


class RoadmapPlan:
    """Encapsulates the generated learning roadmap and structured recommendations."""

    def __init__(
        self,
        missing_skills: List[str],
        matched_skills: List[str],
        candidate_skills: List[str] = None,
        match_percentage: float = 0.0,
    ):
        self.missing_skills = missing_skills
        self.matched_skills = matched_skills
        # Candidate skills includes both matched skills and bonus resume skills
        self.candidate_skills = set(candidate_skills if candidate_skills is not None else matched_skills)
        self.match_percentage = match_percentage
        self.phases = self._build_phases()
        self.total_estimated_weeks = self._calculate_total_weeks()

    def _build_phases(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Organizes missing skills into 3 sequential learning phases
        based on skill hierarchy, prerequisites, and priority tiers.
        """
        # Tier 1: Core Fundamentals & Prerequisite Foundations
        # Tier 2: Core Technologies, Frameworks, & Databases
        # Tier 3: Advanced Specializations, Cloud, & Deployment
        phase_map: Dict[str, List[Dict[str, Any]]] = {
            "Phase 1: Essential Foundations & Prerequisite Tools": [],
            "Phase 2: Core Frameworks, Libraries & Data Layers": [],
            "Phase 3: Cloud, Production Systems & Advanced AI": [],
        }

        # Sort missing skills by tier then alphabetically
        sorted_skills = sorted(
            self.missing_skills,
            key=lambda s: (
                SKILL_DICTIONARY[s].tier if s in SKILL_DICTIONARY else 99,
                s,
            ),
        )

        for skill_name in sorted_skills:
            skill_def: SkillDefinition = SKILL_DICTIONARY.get(skill_name)
            if not skill_def:
                continue

            # Assess priority badge
            if skill_def.tier == 1:
                priority = "HIGH (Foundational Requirement)"
                target_phase = "Phase 1: Essential Foundations & Prerequisite Tools"
            elif skill_def.tier == 2:
                priority = "MEDIUM-HIGH (Core Tech Stack)"
                target_phase = "Phase 2: Core Frameworks, Libraries & Data Layers"
            else:
                priority = "MEDIUM (Advanced / Production Tech)"
                target_phase = "Phase 3: Cloud, Production Systems & Advanced AI"

            # Check if candidate already has prerequisites (in resume, either matched or bonus)
            unmet_prereqs = [
                p for p in skill_def.prerequisites if p not in self.candidate_skills
            ]

            card = {
                "name": skill_def.name,
                "category": skill_def.category,
                "tier": skill_def.tier,
                "priority": priority,
                "estimated_weeks": skill_def.estimated_weeks,
                "description": skill_def.description,
                "key_topics": skill_def.key_topics,
                "project_idea": skill_def.project_idea,
                "prerequisites": skill_def.prerequisites,
                "unmet_prerequisites": unmet_prereqs,
            }
            phase_map[target_phase].append(card)

        # Filter out empty phases
        return {k: v for k, v in phase_map.items() if len(v) > 0}

    def _calculate_total_weeks(self) -> int:
        """Calculates rough parallelized study timeline."""
        total = sum(
            SKILL_DICTIONARY[s].estimated_weeks
            for s in self.missing_skills
            if s in SKILL_DICTIONARY
        )
        # Assuming realistic dedicated study pace (approx 1-2 skills simultaneously)
        return max(1, round(total * 0.75))

    def get_summary_level(self) -> str:
        """Returns readiness evaluation based on match percentage."""
        if self.match_percentage >= 85.0:
            return "Exceptional Match! You meet nearly all technical requirements."
        elif self.match_percentage >= 70.0:
            return "Strong Candidate! A targeted 2-3 week brush-up will make you a standout applicant."
        elif self.match_percentage >= 50.0:
            return "Moderate Match! You possess core baseline skills but have noticeable framework or tool gaps."
        elif self.match_percentage > 0.0:
            return "Emerging Match. Focus on bridging foundational and framework gaps before applying."
        else:
            return "Early Learner. Comprehensive upskilling is recommended for this target position."

    def get_actionable_tips(self) -> List[str]:
        """Provides high-impact resume enhancement strategies."""
        tips = [
            "Translate Learning to GitHub: Build 1-2 focused repository projects showcasing the missing skills with clean documentation, tests, and CI/CD.",
            "Highlight Adjacent Experience: If you know an equivalent technology (e.g. Flask instead of FastAPI, or PostgreSQL instead of MySQL), explicitly mention your ability to adapt fast.",
            "Use Action Verbs & Metrics: Re-phrase project bullet points on your resume using the STAR method (Situation, Task, Action, Result) with quantitative outcomes.",
            "Target Keyword Placement: Ensure matched skills are represented in both your 'Technical Skills' summary and contextualized within your experience bullet points.",
        ]
        return tips


def generate_roadmap(
    missing_skills: List[str],
    matched_skills: List[str],
    candidate_skills: List[str] = None,
    match_percentage: float = 0.0,
) -> RoadmapPlan:
    """Factory function to build and return a complete RoadmapPlan."""
    return RoadmapPlan(
        missing_skills=missing_skills,
        matched_skills=matched_skills,
        candidate_skills=candidate_skills,
        match_percentage=match_percentage,
    )
