"""
test_analyzer.py - Comprehensive Unit Tests for Resume Keyword Analyzer
========================================================================
Validates skill extraction, boundary handling, text normalization,
match score calculation, roadmap generation, and edge cases.
"""

import unittest
from skill_extractor import (
    SKILL_DICTIONARY,
    normalize_text,
    extract_skills,
    calculate_match,
    get_all_skills_by_category,
)
from roadmap import generate_roadmap


class TestSkillExtractor(unittest.TestCase):
    """Tests skill extraction and NLP normalization rules."""

    def test_all_33_required_skills_present_in_dictionary(self):
        """Verifies all 33 required skills exist in the skill dictionary."""
        required_skills = [
            "Python", "Java", "C++", "JavaScript", "React", "Node.js", "HTML", "CSS",
            "SQL", "MySQL", "MongoDB", "Machine Learning", "Deep Learning", "NLP",
            "Generative AI", "Flask", "Django", "FastAPI", "REST API", "Git", "GitHub",
            "Docker", "AWS", "Linux", "Data Structures", "Algorithms", "Pandas",
            "NumPy", "TensorFlow", "PyTorch", "Power BI", "Excel", "Communication Skills",
        ]
        for skill in required_skills:
            self.assertIn(skill, SKILL_DICTIONARY, f"Missing required skill: {skill}")

    def test_text_normalization(self):
        """Tests unicode replacement, lowercasing, and spacing normalization."""
        raw = "Expert in  Python,   \t\n C++, and ‘SQL’—with “Docker”!"
        normalized = normalize_text(raw)
        self.assertIn("python", normalized)
        self.assertIn("c++", normalized)
        self.assertIn("sql", normalized)
        self.assertIn("docker", normalized)
        self.assertNotIn("‘", normalized)
        self.assertNotIn("“", normalized)

    def test_boundary_handling_c_plus_plus(self):
        """Verifies C++ matches properly and doesn't conflict with other words."""
        text = "Proficient in C++, Python, and C#."
        skills = extract_skills(text)
        self.assertIn("C++", skills)
        self.assertIn("Python", skills)

    def test_boundary_handling_java_vs_javascript(self):
        """Verifies Java is not falsely detected when only JavaScript is present."""
        text_js_only = "Strong experience with JavaScript frontend engineering."
        skills_js = extract_skills(text_js_only)
        self.assertIn("JavaScript", skills_js)
        self.assertNotIn("Java", skills_js)

        text_both = "Core Java backend and JavaScript frontend."
        skills_both = extract_skills(text_both)
        self.assertIn("Java", skills_both)
        self.assertIn("JavaScript", skills_both)

    def test_boundary_handling_sql_vs_mysql(self):
        """Verifies SQL and MySQL distinction."""
        text_mysql = "Database administration using MySQL."
        skills = extract_skills(text_mysql)
        self.assertIn("MySQL", skills)
        self.assertNotIn("SQL", skills)

        text_both = "Proficient in SQL and MySQL."
        skills_both = extract_skills(text_both)
        self.assertIn("SQL", skills_both)
        self.assertIn("MySQL", skills_both)

    def test_multi_word_and_acronym_skills(self):
        """Verifies multi-word skills and aliases (e.g. GenAI, DSA, REST API)."""
        text = "Experienced in Generative AI (GenAI), Data Structures and Algorithms (DSA), and RESTful APIs."
        skills = extract_skills(text)
        self.assertIn("Generative AI", skills)
        self.assertIn("Data Structures", skills)
        self.assertIn("Algorithms", skills)
        self.assertIn("REST API", skills)

    def test_soft_skills_extraction(self):
        """Verifies communication skills matching variants."""
        variants = [
            "Excellent communication skills",
            "Effective communication and teamwork",
            "Strong interpersonal skills",
            "Demonstrated written communication",
        ]
        for variant in variants:
            skills = extract_skills(variant)
            self.assertIn("Communication Skills", skills, f"Failed for: {variant}")


class TestMatchCalculation(unittest.TestCase):
    """Tests match percentage and set difference calculations."""

    def test_standard_match_percentage(self):
        """Tests standard partial match calculation."""
        resume_skills = {"Python", "SQL", "Git", "Docker"}
        job_skills = {"Python", "SQL", "Docker", "AWS", "FastAPI"}
        # Matched: Python, SQL, Docker (3)
        # Missing: AWS, FastAPI (2)
        # Total job: 5 -> 3/5 = 60.0%
        result = calculate_match(resume_skills, job_skills)
        self.assertEqual(result["match_percentage"], 60.0)
        self.assertEqual(result["matched_skills"], ["Docker", "Python", "SQL"])
        self.assertEqual(result["missing_skills"], ["AWS", "FastAPI"])
        self.assertEqual(result["bonus_skills"], ["Git"])
        self.assertEqual(result["match_count"], 3)
        self.assertEqual(result["missing_count"], 2)

    def test_zero_job_skills_edge_case(self):
        """Verifies graceful handling when no skills are in job description."""
        resume_skills = {"Python", "Git"}
        job_skills = set()
        result = calculate_match(resume_skills, job_skills)
        self.assertEqual(result["match_percentage"], 0.0)
        self.assertFalse(result["has_job_skills"])
        self.assertEqual(result["matched_skills"], [])
        self.assertEqual(result["missing_skills"], [])

    def test_zero_resume_skills_edge_case(self):
        """Verifies 0% match when resume contains no recognized skills."""
        resume_skills = set()
        job_skills = {"Python", "Django"}
        result = calculate_match(resume_skills, job_skills)
        self.assertEqual(result["match_percentage"], 0.0)
        self.assertEqual(result["missing_skills"], ["Django", "Python"])
        self.assertEqual(result["match_count"], 0)

    def test_perfect_100_percent_match(self):
        """Verifies 100% match when all required skills are present."""
        skills = {"Python", "FastAPI", "Docker", "AWS"}
        result = calculate_match(skills, skills)
        self.assertEqual(result["match_percentage"], 100.0)
        self.assertEqual(len(result["missing_skills"]), 0)


class TestRoadmapGenerator(unittest.TestCase):
    """Tests roadmap synthesis, sequencing, and prerequisite tracking."""

    def test_roadmap_phases_and_tier_sequencing(self):
        """Verifies that missing skills are categorized into correct sequential phases."""
        missing = ["Python", "React", "AWS"]
        matched = []
        roadmap = generate_roadmap(
            missing_skills=missing,
            matched_skills=matched,
            candidate_skills=matched,
            match_percentage=0.0,
        )

        phase_names = list(roadmap.phases.keys())
        self.assertIn("Phase 1: Essential Foundations & Prerequisite Tools", phase_names)
        self.assertIn("Phase 2: Core Frameworks, Libraries & Data Layers", phase_names)
        self.assertIn("Phase 3: Cloud, Production Systems & Advanced AI", phase_names)

        # Check Python is in Phase 1
        phase1_skills = [c["name"] for c in roadmap.phases["Phase 1: Essential Foundations & Prerequisite Tools"]]
        self.assertIn("Python", phase1_skills)

        # Check React is in Phase 2
        phase2_skills = [c["name"] for c in roadmap.phases["Phase 2: Core Frameworks, Libraries & Data Layers"]]
        self.assertIn("React", phase2_skills)

        # Check AWS is in Phase 3
        phase3_skills = [c["name"] for c in roadmap.phases["Phase 3: Cloud, Production Systems & Advanced AI"]]
        self.assertIn("AWS", phase3_skills)

    def test_candidate_skills_satisfy_prerequisites(self):
        """Verifies that candidate skills satisfy prerequisites for missing skills."""
        missing = ["Machine Learning"]
        candidate_skills = ["Python", "Pandas", "NumPy"]
        roadmap = generate_roadmap(
            missing_skills=missing,
            matched_skills=[],
            candidate_skills=candidate_skills,
            match_percentage=0.0,
        )
        card = roadmap.phases["Phase 2: Core Frameworks, Libraries & Data Layers"][0]
        self.assertEqual(card["unmet_prerequisites"], [])


class TestDocumentParser(unittest.TestCase):
    """Tests file upload text extraction (PDF, DOCX, TXT) and error handling."""

    def test_extract_from_txt_file(self):
        """Verifies text extraction from a TXT file object."""
        import io
        from app import extract_text_from_upload
        txt_content = "Software Engineer with Python, React, and Docker.".encode("utf-8")
        file_obj = io.BytesIO(txt_content)
        file_obj.name = "resume.txt"
        ok, text = extract_text_from_upload(file_obj)
        self.assertTrue(ok)
        self.assertIn("Python", text)
        self.assertIn("React", text)

    def test_extract_from_docx_file(self):
        """Verifies text extraction from a DOCX file object."""
        import io
        import docx
        from app import extract_text_from_upload
        doc = docx.Document()
        doc.add_paragraph("Full-Stack Developer with JavaScript and FastAPI.")
        doc_bytes = io.BytesIO()
        doc.save(doc_bytes)
        doc_bytes.seek(0)
        doc_bytes.name = "candidate.docx"
        ok, text = extract_text_from_upload(doc_bytes)
        self.assertTrue(ok)
        self.assertIn("JavaScript", text)
        self.assertIn("FastAPI", text)

    def test_unsupported_file_extension(self):
        """Verifies error handling for unsupported formats (e.g. .png)."""
        import io
        from app import extract_text_from_upload
        file_obj = io.BytesIO(b"fake image data")
        file_obj.name = "photo.png"
        ok, msg = extract_text_from_upload(file_obj)
        self.assertFalse(ok)
        self.assertIn("Unsupported", msg)

    def test_empty_txt_file_handling(self):
        """Verifies error handling when a TXT file is empty."""
        import io
        from app import extract_text_from_upload
        file_obj = io.BytesIO(b"   \n  \t ")
        file_obj.name = "empty.txt"
        ok, msg = extract_text_from_upload(file_obj)
        self.assertFalse(ok)
        self.assertIn("empty", msg.lower())


if __name__ == "__main__":
    unittest.main()
