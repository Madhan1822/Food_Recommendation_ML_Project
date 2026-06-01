from ml_utils import hybrid_recommendation

def get_ai_response(
    user_id,
    question
):

    question = question.lower()

    if "lunch" in question:

        recommendations = (
            hybrid_recommendation(
                user_id,
                "Lunch"
            )
        )

        response = "🍽 Recommended Lunch Items:\n\n"

        for food, score in recommendations[:3]:

            response += f"• {food}\n"

        return response

    elif "morning" in question:

        recommendations = (
            hybrid_recommendation(
                user_id,
                "Morning"
            )
        )

        response = "☀ Recommended Morning Items:\n\n"

        for food, score in recommendations[:3]:

            response += f"• {food}\n"

        return response

    elif "evening" in question:

        recommendations = (
            hybrid_recommendation(
                user_id,
                "Evening"
            )
        )

        response = "🌙 Recommended Evening Items:\n\n"

        for food, score in recommendations[:3]:

            response += f"• {food}\n"

        return response

    else:

        return """
Try asking:

• What should I eat for lunch?

• What should I eat in the morning?

• Suggest evening snacks.
"""