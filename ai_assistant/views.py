from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .services import ask_gemini

from .services import ask_gemini, generate_hr_insights, generate_employee_insights

from employees.models import Employee

class AIAskAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        question = request.data.get("question", "").strip()

        history = request.data.get("history", [])

        if not question:

            return Response(
                {
                    "error": "Question is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not isinstance(history, list):

            return Response(
                {
                    "error": "History must be a list."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Keep only valid message objects
        cleaned_history = []

        for message in history[-10:]:

            if not isinstance(message, dict):
                continue

            role = message.get("role")
            content = message.get("content")

            if role not in ["user", "assistant"]:
                continue

            if not isinstance(content, str):
                continue

            content = content.strip()

            if not content:
                continue

            cleaned_history.append(
                {
                    "role": role,
                    "content": content,
                }
            )

        try:

            answer = ask_gemini(
                question,
                cleaned_history,
            )

            return Response(
                {
                    "question": question,
                    "answer": answer,
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as error:

            return Response(
                {
                    "error": str(error)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as error:

            # print(
            #     "AI ASSISTANT ERROR:",
            #     repr(error)
            # )

            return Response(
                {
                    "error": "Unable to process your question."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
                
        
class AIHRInsightsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:

            insights = generate_hr_insights()

            return Response(
                {
                    "insights": insights,
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as error:

            return Response(
                {
                    "error": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as error:
        
            # print("AI HR INSIGHTS ERROR:", repr(error))

            return Response(
                {
                    "error": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            

class AIEmployeeInsightsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, employee_id):

        try:

            employee = Employee.objects.select_related(
                "department"
            ).get(
                id=employee_id,
                is_deleted=False,
            )

        except Employee.DoesNotExist:

            return Response(
                {
                    "error": "Employee not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:

            insights = generate_employee_insights(employee)

            return Response(
                {
                    "employee_id": employee.employee_id,
                    "employee_name": employee.full_name,
                    "insights": insights,
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as error:

            return Response(
                {
                    "error": str(error)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception:

            return Response(
                {
                    "error": "Unable to generate employee insights."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )