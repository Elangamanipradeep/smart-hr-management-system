import os

from google import genai

from employees.models import Employee
from departments.models import Department
from .analytics import get_hr_analytics

def get_hr_context():
    """
    Collect relevant HR data from the database
    and convert it into text that can be provided to Gemini.
    """

    employees = (
        Employee.objects
        .filter(is_deleted=False)
        .select_related("department")
        .order_by("employee_id")
    )

    departments = Department.objects.all().order_by("name")

    context = []

    # =========================================
    # Departments
    # =========================================

    context.append("DEPARTMENTS:")

    for department in departments:

        context.append(
            f"""
Department Code: {department.department_code}
Department Name: {department.name}
Description: {department.description or "No description"}
"""
        )

    # =========================================
    # Employees
    # =========================================

    context.append("\nEMPLOYEES:")

    for employee in employees:

        status = "Active" if employee.is_active else "Inactive"

        context.append(
            f"""
            Employee ID: {employee.employee_id}
            Name: {employee.full_name}
            Department: {employee.department.name}
            Designation: {employee.designation}
            Salary: ₹{employee.salary}
            Joining Date: {employee.joining_date}
            Status: {status}
            """
        )

    return "\n".join(context)


def ask_gemini(question, history=None):
    """
    Send an HR-related question and optional conversation history
    to Gemini.
    """

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not configured."
        )

    client = genai.Client(
        api_key=api_key
    )

    hr_context = get_hr_context()

    if history is None:
        history = []

    # Keep only the most recent 10 messages
    history = history[-10:]

    conversation_context = ""

    for message in history:

        role = message.get("role")
        content = message.get("content", "").strip()

        if not content:
            continue

        if role == "user":

            conversation_context += (
                f"USER: {content}\n"
            )

        elif role == "assistant":

            conversation_context += (
                f"AI ASSISTANT: {content}\n"
            )

    prompt = f"""
        You are an AI assistant for a Human Resources Management System.

        Your job is to answer questions using ONLY the HR data
        provided below.

        HR DATA:
        {hr_context}

        PREVIOUS CONVERSATION:
        {conversation_context or "No previous conversation."}

        CURRENT USER QUESTION:
        {question}

        INSTRUCTIONS:

        1. Answer based only on the provided HR data and the
        previous conversation.
        2. Use the previous conversation to understand references
        such as "they", "them", "that employee", "that department",
        and similar follow-up questions.
        3. Do not invent employees, departments, salaries, or other
        HR information.
        4. If the requested information is not available, clearly
        say so.
        5. Keep the answer concise and professional.
        6. When listing employees, include their employee ID and name.
        7. Format lists clearly when appropriate.
        8. Do not expose private information such as phone numbers
        or email addresses unless specifically required and
        permitted.
        9. Treat the CURRENT USER QUESTION as the question that
        needs to be answered now.
        10. Do not assume information from the conversation is true
            if it conflicts with the latest HR DATA.
        """

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
    )

    return interaction.output_text

def generate_employee_insights(employee):
    """
    Generate AI insights for a single employee
    using only the employee's HR information.
    """

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not configured."
        )

    client = genai.Client(
        api_key=api_key
    )

    status = "Active" if employee.is_active else "Inactive"

    employee_context = f"""
Employee ID: {employee.employee_id}
Name: {employee.full_name}
Department: {employee.department.name}
Designation: {employee.designation}
Salary: ₹{employee.salary}
Joining Date: {employee.joining_date}
Employment Status: {status}
"""

    prompt = f"""
You are an AI HR assistant for a Human Resources Management System.

Generate a concise professional HR insight for the employee below.

EMPLOYEE DATA:
{employee_context}

INSTRUCTIONS:

1. Use ONLY the employee data provided above.
2. Do not invent performance ratings, achievements,
   skills, attendance, leave information, or other facts.
3. Do not make assumptions about the employee.
4. Do not expose email addresses or phone numbers.
5. Summarize the employee's current HR profile.
6. Mention their department, designation, employment status,
   salary, and joining date when relevant.
7. You may calculate or describe their approximate tenure
   from the joining date, but do not invent other information.
8. Keep the response professional and concise.
9. If something cannot be determined from the available data,
   clearly state that it is not available.
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
    )

    return interaction.output_text



def generate_hr_insights():
    """
    Generate AI-powered insights from HR analytics data.
    """

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not configured."
        )

    client = genai.Client(
        api_key=api_key
    )

    analytics = get_hr_analytics()

    prompt = f"""
You are an AI HR analytics assistant.

Analyze the following HR analytics data and provide useful,
professional insights for an HR administrator.

HR ANALYTICS:

Total Employees: {analytics["total_employees"]}

Active Employees: {analytics["active_employees"]}

Inactive Employees: {analytics["inactive_employees"]}

Average Salary: ₹{analytics["average_salary"]}

Highest Paid Employee:
{analytics["highest_paid_employee"]}

Lowest Paid Employee:
{analytics["lowest_paid_employee"]}

Department Distribution:
{analytics["department_distribution"]}


INSTRUCTIONS:

1. Use ONLY the provided analytics data.
2. Do not invent any information.
3. Identify important workforce patterns.
4. Mention employee activity status.
5. Mention department distribution.
6. Mention salary observations when useful.
7. Keep the response concise and professional.
8. Do not expose phone numbers or email addresses.
9. Use clear bullet points.
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
    )

    return interaction.output_text