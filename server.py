from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent


# =========================================================
# JOB ROLE SKILLS
# =========================================================

JOB_ROLES = {

    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "git",
        "responsive design",
        "rest api"
    ],

    "Backend Developer": [
        "python",
        "flask",
        "sql",
        "rest api",
        "git",
        "database",
        "api"
    ],

    "Full Stack Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "python",
        "flask",
        "sql",
        "git"
    ],

    "Python Developer": [
        "python",
        "flask",
        "django",
        "sql",
        "git",
        "rest api",
        "api"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "pandas",
        "numpy",
        "matplotlib",
        "power bi"
    ],

    "Java Developer": [
        "java",
        "oops",
        "sql",
        "spring boot",
        "rest api",
        "git",
        "database"
    ],

    "QA Engineer": [
        "testing",
        "selenium",
        "python",
        "java",
        "sql",
        "git",
        "automation testing"
    ],

    "DevOps Engineer": [
        "linux",
        "git",
        "docker",
        "aws",
        "azure",
        "ci/cd",
        "kubernetes"
    ]
}


# =========================================================
# LEARNING RECOMMENDATIONS
# =========================================================

LEARNING = {

    "html":
        "Learn HTML structure, forms, semantic elements and accessibility.",

    "css":
        "Learn CSS layouts, Flexbox, Grid, responsive design and animations.",

    "javascript":
        "Learn JavaScript fundamentals, DOM, events, ES6 and APIs.",

    "react":
        "Learn React components, props, state, hooks and routing.",

    "python":
        "Learn Python syntax, functions, OOP, modules and error handling.",

    "flask":
        "Learn Flask routing, REST APIs, request handling and JSON responses.",

    "django":
        "Learn Django models, views, URLs, templates and REST framework.",

    "sql":
        "Learn SQL queries, joins, grouping, subqueries and database design.",

    "git":
        "Learn Git commands, branching, commits, merging and GitHub workflows.",

    "rest api":
        "Learn REST principles, HTTP methods, JSON and API integration.",

    "api":
        "Learn API concepts, requests, responses, authentication and JSON.",

    "database":
        "Learn relational databases, keys, normalization and CRUD operations.",

    "responsive design":
        "Learn mobile-first layouts, media queries and responsive UI.",

    "excel":
        "Learn Excel formulas, functions, pivot tables and data analysis.",

    "pandas":
        "Learn Pandas DataFrames, filtering, grouping and data cleaning.",

    "numpy":
        "Learn NumPy arrays, mathematical operations and numerical processing.",

    "matplotlib":
        "Learn charts, plots and data visualization using Matplotlib.",

    "power bi":
        "Learn Power BI dashboards, Power Query and data visualization.",

    "java":
        "Learn Java fundamentals, OOP, collections, exceptions and JDBC.",

    "oops":
        "Learn classes, objects, inheritance, polymorphism and encapsulation.",

    "spring boot":
        "Learn Spring Boot, REST controllers, dependency injection and JPA.",

    "testing":
        "Learn software testing concepts, test cases and defect reporting.",

    "selenium":
        "Learn Selenium WebDriver, locators, automation and test scripts.",

    "automation testing":
        "Learn automated testing frameworks and test automation practices.",

    "linux":
        "Learn Linux commands, file systems, permissions and shell basics.",

    "docker":
        "Learn Docker images, containers, Dockerfiles and networking.",

    "aws":
        "Learn AWS basics including EC2, S3, IAM and cloud deployment.",

    "azure":
        "Learn Azure services, App Service, storage and cloud deployment.",

    "ci/cd":
        "Learn continuous integration, continuous deployment and pipelines.",

    "kubernetes":
        "Learn Kubernetes pods, deployments, services and containers."
}


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return send_from_directory(
        BASE_DIR,
        "index.html"
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "success",
        "message": "Skill Gap Analyzer backend is running."
    })


# =========================================================
# ANALYZE SKILL GAP
# =========================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "error": "No data received."
            }), 400

        # Get current skills
        current_skills = data.get(
            "current_skills",
            []
        )

        # Get target role
        target_role = data.get(
            "target_role",
            ""
        )

        # Make sure current_skills is a list
        if not isinstance(current_skills, list):

            return jsonify({
                "error": "current_skills must be a list."
            }), 400

        # Convert skills to lowercase
        current_skills = [
            str(skill).strip().lower()
            for skill in current_skills
            if str(skill).strip()
        ]

        # Remove duplicate skills
        current_skills = list(
            dict.fromkeys(current_skills)
        )

        # Check target role
        if not target_role:

            return jsonify({
                "error": "Please select a target role."
            }), 400

        if target_role not in JOB_ROLES:

            return jsonify({
                "error": "Invalid target role."
            }), 400

        # Required skills for selected role
        required_skills = JOB_ROLES[target_role]

        # Convert current skills to set
        current_set = set(current_skills)

        matched = []
        missing = []

        # =====================================================
        # COMPARE SKILLS
        # =====================================================

        for skill in required_skills:

            if skill in current_set:

                matched.append(skill)

            else:

                missing.append(skill)

        # =====================================================
        # MATCH PERCENTAGE
        # =====================================================

        total = len(required_skills)

        if total > 0:

            match_percentage = int(
                (len(matched) / total) * 100
            )

        else:

            match_percentage = 0

        gap_percentage = 100 - match_percentage

        # =====================================================
        # LEARNING PLAN
        # =====================================================

        learning_plan = []

        for skill in missing:

            learning_plan.append({
                "skill": skill,
                "recommendation": LEARNING.get(
                    skill,
                    f"Learn the fundamentals of {skill}."
                )
            })

        # =====================================================
        # LEVEL
        # =====================================================

        if match_percentage >= 80:

            level = "Job Ready"

        elif match_percentage >= 60:

            level = "Almost Ready"

        elif match_percentage >= 40:

            level = "Developing"

        else:

            level = "Beginner"

        # =====================================================
        # SUGGESTIONS
        # =====================================================

        suggestions = []

        if missing:

            suggestions.append(
                f"Focus on {len(missing)} missing skills "
                "for your target role."
            )

        if match_percentage < 60:

            suggestions.append(
                "Build small projects using the missing skills."
            )

        if match_percentage >= 60:

            suggestions.append(
                "Practice interview questions and "
                "real-world projects."
            )

        if not current_skills:

            suggestions.append(
                "Start by learning the core skills "
                "required for your target role."
            )

        # =====================================================
        # RESULT
        # =====================================================

        result = {

            "target_role": target_role,

            "required_skills": required_skills,

            "current_skills": current_skills,

            "matched_skills": matched,

            "missing_skills": missing,

            "match_percentage": match_percentage,

            "gap_percentage": gap_percentage,

            "level": level,

            "learning_plan": learning_plan,

            "suggestions": suggestions

        }

        return jsonify(result), 200

    except Exception as error:

        print(
            "ERROR:",
            repr(error)
        )

        return jsonify({
            "error": str(error)
        }), 500


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5001
        )
    )

    print("")
    print("=" * 60)
    print("SKILL GAP ANALYZER")
    print("=" * 60)
    print("")
    print(f"http://127.0.0.1:{port}")
    print("")
    print("=" * 60)

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )